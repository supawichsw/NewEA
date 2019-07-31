//+------------------------------------------------------------------+
//|                                                          kuy.mq4 |
//|                        Copyright 2019, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2019, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
MqlTick last_tick;
string filename;
string token="kWqvDAx6OXTFstbfjPBl2rQXYA6KkMPlk2QBUjpglsP";
datetime day;
extern int lengthday = 500;   // The amount of bars sent to be processed
extern int lengthhour=200;
extern int lengthM5=80;
extern int pricelength=20;
extern int MagicnumberH1=1000;
extern int MagicnumberM5=2000;
extern double diffopen=1.5;
double Price2=0.0;
string BuyOrder;
string SellOrder;
string TrendH1;
MqlRates rates[];
double Added;
double Highbrake;
double Lowbrake;
double ATRday[];
double ATRhour;
double ATRM5[];
double zig[];
static datetime today=-1;
static datetime currentHour=-1;
static datetime M5=-1;
string s[10][1000];
double Htp[1000];
double Ltp[1000];
double Meandiff;
double MeandiffM5;
double Highpricebrake;
double Lowpricebrake;
int LastTotalOrder=0;
double sdhighM5;
double sdlowM5;
double HighbrakeM5;
double LowbrakeM5;
double highTP;
double LowTP;
double oldhighTP;
double oldLowTP;
int OnInit()
 {
//--- indicator buffers mappingp
   string nameData = Symbol()+"_tick.txt";
    static int old_bars = 0;   // remember the amount of bars already known  
   
   
   //Print(old_bars,"Old_bars and",Bars);
                 // remember how many bars are known
   return(0);
 }


