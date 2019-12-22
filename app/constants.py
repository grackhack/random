import re

CNT_REGEX = 25
XRNG = 1000
XTICK = 10
MIN_SERIES = 6
TBL_COL = 85
KOEF = 1.92


def gen_regexs():
    sw = {}
    sl = {}

    for i in range(1, CNT_REGEX):
        sw[str(i)] = r'(1)0{{{d:}}}(?:$|1)'.format(d=i)
        sl[str(i)] = r'(0)1{{{d:}}}(?:$|0)'.format(d=i)

    return sw, sl


SW, SL = gen_regexs()

PL_GAMES = """
select  p.id,game_time, game_digit, game_win , game_bet, game_result from play p
join play_game pg on p.id = pg.game_id where user_id=%s and p.game_result isnull
"""

PL_GAME_RES = 'select de{de:} from game where date> %s order by date limit 1'

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