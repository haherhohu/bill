#/usr/bin/env python3
# -*- coding: utf-8 -*-

def input_provider(filename):
    return open(filename, 'r').readlines()

def readi(line):
    try: 
        n, m = map(int, line.split(' '))
        return (n,m)
    except ValueError:
        return (0,0)

def readc(line):
    try:
        i, u = line.strip().split(' ')
        return (i,u)
    except ValueError:
        return (' ',' ')

def reads(lines):
    _, m = readi(lines[0])
    peoples = lines[1].strip()

    iu = []
    for i in range(2, 2+m):
        iu.append(readc(lines[i]))
    return peoples, iu

def validate(peoples, iu):
    if(len(iu) > 5000):
        iu = iu[:5000]
    peoples = [e for e in peoples if e.isalpha()]


def make_frends_map(peoples, iu):
    friends = dict([(e,set()) for e in peoples], )
    for i, u in iu:
        friends[i].add(u)
        friends[u].add(i)

    return friends

# friends recommend method only social network
def recommend_friend(friends):
    intersection = []

    for i in friends:
        for u in friends:
            if i != u:
                intersection.append((i, u, len(friends[i] & friends[u])))

    # 솎아내기, e[1] 과 e[0] 는 친구가 아니어야 함.
    intersection = [e for e in intersection if e[1] not in friends[e[0]]]
    print(intersection)
    
    # most know mutual friends
    recommend = sorted(intersection, key=lambda x: x[2], reverse=True)[0]
    return recommend

if __name__ == "__main__":
    lines = input_provider('p3_input.txt')
    peoples, iu = reads(lines)
    validate(peoples, iu)
    friends = make_frends_map(peoples, iu)
    recommend = recommend_friend(friends)

    print (recommend[0], recommend[1])
    print (recommend[2])
    
