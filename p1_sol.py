#/usr/bin/env python3
# -*- coding: utf-8 -*-

def input_provider(filename):
    return open(filename, 'r').readlines()

def read(line):
    try:
        p, q = map(int, line.split(' '))
        return (p,q)
    except ValueError:
        return (0,0)

def reads(lines):
    n, m = read(lines[0])
    votes = []
    for i in range(1, m):
        votes.append(read(lines[i]))

    return n, votes

def validate(n, votes):
    validvotes = []
    for vote in votes:
        if vote[0] > 0 and vote[0] <= n and vote[1] > 0 and vote[1] <= n and vote[0] != vote[1]:
            validvotes.append(vote)
        else:
            validvotes.append((0,0))
    return n, validvotes

def cal_points(n, votes):
    points = [0 for i in range(n+1)]
    for vote in votes:
        if(vote[0] != 0):
            points[vote[0]] += 5
        if(vote[1] != 0):
            points[vote[1]] += 3
    points = [(i, p) for i, p in enumerate(points)][1:]
    return points

def sort_points(points):
    return sorted(points, key=lambda x: x[1], reverse=True)

def set_rank(points):
    rank = 1
    skip = 0
    ranks = []
    ranks.append((rank, points[0][0], points[0][1]))
    for i,p in enumerate(points[1:]):
        # 앞과 비교
        if p[1] == ranks[i][1]:
            ranks.append((*p, rank))
            skip = skip + 1
        else:
            # skip 된 항목이 없음
            skip = 1 if skip == 0 else skip
            ranks.append((*p, rank+skip))
            rank = rank+skip
            skip = 0

    return ranks

if __name__ == '__main__':
    lines = input_provider('p1_input.txt')
    [print(*e) for e in set_rank(sort_points(cal_points(*validate(*reads(lines)))))]