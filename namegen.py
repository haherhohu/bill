import random

# AC00–D7A3 Hangul Syllables in unicode
# 44032~55203 (integer)

# B0A1~B0FE
# B1A1~B1FE 
# ...
# C8A1~C8FE Hangul Syllables in EUC-KR

n_names = 10
def gen_unicode_name(n_names):
    result = []
    for i in range(n_names):
        # 이름의 길이
        size = random.randint(3, 20)
        # 이름에 사용될 글자 랜덤 생성
        intarr = random.sample(range(44032,55203), size) # 0xAC00 ~ 0xD7A3
        # 값을 utf-16으로 변환
        bytes = [e.to_bytes(3,'little') for e in intarr ]
        decoded = [e.decode(encoding='utf-16', errors=u'ignore') for e in bytes]
        # 이름 추가
        result.append(''.join(decoded))
    return "\n".join(result)

def gen_euckr_name(n_names):
    # 완성형 준비작업
    ksx1001 = zip(range(0xB0A1, 0xC8A1, 0x0100), range(0xB0FE, 0xC8FE, 0x0100))
    # 완성형 한글 타겟 설정
    targets = [e for r in [range(s,e) for s, e in ksx1001] for e in r]

    # 한줄로
    return "\n".join([''.join([e.decode(encoding='euc-kr', errors=u'ignore') for e in 
                       [e.to_bytes(2,'big') for e in random.sample(targets, random.randint(3, 20))]
                       ]) for i in range(n_names)])


if __name__ == '__main__':
    print(gen_unicode_name(n_names))
    print("")
    print(gen_euckr_name(n_names))