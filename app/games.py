import re
from typing import List, Dict, Any, Union

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app import constants
from app import special
from app.types import SeriesRaw, DigitRaw
from app.utils import timing
from config import Config

from abc import ABCMeta, abstractmethod

SPEC_MAP = {
    'k15': special.get_k15,
    'E>O': special.get_even_more_odd,
    'NR': special.get_nr,
    'EVEN': special.get_all_even,
    'ODD': special.get_all_odd,
    'E13': special.get_even13,
    'O13': special.get_odd13,
    'EQ': special.get_eq,
    'MNE': special.get_min_even,
    'MXE': special.get_max_odd,
    'k152': special.get_sum_152,
}


class AbcGame(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_raw_data(self, label: int, limit: int = 0) -> str:
        """Строка 1/0 за все игры для числа и количество"""

    def get_calc_raw_data(self, label: str, limit: int = 0) -> str:
        """строка 1/0 посчитанная по условиям"""

    def get_full_raw_data(self, limit: int = 0) -> DigitRaw:
        """Словарь число: строка 0/1"""

    def get_raw_series(self, label: str, limit: int = 0) -> SeriesRaw:
        """Словарь {'0': {серия: сумма }, '1': {серия: сумма }}"""

    def get_full_series(self, limit: int = 0) -> SeriesRaw:
        """Список всех словарей серий"""

    def get_full_view(self, ser_type: str, limit: int = 0) -> List[Dict[str, str]]:
        """Список серий для отображений"""


class Loto(AbcGame):

    def __init__(self, game_type: str):
        self.game_type = game_type
        self.name = constants.GAME_MAP[game_type]['name']
        self.range = constants.GAME_MAP[game_type]['range']
        self.model = constants.GAME_MAP[game_type]['model']
        self.tbl = constants.GAME_MAP[game_type]['tbl']
        self.base_link = constants.GAME_MAP[game_type]['base_link']
        self.events = constants.GAME_MAP[game_type]['event_list']

    def get_raw_data(self, label: int, limit: int = 0) -> str:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
        limit_str = f'limit {limit}' if limit > 0 else ''
        result = engine.execute("""
                    select array(select (case when de{d:} = TRUE then '1' else '0' end)
                         from {tbl:}
                         order by date desc {limit:})
                    """.format(d=label, tbl=self.tbl, limit=limit_str))
        result = result.fetchone()
        raw = ''.join(result[0])
        return raw

    def get_full_raw_data(self, limit: int = 0) -> DigitRaw:
        full_raw = {}
        for digit in self.range:
            digit_row = self.get_raw_data(digit, limit=limit)
            full_raw[str(digit)] = digit_row
        return full_raw

    def get_full_series(self, limit: int = 0) -> SeriesRaw:
        full_series = {constants.GR: {}, constants.RD: {}}
        for digit in self.range:
            one_ser = self.get_raw_series(str(digit), limit=limit)
            for key, val in one_ser.items():
                full_series[key].update(val)

        for koef in self.events:
            one_ser = self.get_raw_series(koef, limit=limit)
            for key, val in one_ser.items():
                full_series[key].update(val)

        return full_series

    def get_calc_raw_data(self, label: str, limit: int = 0) -> str:
        raw = ''
        if self.game_type == constants.G1 or self.game_type == constants.GTEST:
            de = self.get_full_raw_data(limit=limit)
            raw = SPEC_MAP[label](de)
            return raw
        if self.game_type == constants.G2:
            de = self.get_full_raw_data(limit=limit)
            raw = SPEC_MAP[label](de)
            return raw
        if self.game_type == constants.G3:
            de = self.get_full_raw_data(limit=limit)
            raw = SPEC_MAP[label](de)
            return raw
        return raw

    def get_raw_series(self, label: str, limit: int = 0) -> SeriesRaw:
        if label.isdigit():
            raw = self.get_raw_data(int(label), limit=limit)
        else:
            raw = self.get_calc_raw_data(label, limit=limit)
        series = {}
        series_win = {}
        series_los = {}
        for d in constants.SW:
            ser0 = [m.start() + constants.SERIES_BEGIN_POS for m in re.finditer(constants.SW[d], raw)]
            ser1 = [m.start() + constants.SERIES_BEGIN_POS for m in re.finditer(constants.SL[d], raw)]
            if ser0:
                series_win[d] = ser0
            if ser1:
                series_los[d] = ser1

        series[constants.RD] = series_win
        series[constants.GR] = series_los
        return series

    @staticmethod
    def series_tolist(raw: str) -> List[int]:
        return list(map(int, raw))

    @staticmethod
    def series_for_view(ser: List[int], ser_type: str) -> List[str]:
        """10011 -> .21.. or 1..21"""
        play = 0 if ser_type == constants.RD else 1
        ng = False
        res = []
        cnt = 1
        for i in ser[::-1]:
            if i == play and not ng:
                cnt = 1
                ng = True
                res.append(str(cnt))
            elif i == play and ng:
                cnt += 1
                res.append(str(cnt))
            else:
                res.append('•')
                ng = False
        return res[::-1]

    def get_full_view(self, ser_type: str, limit: int = 0) -> List[Dict[str, str]]:
        games = []
        for digit in self.range:
            raw = self.get_raw_data(digit, limit=limit)
            raw_list = Loto.series_tolist(raw)
            view_ser = Loto.series_for_view(raw_list, ser_type=ser_type)
            games.append({'digit': digit, 'game': view_ser})
        for spec in self.events:
            raw = self.get_calc_raw_data(spec, limit=limit)
            raw_list = Loto.series_tolist(raw)
            view_ser = Loto.series_for_view(raw_list, ser_type=ser_type)
            games.append({'digit': spec, 'game': view_ser})
        return games

    def get_full_stat(self, limit: int = 0) -> Dict[Any, Dict[str, dict]]:
        """
           Количество серйи по всем числам Для игры
           """
        full_info = {}
        for digit in self.range:
            series = self.get_raw_series(str(digit), limit=limit)
            full_counts = Loto.get_full_counts(series)
            full_info[digit] = full_counts
        return full_info

    def get_full_events_stat(self, limit: int = 0) -> Dict[Any, Dict[str, dict]]:
        """Количество серйи по всем спец кэфам для игры"""
        full_info = {}
        for koef in self.events:
            series = self.get_raw_series(koef, limit=limit)
            full_counts = Loto.get_full_counts(series)
            full_info[koef] = full_counts
        return full_info

    @staticmethod
    def get_full_counts(series):
        """Подсчет серии"""
        res = {'W': {}, 'L': {}}
        for game, digs in series.items():
            for d, ser in digs.items():
                size = len(ser)
                if size > 0:
                    res[game][d] = size
        return res

    @staticmethod
    def get_max_series(full_stat) -> int:
        max_ser = {constants.RD: 0, constants.GR: 0}
        for d, digs in full_stat.items():
            for g, ser in digs.items():
                tmp_max = max(map(int, ser.keys())) if ser.keys() else 0
                max_ser[g] = tmp_max if tmp_max > max_ser[g] else max_ser[g]
        return max_ser
