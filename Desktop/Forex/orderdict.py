from collections import OrderedDict
import numpy
import itertools
import pandas as pd

#import test

import time

def Trendline(meanlist,difflist,mean=0):
        if mean!=0:
            mean=mean
        else:
            mean=meanlist[-1]
        k = numpy.std(difflist)

        print(difflist,"difflist aksodjsak;djksal;jdksajdk;sajdk;asdjsakld;")
        SDhigh=mean+(1*k)
        SDlow=mean-(1*k)
        print(SDhigh,"up")
        print(SDlow,"low")
        return SDhigh,SDlow,k

class checker():
    def __init__(self,a,b,closelist):
        self.meanlist=[]
        self.lowlist=[]
        self.highlist=[]
        self.Trend=[]
        self.bars=[]
        self.difflist=[]
        self.highseries=[]
        self.lowseries=[]
        self.k=0
        self.oldk=0
        self.lastsdhigh=0
        self.lastsdlow=100
        self.listA=a
        self.listB=b
        self.oldhigh = a[0]
        self.lastk=0
        self.oldlow = b[0]

        self.close=closelist

    def check(self):
        s=time.time()
        self.updiff=[]
        self.downdiff=[]
        self.difflist=[]
        print(s,"s first time kuyyyyyyyyy")
        bars=0
        for i,j,k2 in zip(self.listA,self.listB,self.close):

            mean=(i+j)/2
            diff=i-j


            print(self.oldk,"oldddd kkk with ",i,j)
            print(self.oldhigh, "up")
            print(self.oldlow, "down")
            print(self.lastsdlow,"sss and",self.lastsdhigh)
            c=False

            if (i > self.oldhigh and j < self.oldlow) or (i == self.oldhigh and j == self.oldlow):  # กรณีเท่ากัน และ i>oldhihj but j<oldlow
                print("1as")
             #   if self.oldk=="up":
                  #  self.updiff.append(diff)
              #  elif self.oldk=="down":
                   # self.downdiff.append(diff)
                c=True


            elif i > self.oldhigh or (j> self.oldlow and self.oldk=="down"):
                print("2ad")
                self.k="up"

               # self.updiff.append(diff)

                c=True

            elif j<self.oldlow or (i<self.oldhigh and self.oldk=="up") :
                print("3ds")
                self.k="down"
                #self.downdiff.append(diff)

                c=True

            if self.k==self.oldk or self.oldk==0:
                diff = i - j
                if self.oldk=="down":
                    self.downdiff.append(diff)
                elif self.oldk=="up":
                    self.updiff.append(diff)
                self.meanlist.append(mean)


            elif self.k!=self.oldk:

                print(self.k,"adsdsadas")
                if self.oldk=="up":
                    diff1=i-j
                    diff2=(self.oldhigh-k2)
                    maxdiff=[diff1,diff2]
                    diff=max(maxdiff)
                    self.sdhigh, self.sdlow, k = Trendline(self.meanlist, self.updiff)
                    print(self.lastk,"last kkk")
                    print(self.lastsdhigh + 0.2 * self.lastk)
                    print(k,"this is k")

                    if  j>self.sdlow or (len(self.lowseries)>0 and  self.oldhigh<self.lastsdhigh+0.3*self.lastk and j>self.lowseries[-1]):
                        print("dsakldsakd;lkasl;dsa")
                        self.updiff.append(diff)
                        #(self.sdlow<self.lastsdhigh and self.sdlow>self.lastsdlow)  :
                        self.k="up"

                    elif j <self.sdlow   :

                        self.highseries.append(max(self.highlist))
                        self.highlist = []
                        self.meanlist = [self.meanlist[-1], mean]
                        self.updiff = []
                        self.downdiff.append(diff)
                        self.lastsdhigh = self.sdhigh
                        self.lastsdlow = self.sdlow
                        self.Trend.append("up")
                        self.lastk=k

                if self.oldk == "down" :
                    diff1 = i - j
                    diff2 = (k2-self.oldlow)
                    maxdiff = [diff1, diff2]
                    diff = max(maxdiff)
                    self.sdhigh, self.sdlow, k = Trendline(self.meanlist, self.downdiff)
                    print(k, "this is k")
                    if (len(self.highseries)>0 and j>self.lastsdlow and i<self.highseries[-1]):
                        print("dasdas")
                    if  i<self.sdhigh or (len(self.highseries)>0 and self.oldlow>self.lastsdlow-0.3*self.lastk and i<self.highseries[-1]) :
                        print(self.lastk,"sadlas;das;dksa;'dkl;sakd;lsa")
                        print(self.sdhigh,"dasdsa")
                        print("downnnnn")
                        self.k="down"
                        self.downdiff.append(diff)


                    elif i > self.sdhigh :

                        self.lowseries.append(min(self.lowlist))
                        self.lowlist = []
                        self.meanlist=[self.meanlist[-1],mean]
                        self.downdiff=[]
                        self.updiff.append(diff)
                        self.lastsdhigh = self.sdhigh
                        self.lastsdlow=self.sdlow
                        self.lastk=k
                        self.Trend.append("down")

            print(self.lowlist,"and",self.highlist)
            print(self.lastk,"last k")
            self.oldk=self.k
            print(self.highseries,"highseries")
            print(self.lowseries,"lowseries")

            if self.oldk=="down":
                self.difflist=self.downdiff
                self.lowlist.append(j)
            elif self.oldk=="up":
                self.difflist=self.updiff
                self.highlist.append(i)



            if c:
                self.oldlow=j
                self.oldhigh=i
            bars=bars+1

        l=time.time()
        print(l)
        print(l-s,"diff time")

    def tickcheck(self):

        k = numpy.std(self.difflist)

        sdhigh=self.meanlist[-1]+(1*k)
        sdlow=self.meanlist[-1]-(1*k)
        Trend=self.oldk
        print(self.oldk,"oldk")



        return sdlow, sdhigh, Trend

