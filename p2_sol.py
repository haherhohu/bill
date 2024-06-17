#/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter

def input_provider(filename):
    return open(filename, 'r').readlines()

def read(line):
    try:
        s, e = map(int, line.split(' '))
        return (s,e)
    except ValueError:
        return (0,0)

def reads(lines):
    n, m = read(lines[0])
    chars = lines[1]

    se = []
    for i in range(2, 2+m):
        se.append(read(lines[i]))
    return n, chars, se

def validate(n, chars, se):
    if (n > 100000):
        n = 100000
    if("".join(sorted(chars)) != chars):
        chars = "".join(sorted(chars))
    if(len(se) > 200000):
        se = se[:200000]
    
    validse = [ e for e in se if e[0] < e[1]]

    return n, chars, validse

def cal_freq_char(n, chars, validse):
    targets = [chars[e[0]:e[1]] for e in validse]
    freqs = [Counter(e).most_common()[0][0] for e in targets]

    return freqs

if __name__ == '__main__':
    lines = input_provider('p2_input.txt')
    n, chars, se = reads(lines)
    n, chars, validse = validate(n, chars, se)
    freqs = cal_freq_char(n, chars, validse)
    [print(e) for e in freqs]