# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 09:52:00 2019

@author: Daegung Kim
"""
# SRS 데이터 읽어서 필요한 라인만 추출 (1996~2017까지) 후 GOES X-ray와 비교하여 C, M, X 카운트

import numpy as np
from datetime import datetime

# 부모 데이터 클래스.
class SRSSample(object):
    # 기본적인 타임태그와 흑점번호 정보 갖고 있음
    def __init__(self):
        self.timetag = datetime.now
        self.sunspot = 0

    # 비교 연산자 구현
    def __eq__(self, other):
        return (self.timetag == other.timetag and self.sunspot == other.sunspot)

# 자식 1 데이터 클래스
class SRSArchive(SRSSample):
    # 자식새끼가 갖고있는 로케이션과 흑점타입 정보 
    def __init__(self):
        # 부모 데이터 초기화
        SRSSample.__init__(self)
        self.location = ""
        self.spottype = ""

    # str() 연산자 대응
    def __str__(self):
        return self.timetag.strftime("%Y-%m-%d") + " " + str(self.sunspot) + " " + self.spottype + " " + self.location

    # line parsing 
    def fromString(self, line):
        # 스트링 파싱할 때는 이게 좋습니다.
        e = line.split()

        # 예외
        if(len(e) < 8 
            or e[3].upper() == 'NONE' 
            or e[3].upper() == 'CORRECTED'
            or e[3].upper() == '1A.'
            or e[3].upper() == 'II.'):
            return self
        
        # 파싱
        self.sunspot = int(e[3])
        self.timetag = datetime(int(e[0]), int(e[1]), int(e[2]))
        self.location = e[4]
        self.spottype = e[7]

        return self

# 자식 2 데이타 클래스
class XRSReport(SRSSample):
    # 자식새끼가 갖고있는 추가정보
    def __init__(self):
        # 부모 데이터 초기화
        SRSSample.__init__(self)
        self.station = ""
        self.start = 0
        self.peak = 0
        self.end = 0
        self.location = ""
        self.flarelevel = ""
        self.satellite = ""

    # str() 연산자 대응
    def __str__(self):
        return self.timetag.strftime("%Y-%m-%d") + " " + str(self.sunspot) + " " + self.flarelevel + " " + self.location

    # line parsing 
    def fromString(self, line):

        # fill None value for parsing        
        sample = line[28:32]
        sample = sample.replace("    ", "None")
        line = line[0:28] + sample + line[32:]
        sample = line[72:73]
        sample = sample.replace(" ", "_")
        line = line[0:72] + sample + line[73:]
        
        # 스트링 파싱할 때는 이게 좋습니다.
        e = line.split()

        # 예외 
        if(len(e) < 10):
            return self
        
        # 파싱
        self.station = e[0][0:5]
        self.timetag = datetime(int("19" + e[0][5:7]),int(e[0][7:9]), int(e[0][9:11]))
        self.start = int(e[1])
        self.peak = int(e[2])
        self.end = int(e[3])
        self.location = e[4]
        self.flarelevel = e[5]
        self.satellite = e[7]
        self.sunspot = int(e[9])

        return self


# main
# 파일 열기
f_a = open("SRS_archive.txt", 'r')
f_b = open("goes-xrs-reports_1996.txt", 'r')

# 파일 읽기
srs = f_a.readlines()
xrs = f_b.readlines()

# 2-nd list comprehension for good-parsed data
srsas = [e for e in [SRSArchive().fromString(line) for line in srs] if e.sunspot != 0]
xrsrs = [e for e in [XRSReport().fromString(line) for line in xrs] if e.sunspot != 0]

# 각각 출력 샘플
#for srsa in srsas:
#    print(str(srsa))

#for xrsr in xrsrs:
#    print(str(xrsr))

matched = []
# 매칭되는 것만 출력
for srsa in srsas:
    for xrsr in xrsrs:
        # 여기가 상속 __eq__ 포인트
        if(srsa == xrsr):
            matched.append((srsa, xrsr))

# 종류별로 출력
[print(e[0], e[1]) for e in matched if e[1].flarelevel =="C"]
[print(e[0], e[1]) for e in matched if e[1].flarelevel =="M"]
[print(e[0], e[1]) for e in matched if e[1].flarelevel =="X"]