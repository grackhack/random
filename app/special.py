"""Вычисляемые события"""
from app.types import DigitRaw


def get_k15(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        if a5 == a10 == a15 == a20 == '0':
            raw += '1'
        else:
            raw += '0'
    return raw


def get_nr(de: DigitRaw) -> str:
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(*de.values()):
        if (a0 == a1 == '1') or (a1 == a2 == '1') or (a2 == a3 == '1') or (a3 == a4 == '1') or (
                a4 == a5 == '1') or (a5 == a6 == '1') or (a6 == a7 == '1') or (a7 == a8 == '1') or (
                a8 == a9 == '1'):
            raw += '1'
        else:
            raw += '0'
    return raw


def get_all_even(de: DigitRaw) -> str:
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, s in zip(*de.values()):
        if a1 == a3 == a5 == a7 == a9 == '0':
            raw += '1'
        else:
            raw += '0'
    return raw


def get_all_odd(de: DigitRaw) -> str:
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, s in zip(*de.values()):
        if a0 == a2 == a4 == a6 == a8 == '0':
            raw += '1'
        else:
            raw += '0'
    return raw


def get_eq(de: DigitRaw) -> str:
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(*de.values()):
        if [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9].count('1') <= 2:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_even13(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26 in zip(
            *de.values()):
        if (a1 == a3 == a5 == a7 == a9 == a11 == a13 == a15 == a17 == a19 == a21 == a23 == a25 == '0'):
            raw += '1'
        else:
            raw += '0'
    return raw


def get_odd13(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26 in zip(
            *de.values()):
        if (a2 == a4 == a6 == a8 == a10 == a12 == a14 == a16 == a18 == a20 == a22 == a24 == a26 == '0'):
            raw += '1'
        else:
            raw += '0'
    return raw


def get_even_more_odd(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        if (sum([int(a2), int(a4), int(a6), int(a8), int(a10), int(a12), int(a14), int(a16), int(a18), int(a20),
                 int(a22), int(a24)]) >

                sum([int(a1), int(a3), int(a5), int(a7), int(a9), int(a11), int(a13), int(a15), int(a17), int(a19),
                     int(a21), int(a23)])):
            raw += '1'
        else:
            raw += '0'
    return raw


def get_min_even(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14])
        pos = tmp.find('1')
        if pos % 2 == 0:
            raw += '0'
        else:
            raw += '1'
    return raw


def get_min_p_even(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17])
        pos = tmp.find('1')
        if pos % 2 == 0:
            raw += '0'
        else:
            raw += '1'
    return raw


def get_max_odd(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        tmp = ''.join([a24, a23, a22, a21, a20, a19, a18, a17, a16, a15, a14, a13, a12, a11])
        pos = tmp.find('1')
        if pos % 2 == 0:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_max_p_odd(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a20, a19, a18, a17, a16, a15, a14, a13, a12, a11, a10, a9, a8, a7])
        pos = tmp.find('1')
        if pos % 2 == 0:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_152(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        tmp = sum([int(a1) * 1, int(a2) * 2, int(a3) * 3, int(a4) * 4, int(a5) * 5, int(a6) * 6,
                   int(a7) * 7, int(a8) * 8, int(a9) * 9, int(a10) * 10, int(a11) * 11, int(a12) * 12,
                   int(a13) * 13, int(a14) * 14, int(a15) * 15, int(a16) * 16, int(a17) * 17, int(a18) * 18,
                   int(a19) * 19, int(a20) * 20, int(a21) * 21, int(a22) * 22, int(a23) * 23, int(a24) * 24])
        if tmp > 152.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_150(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        tmp = sum([int(a1) * 1, int(a2) * 2, int(a3) * 3, int(a4) * 4, int(a5) * 5, int(a6) * 6,
                   int(a7) * 7, int(a8) * 8, int(a9) * 9, int(a10) * 10, int(a11) * 11, int(a12) * 12,
                   int(a13) * 13, int(a14) * 14, int(a15) * 15, int(a16) * 16, int(a17) * 17, int(a18) * 18,
                   int(a19) * 19, int(a20) * 20, int(a21) * 21, int(a22) * 22, int(a23) * 23, int(a24) * 24])
        if tmp > 150.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_148(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
            *de.values()):
        tmp = sum([int(a1) * 1, int(a2) * 2, int(a3) * 3, int(a4) * 4, int(a5) * 5, int(a6) * 6,
                   int(a7) * 7, int(a8) * 8, int(a9) * 9, int(a10) * 10, int(a11) * 11, int(a12) * 12,
                   int(a13) * 13, int(a14) * 14, int(a15) * 15, int(a16) * 16, int(a17) * 17, int(a18) * 18,
                   int(a19) * 19, int(a20) * 20, int(a21) * 21, int(a22) * 22, int(a23) * 23, int(a24) * 24])
        if tmp > 148.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_84(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = sum([int(a1) * 1, int(a2) * 2, int(a3) * 3, int(a4) * 4, int(a5) * 5, int(a6) * 6,
                   int(a7) * 7, int(a8) * 8, int(a9) * 9, int(a10) * 10, int(a11) * 11, int(a12) * 12,
                   int(a13) * 13, int(a14) * 14, int(a15) * 15, int(a16) * 16, int(a17) * 17, int(a18) * 18,
                   int(a19) * 19, int(a20) * 20])
        if tmp > 84.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_88(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = sum([int(a1) * 1, int(a2) * 2, int(a3) * 3, int(a4) * 4, int(a5) * 5, int(a6) * 6,
                   int(a7) * 7, int(a8) * 8, int(a9) * 9, int(a10) * 10, int(a11) * 11, int(a12) * 12,
                   int(a13) * 13, int(a14) * 14, int(a15) * 15, int(a16) * 16, int(a17) * 17, int(a18) * 18,
                   int(a19) * 19, int(a20) * 20])
        if tmp > 88.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_min_25(de: DigitRaw) -> str:
    """Наименьший выпавший номер Больше 2.5"""
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(*de.values()):
        tmp = ''.join([a0, a1, a2, a3, a4, a5, a6, a7, a8, a9])
        pos = tmp.find('1')
        if pos > 2.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_min_75(de: DigitRaw) -> str:
    """Наибольший выпавший номер Больше 7.5"""
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(*de.values()):
        tmp = ''.join([a0, a1, a2, a3, a4, a5, a6, a7, a8, a9])
        pos = tmp[::-1].find('1')
        if pos > 1.5:
            raw += '0'
        else:
            raw += '1'
    return raw


def get_min_15(de: DigitRaw) -> str:
    """Наименьший выпавший номер Больше 1.5"""
    raw = ''
    for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(*de.values()):
        tmp = ''.join([a0, a1, a2, a3, a4, a5, a6, a7, a8, a9])
        pos = tmp.find('1')
        if pos > 1.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_min_p_15(de: DigitRaw) -> str:
    """Наименьший выпавший номер Больше 1.5"""
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20])
        pos = tmp.find('1')
        if pos > 0.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_max_p_18(de: DigitRaw) -> str:
    """Наибольший выпавший номер Больше 1.5"""
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20][::-1])
        pos = tmp.find('1')
        if pos > 1.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_max_p_19(de: DigitRaw) -> str:
    """Наибольший выпавший номер Больше 1.5"""
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20][::-1])
        pos = tmp.find('1')
        if pos > 0.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_min_p_25(de: DigitRaw) -> str:
    """Наименьший выпавший номер Больше 2.5"""
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20 in zip(
            *de.values()):
        tmp = ''.join([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20])
        pos = tmp.find('1')
        if pos > 1.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_14(de: DigitRaw) -> str:
    """Сумма всех выпавших номеров Больше 14.5"""
    raw = ''
    for s in de:
        sum = s if s is not None else 0
        if sum > 14.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_sum_12(de: DigitRaw) -> str:
    """Сумма всех выпавших номеров Больше 12.5"""
    raw = ''
    for s in de:
        sum = s if s is not None else 0
        if sum > 12.5:
            raw += '1'
        else:
            raw += '0'
    return raw


