import re

CNT_REGEX = 25


def gen_regexs():
    sw = {}
    sl = {}

    for i in range(1, CNT_REGEX):
        sw[str(i)] = re.compile(r'[^|0]1{d:}[0|$]'.format(d=i))
        sl[str(i)] = re.compile(r'[^|0]0{d:}[0|$]'.format(d=i))
    return sw, sl


SW, SL = gen_regexs()
