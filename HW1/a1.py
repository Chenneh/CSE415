# CSE 415 HW_1_PART_A
# Chen Bai 1560405
# Jan 14 2019

import math


def five_x_cubed_plus_1(x):
    return int(5 * math.pow(x, 3) + 1)


def pair_off(l):
    length = len(l)
    list_re = []
    for i in range(0, length, 2):
        if i == length - 1:
            list_re.append([l[i]])
        else:
            pair = [l[i], l[i + 1]]
            list_re.append(pair)
    return list_re


def mystery_code(s):
    s_re = ""
    for c in s:
        num = ord(c)
        c_new = c
        if 97 <= num <= 103:
            c_new = chr(num - 13)
        elif 104 <= num <= 122:
            c_new = chr(num - 39)
        elif 65 <= num <= 71:
            c_new = chr(num + 51)
        elif 72 <= num <= 90:
            c_new = chr(num + 25)
        s_re += c_new
    return s_re


def past_tense(l):
    list_re = []
    special_map = {"have": "had", "be": "was", "am": "was", "is": "was", "are": "were", "eat": "ate", "go": "went"}
    for w in l:
        if w in special_map:  # special cases
            w_new = special_map[w]
        else:  # non-special cases
            end = w[-1]
            if end == "e":
                w_new = w + "d"
            elif end == "y" and w[-2] not in "aeiou":
                w_new = w[:-1] + "ied"
            elif w[-2] in "aeiou" and w[-3] not in "aeiou" and end not in "aeiou" and end not in "yw":
                w_new = w + end + "ed"
            else:
                w_new = w + "ed"
        list_re.append(w_new)
    return list_re