def get_duel_nr(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26 in zip(
            *de.values()):
        if (a1 == a2 == '1') or (a2 == a3 == '1') or (a3 == a4 == '1') or (a4 == a5 == '1') or (a5 == a6 == '1') or (
                a6 == a7 == '1') or (a7 == a8 == '1') or (a8 == a9 == '1') or (a9 == a10 == '1') or (
                a10 == a11 == '1') or (a11 == a12 == '1') or (a12 == a13 == '1') or (a13 == a14 == '1') or (
                a14 == a15 == '1') or (a15 == a16 == '1') or (a16 == a17 == '1') or (a17 == a18 == '1') or (
                a18 == a19 == '1') or (a19 == a20 == '1') or (a20 == a21 == '1') or (a21 == a22 == '1') or (
                a22 == a23 == '1') or (a23 == a24 == '1') or (a24 == a25 == '1') or (a25 == a26 == '1'):
            raw += '1'
        else:
            raw += '0'
    return raw


def get_duel_eb(de: DigitRaw) -> str:
    raw = ''
    for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26 in zip(
            *de.values()):
        if (sum([int(a2), int(a4), int(a6), int(a8), int(a10), int(a12), int(a14), int(a16), int(a18), int(a20),
                 int(a22), int(a24), int(a26)]) >

                sum([int(a1), int(a3), int(a5), int(a7), int(a9), int(a11), int(a13), int(a15), int(a17), int(a19),
                     int(a21), int(a23), int(a25)])):
            raw += '1'
        else:
            raw += '0'
    return raw


def empty(de: DigitRaw) -> str:
    return '1' * len(de['1'])
