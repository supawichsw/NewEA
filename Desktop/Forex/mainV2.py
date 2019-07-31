import box
import GivendataMT4
from orderdict import checker
import orderdict
import test2
from datetime import datetime as date
import pandas as pd
import os
import numpy
import box
import time
class Maincsv():
    def __init__(self):
        self.Highpricebreak=0

        self.Downpricebreak=0
        self.lowTParray=[]
        self.highTParray=[]
        self.meandiff=0
        self.lowboxM5=0
        self.highboxM5=0
        self.LastTrend=0
    def mainV2(self,Pair):

        highlist = {}
        lowlist = {}
        highlist.setdefault("hour",[])
        highlist.setdefault("day",[])
        lowlist.setdefault("hour",[])
        lowlist.setdefault("day",[])
        c=True
        while c:
            s=time.time()

            if os.path.exists('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataDay.csv'):

                dfday = pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataDay.csv')
                highday = dfday["HIGH"].tolist()
                lowday = dfday["LOW"].tolist()
                closelist=dfday["CLOSE"].tolist()

                d=checker(highday,lowday,closelist)
                d.check()
                highlist["day"]=[]
                lowlist["day"]=[]
                highlist["day"].extend(d.highseries)
                lowlist["day"].extend(d.lowseries)

                os.remove('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataDay.csv')

            if os.path.exists('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataHour.csv'):

                dfhour = pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/'+Pair+'DataHour.csv')
                highhour = dfhour["HIGH"].tolist()
                lowhour = dfhour["LOW"].tolist()
                closelist = dfhour["CLOSE"].tolist()

                c = checker(highhour, lowhour,closelist)
                c.check()
                sdlowhour,sdhighhour,Trendhour=c.tickcheck()

                highlist["hour"] = []
                lowlist["hour"] = []
                highlist["hour"].extend(c.highseries)
                lowlist["hour"].extend(c.lowseries)
                self.LastTrend=c.Trend[-1]
                self.Highpricebreak, self.Downpricebreak, self.lowTParray, self.highTParray, self.meandiff = GivendataMT4.PricebrakeH1(
                    "XAUUSD", c.difflist, highlist, lowlist, highhour[-1], lowhour[-1], closelist[-1])
                os.remove('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/'+Pair+'DataHour.csv')



            if os.path.exists(
            '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataM5.csv'):
                dfM5=pd.read_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataM5.csv')
                highM5=dfM5["HIGH"].tolist()
                LowM5=dfM5["LOW"].tolist()
                CloseM5=dfM5["CLOSE"].tolist()

                e=checker(highM5,LowM5,CloseM5)
                e.check()
                meandiffM5 = numpy.mean(e.difflist)
                sdlowM5,sdhighM5,TrendM5=e.tickcheck()
                self.lowboxM5, self.highboxM5 = box.pricebox(e.highseries, e.lowseries, 0.300, highM5[-1], LowM5[-1])
                dfObj3 = pd.DataFrame(
                    {'Highpricebrake': [self.Highpricebreak],
                     'Lowpricebrake': [self.Downpricebreak],
                     'Meandiff': [self.meandiff],
                     'sdlowM5': [sdhighM5], 'sdhighM5': [sdhighM5], 'TrendH1': [self.LastTrend],
                     'highbox': [self.highboxM5], 'lowbox': [self.lowboxM5], 'MeandiffM5': [meandiffM5]
                     })
                dfObj = pd.DataFrame(self.lowTParray, columns=['lowTParrayH1'])
                dfObj2 = pd.DataFrame(self.highTParray, columns=['highTParrayH1'])
                dfObj3.to_csv(
                    '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/' + Pair + 'PricebrakeAndMeandiff.csv')
                dfObj.to_csv(
                    '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/' + Pair + 'LowTP.csv')
                dfObj2.to_csv(
                    '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/' + Pair + 'HighTP.csv')

                os.remove('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/XAUUSDmDataM5.csv')

            #self.Highpricebreak, self.Downpricebreak, self.lowTParray, self.highTParray, self.meandiff = GivendataMT4.PricebrakeH1("XAUUSD", c.difflist, highlist, lowlist, highhour[-1], lowhour[-1], closelist[-1])

            #self.lowboxM5,self.highboxM5=box.pricebox(e.highseries,e.lowseries,0.300,highM5[-1],LowM5[-1])

            l=time.time()
            print(l-s,"time")
            #print(self.highTParray,"lasttttt")
            #print(self.Highpricebreak,"la")
            #print(e.highseries,"jjjjjx  ")

m=Maincsv()
m.mainV2("XAUUSDm")
