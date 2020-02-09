from pprint import pprint
from typing import List

from app import constants
from app.games import Loto


def emulate(rules: dict) -> List[dict]:
    start = int(rules.get('start'))
    stop = int(rules.get('stop'))
    count_games = int(rules.get('game'))
    game_start = int(rules.get('game_start'))
    game_type = rules.get('game_type')
    game_digit = rules.get('game_digit', '')
    game_ser = rules.get('game_ser', '')
    max_play = stop - start + 1
    loto = Loto(game_type)
    get_func = loto.get_raw_data
    if game_digit:
        if game_digit.isdigit():
            dig = int(game_digit)
            full_range = range(dig, dig + 1)
        else:
            full_range = [game_digit, ]
            get_func = loto.get_calc_raw_data
    else:
        full_range = loto.range

    all_stat = {'0': {}, '1': {}}
    if game_ser == '1':
        range_ser = [False, ]
    elif game_ser == '0':
        range_ser = [True, ]
    else:
        range_ser = [False, True]

    for series in range_ser:
        tmp_dgt = {}
        for digit in full_range:
            mask = f'{int(series)}' * start + f'{int(not series)}'
            games = get_func(digit)[game_start:count_games + 1]
            # print(games)
            sts = False
            game_step = 0
            stat = []
            game_round = 0
            delta_games = count_games - game_start + 1
            for i in range(delta_games):
                game_delta = games[delta_games - i - start - 1:delta_games - i]
                if not game_delta:
                    break
                if sts:
                    game_step += 1
                    if check_win(game_delta, series):
                        # print('win')
                        stat.append({'game_round': game_round,
                                     'attemp': game_step,
                                     'win': True,
                                     'total': 100})
                        sts = False
                        game_step = 0
                    elif game_step == max_play:
                        # print('fail')
                        stat.append({'game_round': game_round,
                                     'attemp': game_step,
                                     'win': False,
                                     'total': -(2 ** game_step) * 100 + 100})
                        sts = False
                        game_step = 0
                    # else:
                    #     print('fail')
                if game_delta.startswith(mask):
                    sts = True
                    game_round = count_games - i - start - 1
                # print(i, game_delta)
            tmp_dgt[digit] = stat
        all_stat[f'{int(series)}'] = tmp_dgt
    return all_stat


def check_win(delta, series):
    return delta[0] == f'{int(not series)}'


def calculate_emu_games(stat: List[dict]) -> int:
    all_sum = {}
    total = 0
    for series, play in stat.items():
        tmp_sum = {}
        for digit, game in play.items():
            tmp_sum[digit] = 0
            for item in game:
                total += item.get('total')
                tmp_sum[digit] += item.get('total')
        all_sum[series] = tmp_sum

    return all_sum, total

# if __name__ == '__main__':
#     res = emulate({'start': '2', 'stop': '3', 'game': '15', 'game_start': '0', 'game_type': '3', 'game_digit': 'NR', 'game_ser': '0'})
#     pprint(res)
#     all_sum, total = calculate_emu_games(res)
#     pprint(all_sum)
#     print(total)