//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnTimer()
{
   
}
void OnDeinit(const int reason)
  {
//--- destroy timer
   
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()

  {
//---
     // remember the amount of bars already known
  int Minutes_2delete = 1;

  
  double ATRTick=iATR(Symbol(),PERIOD_H1,14,0);
  ATRhour=iATR(Symbol(),PERIOD_H1,14,1);
  
  if    (today != iTime (Symbol(), PERIOD_D1, 0)){
      today = iTime (Symbol(), PERIOD_D1, 0);      // if a new bar is received 
   
      write_data_Day(); 
      
                                 // write the data file                              
   }      
   if    (currentHour != iTime (Symbol(), PERIOD_H1, 0)){
      currentHour = iTime (Symbol(), PERIOD_H1, 0);      // if a new bar is received 
   
      write_data_Hour(); 
      
                                 // write the data file                              
   } 
   if (M5!=iTime(Symbol(),PERIOD_M5,0)){
      M5=iTime(Symbol(),PERIOD_M5,0);
      write_data_M5();
      
   }
   
   string File3=Symbol()+"PricebrakeAndMeandiff.csv";
   string File2=Symbol()+"LowTP.csv";
   string File1=Symbol()+"HighTP.csv";
   
   if (FileIsExist(File3)){     
      Read1();
      
      Print(FileIsExist(File3),"kuyyyy");
      FileDelete(File3);
      
      
  
   }
   if (FileIsExist(File2)){
      ReadLTP();
      FileDelete(File2);
   }
   if (FileIsExist(File1)){
      
      ReadHTP();
      FileDelete(File1);
   }
   
   Print(Meandiff,"Meandiff");
    Print(Highpricebrake,"hpb");
      Print(Lowpricebrake,"lpb");
      
         Print(sdlowM5,"sdlowM5");
         Print(sdhighM5,"sdhighM5");
         Print(TrendH1,"Trend");
         Print(HighbrakeM5,"HpbM5");
         Print(LowbrakeM5,"LpbM5");
         Print(MeandiffM5,"MeandiffM5");
         for(int x=1;x<ArraySize(Ltp);x++){
            Print(Ltp[x],"Ltp");
         
         }
          for(int x=1;x<ArraySize(Htp);x++){
            Print(Htp[x],"Htp");
         
         }
  
   
   
   LastTotalOrder=OrdersTotal();
   //for open order
   if ((Ask<Lowbrake && ATRTick>ATRhour)||(Ask<oldLowTP && ATRTick>ATRhour)) {
      
      for(int x=0;x<ArraySize(Ltp);x++){
         if (Ask>Ltp[x]){
            double LowTP=Ltp[x];
            break;
         }
         
         
         
      }
      
      
      if (iClose(Symbol(),PERIOD_CURRENT,0)-LowTP>diffopen && OrdersTotal()<2){
         int numorder2=TotalOpenOrder(2);
         if (numorder2<2 && oldLowTP!= LowTP){
            if (numorder2==1){
               
                  OrderSend(Symbol(),OP_SELLLIMIT,0.01,Ask+(Ask-Bid),3,sdhighM5,LowTP,NULL,2,TimeCurrent()+(PERIOD_M1*60)*15);
                  oldLowTP=LowTP;
                  LineNotify("OP_SELLIMIT");
                  }
               else{
                  OrderSend(Symbol(),OP_SELLLIMIT,0.01,Ask+(Ask-Bid),3,sdhighM5,NULL,NULL,2,TimeCurrent()+(PERIOD_M1*60)*15);
                  oldLowTP=LowTP;
                  LineNotify("OP_SELLLIMIT");
               }
      }
   
   } 
   }
  
   else if ((Bid>Highbrake && ATRTick>ATRhour)|| (Bid>oldhighTP && ATRTick>ATRhour)){
   //get the highTP for checking the diff next
   
      for(int x=0;x<ArraySize(Htp);x++){
         if (Bid<Htp[x]){
            double highTP=Htp[x];
            break;
         }
         

      }
      
   
      if (highTP-iClose(Symbol(),PERIOD_CURRENT,0)>diffopen && OrdersTotal()<2){
            int numorder2=TotalOpenOrder(2);
            if (numorder2<2 && oldhighTP!= highTP){
               if (numorder2==1){
               
                  OrderSend(Symbol(),OP_BUYLIMIT,0.01,Bid-(Ask-Bid),3,sdlowM5,highTP,NULL,2,TimeCurrent()+(PERIOD_M1*60)*15);
                  oldhighTP=highTP;
                  LineNotify("OP_BUYLIMIT");
                  }
               else{
                  OrderSend(Symbol(),OP_BUYLIMIT,0.01,Bid-(Ask-Bid),3,sdlowM5,NULL,NULL,2,TimeCurrent()+(PERIOD_M1*60)*15);
                  LineNotify("OP_BUYLIMIT");
                  oldhighTP=highTP;
               }
            
            
            
            
         }
         }
        
      
      }
   if (TrendH1=="up" && Bid>sdhighM5 && ATRTick>ATRhour){
      Price2=sdhighM5;
      BuyOrder=True;
      
   }
    if (TrendH1=="down" && Ask<sdlowM5 && ATRTick>ATRhour){
      Price2=sdlowM5;
      SellOrder=True;
      
   }
   //pricebox for open orders
   if (Bid>HighbrakeM5){
      Price2=HighbrakeM5;
      BuyOrder=True;
      
      
   }
   if (Ask<LowbrakeM5){
      Price2=LowbrakeM5;
      SellOrder=True;
   }
   
   
   if (Price2 != 0.0 && Ask<Price2 && BuyOrder==True ){
      int numorder1=TotalOpenOrder(1);
      if (numorder1<1){
         OrderSend(Symbol(),OP_BUY,0.01,Ask,3,NULL,NULL,NULL,1);
         BuyOrder=False;
         Price2=0.0;
         LineNotify("OP_BUY");
      }
   
   }
   if (Price2 != 0.0 && Bid>Price2 && SellOrder==True){
      int numorder1=TotalOpenOrder(1);
      if (numorder1<1){
         OrderSend(Symbol(),OP_SELL,0.01,Bid,3,NULL,NULL,NULL,1);
         SellOrder=False ;
         Price2=0.0;
         LineNotify("OP_SELL");
   }
   
   }

   
   
    // for close wide diff H1
   if (iHigh(Symbol(),PERIOD_H1,0)-iLow(Symbol(),PERIOD_H1,0)>Meandiff ){
      for(int i=0; i<OrdersTotal();i++){
         
         OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
         
         if (OrderType()==OP_BUY && OrderMagicNumber()==2 && Bid<iHigh(Symbol(),PERIOD_H1,0)-((iHigh(Symbol(),PERIOD_H1,0)-iOpen(Symbol(),PERIOD_H1,0))*0.333)){
           
            OrderClose(OrderTicket(),0.01,Bid,3);
            LineNotify("CLOSE Buy wide diff H1");
            oldhighTP=Highbrake;
            
            //send file back for getting the id
            
         
         }
         else if (OrderType()==OP_SELL && OrderMagicNumber()==2 && Ask>iLow(Symbol(),PERIOD_H1,0)+((iOpen(Symbol(),PERIOD_H1,0)-iLow(Symbol(),PERIOD_H1,0))*0.333)){
            OrderClose(OrderTicket(),0.01,Ask,3);
            LineNotify("CLOSE Sell wide diff H1");
            oldLowTP=Lowbrake;
        
      }
      
      
      }
   
   }
   // for close wide diff M5
   if (iHigh(Symbol(),PERIOD_M5,0)-iLow(Symbol(),PERIOD_M5,0)>MeandiffM5 ){
      for(int i=0; i<OrdersTotal();i++){
         
         OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
         
         if (OrderType()==OP_BUY && OrderMagicNumber()==1 && Bid<iHigh(Symbol(),PERIOD_M5,0)-((iHigh(Symbol(),PERIOD_M5,0)-iOpen(Symbol(),PERIOD_M5,0))*0.333)){
           
            OrderClose(OrderTicket(),0.01,Bid,3);
            LineNotify("CLOSE buy wide diff M5");
            
            
            //send file back for getting the id
            
         
         }
         else if (OrderType()==OP_SELL && OrderMagicNumber()==1 && Ask>iLow(Symbol(),PERIOD_M5,0)+((iOpen(Symbol(),PERIOD_M5,0)-iLow(Symbol(),PERIOD_M5,0))*0.333)){
            OrderClose(OrderTicket(),0.01,Ask,3);
            LineNotify("CLOSE sell wide diff M5");
        
      }
      
      
      }
   
   }
   
   if (OrdersTotal()>0){
       for(int i=0; i<OrdersTotal();i++){
         
         OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
         if (OrderType()==OP_BUY && Bid<sdlowM5){
            OrderClose(OrderTicket(),0.01,Bid,3);
            LineNotify("CLOSE sdlowM5");
            
         
         }
         else if (OrderType()==OP_SELL && Ask>sdhighM5){
            OrderClose(OrderTicket(),0.01,Ask,3);
            LineNotify("CLOSE sdhighM5");
            
         
         }
   }
   } 
   }

   
//---
int TotalOpenOrder(int magic)
 {
      int totalOrdermagic2=0;
      int totalOrdermagic1=0;
      if (OrdersTotal()>0){
      
         for(int i=0; i<OrdersTotal();i++){
         
         OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
         
            if (OrderMagicNumber()==1){
               totalOrdermagic1=totalOrdermagic1+1;
        
        
        
      }
            else if (OrderMagicNumber()==2){
               totalOrdermagic2=totalOrdermagic2+1;
      }
      
      
      }
      
     
}
   if (magic==1){
      return (totalOrdermagic1);
   }
   else{
      return (totalOrdermagic2);
   }
  
}

void write_data_Day()
{
  //ArrayResize(ATRday,lengthday);

  //int copied=CopyRates("ATR",0,0,100,rates);
  int handle=0;
  handle = FileOpen(Symbol()+"DataDay.csv", FILE_CSV|FILE_WRITE,',');
  Print(handle,"dasda");
  if(handle < 1)
  {
    Comment("Creation of  failed. Error #", GetLastError());
   
  }
                    // heading
  FileWrite(handle,"HIGH","LOW","CLOSE","OPEN");   // heading
  
  
  int i;
  
  for (i=lengthday-1; i>=1; i--)
  {
    
    FileWrite(handle,
                      iHigh(Symbol(),PERIOD_D1,i),  iLow(Symbol(),PERIOD_D1,i), iClose(Symbol(),PERIOD_D1,i), iOpen(Symbol(),PERIOD_D1,i));
    
  }
  FileClose(handle);
  Comment("File  has been created. "+TimeToStr(TimeCurrent(), TIME_SECONDS) );
  
  
  }
  void write_data_Hour()
  {
  //ArrayResize(ATRhour,lengthhour);

  //int copied=CopyRates("ATR",0,0,100,rates);
  int handle=0;
  handle = FileOpen(Symbol()+"DataHour.csv", FILE_CSV|FILE_WRITE,',');
  Print(handle,"dasda");
  if(handle < 1)
  {
    Comment("Creation of  failed. Error #", GetLastError());
   
  }
                    // heading
  FileWrite(handle,"TIME,""HIGH","LOW","CLOSE","OPEN","ATR");   // heading
  
  
  int i;
  for (i=lengthhour-1; i>=1; i--)
  {
   // ATRhour[i]=iATR(Symbol(),PERIOD_H1,14,i);
    FileWrite(handle,Time[i],iHigh(Symbol(),PERIOD_H1,i),  iLow(Symbol(),PERIOD_H1,i), iClose(Symbol(),PERIOD_H1,i), iOpen(Symbol(),PERIOD_H1,i));
    
  }
  FileClose(handle);
  Comment("File  has been created. "+TimeToStr(TimeCurrent(), TIME_SECONDS) );
  
  }
  
  void write_data_M5()
  {
  

  //int copied=CopyRates("ATR",0,0,100,rates);
  int handle=0;
  handle = FileOpen(Symbol()+"DataM5.csv", FILE_CSV|FILE_WRITE,',');
  Print(handle,"dasda");
  if(handle < 1)
  {
    Comment("Creation of  failed. Error #", GetLastError());
   
  }
                    // heading
  FileWrite(handle,"TIME,""HIGH","LOW","CLOSE","OPEN");   // heading
  
  
  int i;
  for (i=lengthM5-1; i>=1; i--)
  {
    //ATRM5[i]=iATR(Symbol(),PERIOD_M5,14,i);
    FileWrite(handle,Time[i],iHigh(Symbol(),PERIOD_M5,i),  iLow(Symbol(),PERIOD_M5,i), iClose(Symbol(),PERIOD_M5,i), iOpen(Symbol(),PERIOD_M5,i));
    
  }
  FileClose(handle);
  Comment("File  has been created. "+TimeToStr(TimeCurrent(), TIME_SECONDS) );
  
  }
void Start2()

  {
  string FileName = "LastSignal.csv";
string s[10][1000];
string a1;
string a2;
string a3;
string a4;
  int row=0,col=0;
   int rowCnt,colCnt;
   int handle=FileOpen(FileName,FILE_CSV|FILE_READ,",");
 
   if (FileIsExist(FileName)){
      Print("Existdsadsad kuy");
      int    str_size;
      string str;
      //--- read data from the file
      while(True)
     {
       string temp = FileReadString(handle);
       s[col][row]=temp; 
       if(FileIsEnding(handle)) break;
             
       if(FileIsLineEnding(handle))
       {
       
         colCnt = col;
         col = 0;
         row++;
        
       }
       else
       {
         col++;
       }
      
       rowCnt = row;
       Print(rowCnt,colCnt);
       
     }
     FileClose(handle);
     string lines = "  ";
     for(row=0; row<=rowCnt; row++)
     {
      Print(row,"row");
       for(col=0; col<=colCnt; col++)  
       {
         //lines = lines + " " + s[col][row];
          a1=s[0][row];
          a2=s[1][row];
          a3=s[2][row];
          a4=s[3][row];
         
         Print(col,"col");
       }
       
       
       Print(a1," this is a1 ",a2," this is a2 ",a3," this is a3 ",a4," this is a4 ");
       
       //lines = lines + "\n";
      FileClose(handle);
      FileDelete(FileName);
     }
    
   }
   else
      Print("None");
//---
   
  }
  
 void LineNotify(string Massage){   
 string headers;
 char post[], result[];

headers="Authorization: Bearer "+token+"\r\n";
headers+="Content-Type: application/x-www-form-urlencoded\r\n";
ArrayResize(post,StringToCharArray("message="+Massage,post,0,WHOLE_ARRAY,CP_UTF8)-1);
int res = WebRequest("POST", "https://notify-api.line.me/api/notify", headers, 10000, post, result, headers);
Print("Status code: " , res, ", error: ", GetLastError());
 Print("Server response: ", CharArrayToString(result));
}
void Order(){
  int handle=0;
  string TypeOrder;
   handle = FileOpen("Orders.csv", FILE_CSV|FILE_WRITE,',');
   FileWrite(handle,"Typeorder","Symbol","Takeprofit");
   if (OrdersTotal()>0 ) {
       for(int i=0; i<OrdersTotal();i++){
         
         OrderSelect(i,SELECT_BY_POS,MODE_TRADES);
         
         if (OrderType()==OP_BUY){
           
            TypeOrder="buy";
            
            
            //send file back for getting the id
            
         
         }
         else if (OrderType()==OP_SELL){
            TypeOrder="sell";
        
      }
      FileWrite(handle,TypeOrder,OrderSymbol(),OrderTakeProfit());
      
      }
      FileClose(handle);
     
}
}

void Read1()
  {
//---
   Print(iClose(Symbol(),PERIOD_CURRENT,0));
   int handle=0;
   
   handle = FileOpen(Symbol()+"PricebrakeAndMeandiff.csv", FILE_CSV|FILE_READ,',');
   int row=0,col=0;
   int rowCnt,colCnt;
   Print(handle,"handle");
   
   if(handle>0)
   {
     Print(FileIsExist(Symbol()+"PricebrakeAndMeandiff.csv"),"ssdsadasdsadas");
     while(True)
     {
       Print(row,"and",col);
       string temp = FileReadString(handle);
       s[col][row]=temp;  
       if(FileIsEnding(handle)) break;
   
            
       if(FileIsLineEnding(handle))
       {
         Print("kuyyy");
         colCnt = col;
         col = 0;
         row++;
       }
       else
       {
         col++;
       }
       rowCnt = row;
     }
     Print(colCnt,"hello",rowCnt);
  // FileWrite(handle,Time[i],iHigh(Symbol(),PERIOD_M5,1),  iLow(Symbol(),PERIOD_M5,1), iClose(Symbol(),PERIOD_M5,1), iOpen(Symbol(),PERIOD_M5,1));
    string lines = "  ";

         
         lines = lines + " " + s[col][row];
         
         Highpricebrake=s[1][1];
         Lowpricebrake=s[2][1];
         Meandiff=s[3][1];
         sdlowM5=s[4][1];
         sdhighM5=s[5][1];
         TrendH1=s[6][1];
         HighbrakeM5=s[7][1];
         LowbrakeM5=s[8][1];
         MeandiffM5=s[9][1];
         Added=Meandiff*18/100;
         Highbrake=Highpricebrake+Added;
         Lowbrake=Lowpricebrake-Added;
         oldhighTP=Highbrake;
         oldLowTP=Lowbrake;
         
         
     FileDelete(Symbol()+"PricebrakeAndMeandiff.csv");
     FileClose(handle);
     
    
  }
  
  }
    void ReadHTP(){
   int handle=0;
   handle = FileOpen(Symbol()+"HighTP.csv", FILE_CSV|FILE_READ,',');
   int row=0,col=0;
   int rowCnt,colCnt;
   Print(handle,"handle");
   
   if(handle>0)
   {
     while(True)
     {
       Print(row,"and",col);
       string temp = FileReadString(handle);
       Htp[row]=temp;  
       
   
            
       if(FileIsLineEnding(handle))
       {
         Print("kuyyy");
         colCnt = col;
         col = 0;
         row++;
       }
       else
       {
         col++;
       }
       rowCnt = row;
       if(FileIsEnding(handle)) 
       break;
     }
     Print(colCnt,"hello",rowCnt);
     
     FileDelete(Symbol()+"HighTP.csv");
     FileClose(handle);
     
 
 }
 ArrayResize(Htp,rowCnt);
 
 
 
 
 }
 void ReadLTP(){
   int handle=0;
   handle = FileOpen(Symbol()+"LowTP.csv", FILE_CSV|FILE_READ,',');
   int row=0,col=0;
   int rowCnt,colCnt;
   Print(handle,"handle");
   
   if(handle>0)
   {
     while(True)
     {
       Print(row,"and",col);
       string temp = FileReadString(handle);
       Ltp[row]=temp;  
       
   
            
       if(FileIsLineEnding(handle))
       {
         Print("kuyyy");
         colCnt = col;
         col = 0;
         row++;
       }
       else
       {
         col++;
       }
       rowCnt = row;
       if(FileIsEnding(handle)) 
       break;
     }
     Print(colCnt,"hello",rowCnt);
     
     FileDelete(Symbol()+"LowTP.csv");
     FileClose(handle);
     
 
 }
 ArrayResize(Ltp,rowCnt);
 
 
 
 
 }
  
//+------------------------------------------------------------------+


//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| Tester function                                                  |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| ChartEvent function                                              |
//+------------------------------------------------------------------+

  
//---
   
  
//+------------------------------------------------------------------+
