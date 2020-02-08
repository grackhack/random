import re
from app.models import Game, Game2, Game3

GTEST = '0'
G1 = '1'
G2 = '2'
G3 = '3'

RD = 'W'
GR = 'L'
FILL_CHAR = '•'
CNT_REGEX = 120
XRNG = 1000
XTICK = 10
MIN_SERIES = 7
TBL_COL = 300
RAW_LIMIT = 300
KOEF = 1.92
SERIES_BEGIN_POS = 1
MIN_TELE_S = 9
MAX_TELE_S = 25

SHIFT_G2 = 34
SHIFT_G3 = 13

GAME_MAP = {
    '0': {
        'range': range(1, 2),
        'model': Game,
        'tbl': 'test_tbl',
        'base_link': '',
        'name': 'test_game',
        'event_list': ['k15', ],
    },
    '1': {
        'range': range(1, 25),
        'model': Game,
        'tbl': 'game',
        'base_link': 'https://www.stoloto.ru/draw-results/12x24/load',
        'name': '12x24',
        'event_list': ['k15', 'E>O', 'MNE', 'MXE', 'k152'],
    },
    '2': {
        'range': range(1, 27),
        'model': Game2,
        'tbl': 'game2',
        'base_link': 'https://www.stoloto.ru/draw-results/duel/load',
        'name': 'duel',
        'event_list': ['E13', 'O13'],

    },
    '3': {
        'range': range(0, 10),
        'model': Game3,
        'tbl': 'game3',
        'base_link': 'https://www.stoloto.ru/draw-results/top3/load',
        'name': 'top3',
        'event_list': ['NR', 'EQ'],
    },
}


def gen_regexs():
    sw = {}
    sl = {}

    for i in range(1, CNT_REGEX):
        sw[str(i)] = r'(1)0{{{d:}}}(?:$|1)'.format(d=i)
        sl[str(i)] = r'(0)1{{{d:}}}(?:$|0)'.format(d=i)

    return sw, sl


SW, SL = gen_regexs()

PL_GAMES = """
select  p.id,game_time, game_digit, game_win , game_bet, game_result, game_type, game_koef from play p
join play_game pg on p.id = pg.game_id where user_id=%s and p.game_result isnull
"""

PL_GAME_RES = 'select de{de:} from {tbl:} where date> %s order by date limit 1'

UPDATE_SUM = 'update play set game_result = %s where id = %s'

WIN_SUM = """
select case
           when sum(game_result) is null then 0
           else sum(game_result) end -
       case
           when sum(game_bet) is null then 0
           else sum(game_bet)
           end as win
from play p
         join play_game pg
              on p.id = pg.game_id
where user_id = %s
"""

BALANCE = """select balance from "user" where id =%s"""

USERS_ID = 'select id from "user"'

USERS_BAL = """
select username, bal, all_bet, win_b, all_bet - win_b - inplay as lose, inplay
from (
         select username,
                bal.balance + win.win as bal,
                case when all_bet is null then 0 else all_bet end
                                      as all_bet,
                case when all_wins.win_bet is null then 0 else all_wins.win_bet end
                                      as win_b,
                case when not_play is null then 0 else not_play end
                                      as inplay

         from (select id, username, balance from "user") bal
                  join (
             select user_id,
                    case
                        when sum(game_result) is null then 0
                        else sum(game_result) end -
                    case
                        when sum(game_bet) is null then 0
                        else sum(game_bet)
                        end as win
             from play p
                      join play_game pg
                           on p.id = pg.game_id
             group by user_id
         ) win on bal.id = win.user_id
                  join (select user_id, count(*) as all_bet
                        from play p
                                 join play_game pg on p.id = pg.game_id
                        group by user_id) all_bet on all_bet.user_id = win.user_id
                  left join (select user_id, count(*) as win_bet
                             from play p
                                      join play_game pg on p.id = pg.game_id
                             where game_result > 0
                             group by user_id) all_wins
                            on all_wins.user_id = all_bet.user_id
                  left join (select user_id, count(*) as not_play
                             from play p
                                      join play_game pg on p.id = pg.game_id
                             where game_result isnull
                             group by user_id) play on play.user_id = all_bet.user_id
     ) tbl;
"""
