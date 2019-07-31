#from CsvReader import Dataprice,DataATR
#import CsvReader
from orderdict import checker
import Linenotify
import test2
from datetime import datetime as date
import pandas as pd
import os
import numpy



def PricebrakeH1(Pair,diff,highlist,lowlist,lasthigh,lastlow,lastclose): #ประกาศใช้ทุก 1 ชม
    meandiff=numpy.mean(diff)
    Added = (meandiff) * 18 / 100  # (f if f > 0.8 else 0.8)
    highlist2 = list(sorted(highlist["hour"]))
    lowlist2 = list(reversed(sorted(lowlist["hour"])))
    if lastlow>min(lowlist2):
        low=min(lowlist2,key=lambda y:lastlow<y and abs(y-lastlow))
    if lasthigh<max(highlist2):
        high=min(highlist2,key=lambda y:lasthigh>y and abs(y-lasthigh))
        print(highlist2,"sss")

    if lastlow<min(lowlist2):
        array=test2.Takeprofit("down",lowlist["hour"],highlist["hour"],lowlist["day"],highlist["day"],lastclose,lowlist["day"][-1],highlist["day"][-1])
        low=max(array)
    if lasthigh>max(highlist2):
        array=test2.Takeprofit("up",lowlist["hour"],highlist["hour"],lowlist["day"],highlist["day"],lastclose,lowlist["day"][-1],highlist["day"][-1])
        high=min(array)
    Highpricebreak = high
    Downpricebreak = low
    print(high)
    print(low)
    lowTParray = test2.Takeprofit("down", lowlist["hour"], highlist["hour"], lowlist["day"], highlist["day"], Downpricebreak,
                                lowlist["day"][-1], highlist["day"][-1])
    highTParray=test2.Takeprofit("up",lowlist["hour"],highlist["hour"],lowlist["day"],highlist["day"],Highpricebreak,lowlist["day"][-1],highlist["day"][-1])


    print(lowTParray,"low Takeprofit")
    print(highTParray,"high Takeprofit")
    print(Highpricebreak,"up pricebrake")
    print(Downpricebreak,"Down Pricebrake")
    return Highpricebreak,Downpricebreak,lowTParray,highTParray,meandiff
'''''
highlist = {}
lowlist = {}
highlist.setdefault("hour",[])
highlist.setdefault("day",[])
lowlist.setdefault("hour",[])
lowlist.setdefault("day",[])

#dfmin5=pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataM5.csv')

dfhour = pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataHour.csv')
highhour=dfhour["HIGH"].tolist()
lowhour=dfhour["LOW"].tolist()
closelist = dfhour["CLOSE"].tolist()
c = checker(highhour, lowhour)
c.check()
highlist["hour"].extend(c.highseries)
lowlist["hour"].extend(c.lowseries)

dfday = pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataDay.csv')
highday = dfday["HIGH"].tolist()
lowday = dfday["LOW"].tolist()
d = checker(highday, lowday)
d.check()
highlist["day"].extend(d.highseries)
lowlist["day"].extend(d.lowseries)

a,b,c,d,e=PricebrakeH1("XAUUSD",c.difflist,highlist,lowlist,highhour[-1],lowhour[-1],closelist[-1])
npa = numpy.asarray(c)
print(npa)
dfObj3 = pd.DataFrame(
    {'Highpricebrake': [a],
     'Lowpricebrake': [b],
     'Meandiff': [e]
    })

dfObj = pd.DataFrame(c, columns = ['lowTParrayH1'])
dfObj2=pd.DataFrame(d,columns = ['highTParrayH1'])
#ใส่ stoploss ด้วย
dfObj3.to_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/PricebrakeAndMeandiff.csv')
dfObj.to_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/LowTP.csv')
dfObj2.to_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/HighTP.csv')
'''