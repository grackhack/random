from pprint import pprint
from typing import List

from app import constants
from app.work_with_games import get_raw_data


def emulate(rules: dict) -> List[dict]:
    start = int(rules.get('start'))
    stop = int(rules.get('stop'))
    count_games = int(rules.get('game'))
    game_type = rules.get('game_type')
    max_play = stop - start + 1

    all_stat = {'0': {}, '1': {}}
    for series in [False, True]:
        tmp_dgt = {}
        for digit in constants.GAME_MAP[game_type]['range']:
            mask = f'{int(series)}' * start + f'{int(not series)}'
            games = get_raw_data(str(digit), constants.G1)[:count_games]
            # print(games)
            sts = False
            game_step = 0
            stat = []
            game_round = 0

            for i in range(count_games):
                game_delta = games[count_games - i - start - 1:count_games - i]
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


def calculate_emu_games(stat: dict) -> int:
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
#     res = emulate({'start': 7, 'stop': 11, 'game': 100, 'game_type': 1})
#     pprint(res)
#     all_sum, total = calculate_emu_games(res)
#     pprint(all_sum)
#     print(total)
