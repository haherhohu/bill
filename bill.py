#!/opt/anaconda/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import sys
import math


class Bill(object):
    def __init__(self, price=0, date=datetime.date.today(), location="", cancel=False):
        self.price = int(float(price))
        self.date = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M")
        self.location = location
        self.cancel = cancel
        # end of __init__

    def updatePrice(self):
        # value_when_true if condition else value_when_false
        c = "*" if self.cancel else ""
        # update price for canceled
        m = -1 if self.cancel and self.price > 0 else 1
        self.price = self.price * m
        self.location = self.location + c
        return self

    def __str__(self):
        return (str(self.date)[5:].replace("-", "/") + ", " + str(self.price) + ", " + self.location)


def parseSMS(sms):
    try:
        if ("[Web발신]" in sms[0]):
            # 체크카드 출금예정
            if ("출금" in sms[1]):
                sms1 = sms[1].split()
                return Bill(sms1[2].replace(",", "").replace("원", ""),
                            str(datetime.datetime.now().year) + "/" + sms1[3] + " 00:00", sms1[1] + " " + sms1[5])
            # 지연취소(국민)
            elif ("취소완료" in sms[1]):
                sms1 = sms[1].split()
                return Bill(sms1[4].replace(",", "").replace("취소완료(", "").replace("원)", ""),
                            str(datetime.datetime.now().year) + "/" + sms1[3].replace("월", "/").replace("일", "") + " 00:00", sms1[1] + " 취소완료", True)
            # 지연취소(현대)
            elif ("취소처리" in sms[1]):
                sms1 = sms[1].split()
                wonidx = ([i for i, e in enumerate(sms1) if "사용" in e][0] + 1)
                store = "".join(sms1[3:wonidx-1])

                if ("원" in sms1[wonidx]):
                    return Bill(sms1[wonidx].replace(",", "").replace("원", ""),
                                str(datetime.datetime.now().year) + "/" + sms1[2] + " 00:00", store + " 취소완료", True)
                # 철도승차권취소
                else:
                    return Bill(sms1[6].replace(",", "").replace("원", ""),
                                str(datetime.datetime.now().year) +
                                "/" + sms1[2] + " 00:00",
                                sms1[3] + " " + sms1[4] + " 취소완료", True)
            # 외국결제
            elif ("KRW" in sms[4]):
                return Bill(sms[4].replace(",", "").replace("KRW", ""),
                            str(datetime.datetime.now().year) + "/" + sms[3], sms[5], "취소" in sms[1])
            # 후불교통
            elif ("후불교통" in sms[2]):
                return Bill(sms[3].split()[1].replace(",", "").replace("원", ""),
                            str(datetime.datetime.now().year) + "/" + sms[4].replace("결제예정", "00:00"), sms[2])
            # 체크카드
            elif ("체크" in sms[1]):
                return Bill(sms[4].replace(",", "").replace("원", ""),
                            str(datetime.datetime.now().year) + "/" + sms[3], sms[5], len(sms) == 7)

            # 일반결제
            return Bill(sms[3].replace(",", "").replace("원 일시불", ""),
                        str(datetime.datetime.now().year) + "/" + sms[4], sms[5], "취소" in sms[1])
        # else:
    except Exception as ee:
        #print("wrong sms" + sms[0])
        print("debug:" + ",".join(sms))
        return None

        # end of parse SMS


def groupSMS(smslist):
    groups = []
    group = []
    first = True
    for sms in smslist:
        # print(sms)
        sms = sms.rstrip()
        if (first and "[Web발신]" in sms):
            group.append(sms)
            first = False
        elif ("[Web발신]" in sms):
            groups.append(group)
            group = []
            group.append(sms)
        elif ("승인거절" in sms):
            group[0] = group[0] + "*"
            group.append(sms)
        else:
            group.append(sms)
    # last one
    if (len(group) != 0):
        groups.append(group)

    groups = [e for e in groups if not "*" in e[0]]

    # [print(e) for e in groups]

    return groups


if (__name__ == "__main__"):
    with open("in.txt") as f:
        smslist = f.readlines()

    bills = [parseSMS(sms).updatePrice() for sms in groupSMS(smslist)]
    total = sum([bill.price for bill in bills])
    strbills = [str(bill) for bill in bills]
    # print("\n".join(strbills))
    [print(str(bill)) for bill in bills]
    # print(total)
