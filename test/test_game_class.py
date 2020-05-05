import pytest

from app import constants
from app import games
from test.data import game_data


def test_game():
    g = games.Loto(game_type=constants.G1)
    assert g.game_type == constants.G1


@pytest.mark.parametrize('test_data', game_data.FULL_RAWS)
def test_get_full_raw_data(mocker, test_data):
    mocker.patch('app.games.Loto.get_raw_data', return_value=game_data.R1)
    g = games.Loto(game_type=constants.G1)
    raw = g.get_full_raw_data()
    assert test_data['expected_rows'] == raw


@pytest.mark.parametrize('test_data', game_data.FULL_RAWS)
def test_get_calc_raw_data(mocker, test_data):
    mocker.patch('app.games.Loto.get_full_raw_data', return_value=test_data['full_rows'])
    g = games.Loto(game_type=constants.G1)
    raw = g.get_calc_raw_data('L15')
    assert test_data['K15'] == raw


def test_get_full_series(mocker):
    def mock_raw(d: str, limit=0):
        if d.isdigit():
            return game_data.DIG_SER
        else:
            return game_data.SPEC_SER

    mocker.patch('app.games.Loto.get_raw_series', side_effect=mock_raw)
    g = games.Loto(game_type=constants.GTEST)
    raw = g.get_full_series()
    assert game_data.ALL_SERIES == raw


@pytest.mark.parametrize('test_data', game_data.FULL_RAWS)
def test_get_raw_series(mocker, test_data):
    mocker.patch('app.games.Loto.get_raw_data', return_value=game_data.R1)
    mocker.patch('app.games.Loto.get_calc_raw_data', return_value=test_data['K15'])
    g = games.Loto(game_type=constants.G1)
    ser = g.get_raw_series('1')
    ser15 = g.get_raw_series('K15')
    assert test_data['ser1'] == ser
    assert test_data['ser15'] == ser15


def test_ser_tolist():
    assert games.Loto.series_tolist('111') == [1, 1, 1]


def test_ser_for_view():
    ser_list = [1, 1, 1, 0, 0, ]
    red_ser = [constants.FILL_CHAR, constants.FILL_CHAR, constants.FILL_CHAR, '2', '1', ]
    green_ser = ['3', '2', '1', constants.FILL_CHAR, constants.FILL_CHAR]

    assert games.Loto.series_for_view(ser_list, ser_type=constants.RD) == red_ser
    assert games.Loto.series_for_view(ser_list, ser_type=constants.GR) == green_ser


def test_get_full_view(mocker):
    ser_list = '11100'
    spec_list = '11100'
    red_ser = [{'digit': 1, 'game': [constants.FILL_CHAR, constants.FILL_CHAR, constants.FILL_CHAR, '2', '1']},
               {'digit': 'K15', 'game': [constants.FILL_CHAR, constants.FILL_CHAR, constants.FILL_CHAR, '2', '1']}]
    mocker.patch('app.games.Loto.get_raw_data', return_value=ser_list)
    mocker.patch('app.games.Loto.get_calc_raw_data', return_value=spec_list)
    g = games.Loto(game_type=constants.GTEST)
    view = g.get_full_view(ser_type=constants.RD)
    assert view == red_ser


# def test_last_series(mocker):
#     g = games.Loto(game_type=constants.G1)
#     res = g.get_last_series()
#
# def test_prepare_notice(mocker):
#     g = games.Loto(game_type=constants.G1)
#     res = g.prepare_notices()
#     print(res)
# def test_pattern():
#     def get_frame(s0, s1, s2, cnt):
#         pos = len(s0)
#         a = (s0[(pos - cnt - 4):(pos - cnt)],
#              s1[(pos - cnt - 4):(pos - cnt)],
#              s2[(pos - cnt - 4):(pos - cnt)],
#              )
#         return a
#
#     def check_frame(f):
#         DIG=4
#         s = sum([f[0][1:].count('1'), f[1][1:].count('1'), f[2][1:].count('1')])
#         one = f[0][1:].count('1') > 0 and f[1][1:].count('1') > 0 and f[2][1:].count('1') > 0
#         risk = all([f[0][3] == '0', f[1][3] == '0', f[2][3] == '0'])
#         win = all([f[0][0] == '0', f[1][0] == '0', f[2][0] == '0'])
#         half = f[0][0] == '0' and f[1][0] == '0' and f[2][0] == '1'
#         fail = f[0][0] == '1' or f[1][0] == '1'
#         if s >= DIG and one and win and not risk:
#             return 'win'
#         elif s >= DIG and one and half and not risk:
#             return 'half'
#         elif s >= DIG and one and fail and not risk:
#             return 'fail'
#         else:
#             return 'skip'
#
#     g = games.Loto(game_type=constants.G3)
#     s0 = g.get_raw_data('0', limit=1000)
#     s1 = g.get_raw_data('1', limit=1000)
#     s2 = g.get_raw_data('2', limit=1000)
#     # s0 = g.get_raw_data('0')
#     # s1 = g.get_raw_data('1')
#     # s2 = g.get_raw_data('2')
#     cnt = 0
#     stat = {
#         'win': 0,
#         'half': 0,
#         'fail': 0,
#         'skip': 0
#     }
#     resrow = ''
#     while cnt < len(s0):
#         frame = get_frame(s0, s1, s2, cnt)
#         if not frame[0]:
#             break
#         res = check_frame(frame)
#         if res == 'win':
#             resrow += '2'
#         elif res == 'fail':
#             resrow += '1'
#         elif res == 'half':
#             resrow += '3'
#         else:
#             resrow += '0'
#         if res in ('win', 'half'):
#             cnt += 1
#         else:
#             cnt += 1
#         stat[res] += 1
#     print(stat)
#     print(resrow)
#     print('---')