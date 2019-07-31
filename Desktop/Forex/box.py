import numpy
import pandas as pd
from orderdict import checker
highseries=[1422.590,1422.469,1422.452]
lowseries=[1422.291,1421.718,1421.998]
n=numpy.std(highseries)

#append old 80 bars and append new one remove old one
def pricebox(highseriesM5,lowseriesM5,wide,Lasthigh,Lastlow):
    conLow=[]
    conLow2=[]

    conHigh=[]
    conHigh2=[]
    highpricebrake=[]
    lowpricebrake=[]

    for i in range(len(highseriesM5)):
        conHigh=[]

        for j in range(len(highseriesM5)):


            if abs(highseriesM5[j]-highseriesM5[i])<=wide:
               # print(abs(highseriesM5[j]-highseriesM5[i]),"kuy first")
                #print(highseriesM5[j], "and", highseriesM5[i])
                conHigh.append(highseriesM5[j])
                conHigh=list(set(conHigh))
             #   print(highseriesM5[j],"and",highseriesM5[i])
              #  print(abs(highseriesM5[j]-highseriesM5[i]),"first")
        if len(conHigh)>=3:
            print(conHigh)
    print("dasjdkjaskdl;jasl;djsakljdlkshfakslfhjkdshfjkldshafjkdshfjdshjfk jipjijpijipjpijiojiohjiou")
    for i in range(len(lowseriesM5)):
        conLow=[]
        for j in range(len(lowseriesM5)):
            #print(abs(lowseriesM5[j] - lowseriesM5[i]), "second")
            #print(lowseriesM5[j], "and", lowseriesM5[i])
            if abs(lowseriesM5[j] - lowseriesM5[i]) <= wide:
                conLow.append(lowseriesM5[j])
        if len(conLow)>=3:
            print(conLow)


    return min(conLow),max(conHigh)
'''''
    df=pd.DataFrame(conLow2,columns=["LowbrakeM5"])
    df2=pd.DataFrame(conHigh2,columns=["HighbrakeM5"])
    df.to_csv('/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/LowbrakeM5.csv')
    df.to_csv(
        '/Applications/MT4.app/Contents/Resources/drive_c/Program Files (x86)/MetaTrader - EXNESS/MQL4/Files/HighbrakeM5.csv')
    #return conHigh2,conLow2


#pricebox(highseries,lowseries,0.300)

print(a,"conhigh return")
print(b,"conLow return")
'''