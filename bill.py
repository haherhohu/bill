import datetime
import os
import sys
import math

class Bill():
    def __init__(self, price = 0, date = datetime.date.today(), location = "", cancel=False):
        self.price = int(float(price))
        self.date = datetime.datetime.strptime(date, "%Y/%m/%d %H:%M")
        self.location = location
        self.cancel = cancel
        # end of __init__

    def __str__(self):
        # value_when_true if condition else value_when_false
        c = "*" if self.cancel else ""
        return (str(self.date)[5:].replace("-", "/") + ", " + str(self.price) + ", " + self.location + c)

def parseSMS(sms):
    if("[Web발신]" in sms[0] ):
        if("KRW" in sms[4]):
            return Bill(sms[4].replace(",","").replace("KRW", ""),
                    str(datetime.datetime.now().year) + "/" + sms[3], sms[5], "취소" in sms[1])
        return Bill(sms[3].replace(",","").replace("원 일시불",""),
                    str(datetime.datetime.now().year) + "/" + sms[4], sms[5], "취소" in sms[1])
    else:
        print("wrong sms" + sms[0])
        return None
    # end of parse SMS

def groupSMS(smslist):
    groups = []
    group = []
    first = True
    for sms in smslist:
        sms = sms.rstrip()
        if(first and "[Web발신]" in sms):
            group.append(sms)
            first = False
        elif("[Web발신]" in sms):
            groups.append(group)
            group = []
            group.append(sms)
        else:
            group.append(sms)
    # last one
    if(len(group)!= 0):
        groups.append(group)

    return groups

if( __name__ == "__main__"):
    with open("jan.txt") as f:
        smslist = f.readlines()

    bills = [parseSMS(sms) for sms in groupSMS(smslist)]

    total = sum([bill.price for bill in bills])

    [print(bill) for bill in bills]
    print(total)

    
