import re

CNT_REGEX = 25
XRNG = 1000
XTICK = 10
MIN_SERIES = 6

def gen_regexs():
    sw = {}
    sl = {}

    for i in range(1, CNT_REGEX):
        sw[str(i)] = r'(?:^|1)0{{{d:}}}(?:$|1)'.format(d=i)
        sl[str(i)] = r'(?:^|0)1{{{d:}}}(?:$|0)'.format(d=i)

    return sw, sl


SW, SL = gen_regexs()