'''''
        if self.oldk=="up" and high<self.oldhigh:
            SDhigh, SDlow, k=Trendline(self.meanlist,self.difflist)
            if low > self.sdlow or (high < self.lastsdhigh + 0.15 * k and low > self.lastsdlow):
                Trend="up"
            elif low < self.sdlow:
                Trend="down"

        elif self.oldk=="down" and low>self.oldlow:
            SDhigh, SDlow, k = Trendline(self.meanlist, self.difflist)
            if high < self.sdhigh or (low > self.lastsdlow - 0.15 * k and high < self.lastsdhigh):
                Trend="down"
            elif high > self.sdhigh:
                Trend="up"
'''





            #เปลี่ยน mean เป้น bar ให้หมด
            #if len(self.series)!=0:
            #    if max(self.meanlist)<max(self.series[-1]) and min(self.meanlist)>min(self.series[-1]) and j<min(self.series[-1]):




if __name__ == '__main__':
    df = pd.read_csv(
        '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/EURUSDmDataHour.csv')
    Datahigh = df["HIGH"].iloc[136:185].tolist()
    Datalow=df["LOW"].iloc[136:185].tolist()
    ATR=df["ATR"].iloc[62:96].tolist()
    Datahigh=[1419.504,1419.755,1419.821,1420.186,1420.765,1421.021,1421.309,1420.961,1421.390,1421.392,1421.158,1420.483,1420.642,1421.332,1420.986,1420.728]
    Datalow=[1418.661,1419.046,1419.359,1419.461,1420.006,1420.605,1420.678,1420.527,1420.706,1420.691,1420.366,1419.958,1420.234,1420.476,1420.473,1420.244]
    #print(ATR,"ATR")
    #Time=df["TIME"].iloc[54:64].tolist()
    #print(Time,"time")
    #a = (1.11427, 1.11792, 1.11737, 1.12613, 1.12768, 1.13038, 1.12800, 1.13000)
    #b = (1.11158, 1.11243, 1.11597, 1.11593, 1.12262, 1.12187, 0.5, 0.4)
    # e=[1.27411,1.27284,1.27285]
    #d=[1.27164,1.26918,1.26982]
    intradayhigh=[1.130000,1.12500,1.13100]
    intradaylow=[0.8,1.0000,1.1]

    c=checker(Datahigh,Datalow)

    #c.check(a,b)
    #c.check(intradayhigh,intradaylow)
    v=1330.0
    r=1324.00
    c.check()



    q,w,e=c.tickcheck()
    print(e,"askdlas;jkdl;sakd;lsa")
    print(c.meanlist,"lastlist")
    print(c.difflist,"last diff list")
    highlist=[]
    lowlist=[]


    print(c.lowseries,"low series")
    print(c.highseries,"high series")
    print(c.oldk,"oldk")
    print(c.oldhigh,"and ",c.oldlow)
    print(c.lastsdlow,"sdlow")
    print(c.lastsdhigh,"sdhigh")








#เหลือ ทำ series ของ wave
