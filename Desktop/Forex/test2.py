lowlist3={}

lowlist1=[1320]


lowlist2=[1310.0475000000001]

#lowlist=list(reversed(lowlist))

highlist1=[1330]
highlist2=[1340]

#print(highlist)
tickclose=0.08
#for low
#low=min(lowlist, key=lambda y: tickclose<y )#and  abs(y - tickclose) )
#high=min(highlist, key=lambda y: tickclose<y)# and abs(y - tickclose) )


retracements = [23.6,38.2,50.00,61.8,88.6,100]
extensions = [127.2,138.2,150.00,161.8,176.4,261.8,423.6]
fibonacci=[23.6,38.2,50.00,61.8,88.6,100,138.2,150.00,161.8,176.4,261.8,300,400,423.6]

def uptrend(high,low):
    diff = high - low
    pricearray=[]
    print('\n\t\tUPTREND\t\n')
    print('Retracements\t\tExtensions\n')
    for r in fibonacci:
        print(r, ' = ', round((high - (diff * r / 100)), 3))
        pricearray.append(round((high - (diff * r / 100)), 3))

    return pricearray


def downtrend(high,low):
    diff = high - low
    pricearray=[]
    print('\n\t\tDOWNTREND\t\n')
    print('Retracements\t\tExtensions\n')
    for r in fibonacci:
        print(r, ' = ', round((low + (diff * r / 100)), 3))
        pricearray.append(round((low + (diff * r / 100)), 3))

    return pricearray

k=0
Trend="up"
#for low tp
def Takeprofit(Trend,lowlisthour,highlisthour,lowlistday,highlistday,tickclose,oldlow,oldhigh):

    lowlisthour = list(reversed(sorted(lowlisthour)))


    highlisthour=list(sorted(highlisthour))




    if Trend=="down":
        lowarray=[]
        if tickclose>min(lowlisthour) :
            for i in lowlisthour:
                if tickclose>i:
                    lowarray.append(i)

        low2 = None
        k2=lowlistday[-1]
        if tickclose<=min(lowlisthour):
            while (low2==None):
                j = -1
                print(k2,"k2")
                lowpricearray=uptrend(oldhigh,k2)
                lowpricearray=list(reversed(sorted(lowpricearray)))
                print(lowpricearray)

                if tickclose>max(lowpricearray):

                    print("kuyy")
                    break

                if  tickclose<min(lowpricearray):
                    print(min(lowpricearray),"mminnnn")
                    for i in range(len(lowlistday)-2,-1,-1):
                        if lowlistday[i]<k2 and highlistday[j]<oldhigh :
                            k2 =lowlistday[i]

                        j=j-1
                else:
                    low2=max(i for i in lowpricearray if tickclose>i)
                    for j in lowpricearray:
                        if j > tickclose:
                            lowarray.append(j)

        low=max(lowarray,key=lambda y:abs(y-tickclose))
       #if low==low2:
        #    Type="day"
        #else:
         #   Type="hour"
        return lowarray


    elif Trend=="up":
        maxarray = []
        if tickclose<max(highlisthour):
           for j in highlisthour:
               if tickclose < j:
                   maxarray.append(j)



        k1=highlistday[-1]
        high2 = None
        if tickclose >= max(lowlisthour):
            while(high2==None):
                k=-1
                print(k1,"k1")
                highpricearray=downtrend(k1,oldlow)
                highpricearray= list(sorted(highpricearray))
                print(highpricearray)

                if tickclose < min(highpricearray):
                    print("kuyy")
                    break

                if tickclose > max(highpricearray):
                    print(min(highpricearray), "mminnnn")
                    for i in range(len(highlistday) - 2, -1, -1):
                        if highlistday[i] > k1 and lowlistday[k] > oldlow:
                            k1 = highlistday[i]

                        k = k - 1

                else:
                    high2= min(j for j in highpricearray if j > tickclose)# ติดที่ตรงนี้
                    for j in highpricearray:
                        if j>tickclose:

                            maxarray.append(j)
        #high = min(maxarray, key=lambda y: abs(y - tickclose))
        #if high==high2:
        #    Type="day"
        #else:
         #   Type="hour"
        return maxarray

        #if tickclose>min(pricearray)





'''''


low=Takeprofit("down",lowlist1,highlist1,lowlist2,highlist2,1321.36,1319.857,1327.7035)


print(low,"kuy")
'''