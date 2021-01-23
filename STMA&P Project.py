import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import Image, ImageTk 
import pandas as pd #For data related tasks
import seaborn as sns
import matplotlib.pyplot as plt
import pymysql
import numpy as np
from sklearn.model_selection import train_test_split
import quandl #Stock market API for fetching Data
from sklearn.tree import DecisionTreeRegressor # Our DEcision Tree classifier
from sqlalchemy import create_engine
from datetime import datetime as dt
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


mydb=mysql.connector.connect(host="localhost",user='root',password='mysql',database='stocks')                  
my_cursor=mydb.cursor() 

sql7 = "DROP TABLE IF EXISTS market"
my_cursor.execute(sql7)

sql8 = "DROP TABLE IF EXISTS history"
my_cursor.execute(sql8)

sql9 = "DROP TABLE IF EXISTS prediction"
my_cursor.execute(sql9)
                                    
r=tk.Tk()
r.title("Stock Market Prediction")
r.state('zoomed')
photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
r.iconphoto(False, photo)
photo1 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\cover.png").resize((1280, 700), Image.ANTIALIAS))
label=tk.Label(image=photo1)
label.place(x=0,y=0)

class A(object):
    def openl(): 
        l = tk.Toplevel() 
        l.title("Stock Market Prediction: Login")
        l.state('zoomed')
        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
        l.iconphoto(False, photo)
        photo2 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\logincover.png").resize((1280, 700), Image.ANTIALIAS))
        label1=tk.Label(l,image=photo2)
        label1.image=photo2
        label1.place(x=0,y=0) 
        label1.pack()

        e= tk.Entry(l, width = 35, font=("Calibri",16)) 
        e.place(x = 500, y = 270, width = 300,height=50) 
  
        p = tk.Entry(l, show="*", width = 35, font=("Calibri",16)) 
        p.place(x = 500, y = 405, width = 300,height=50)

        def login():                                                                                                     
            current_e=e.get()  
            current_p=p.get()
            f=open("email.txt","w")
            f.write(str(current_e))
            f.close()
            my_q1="select email from user"
            my_cursor.execute(my_q1)
            x=[]
            for i in my_cursor:
                x.append(i[0])      
            if(current_e in x):   
                my_q="""select password from user where email=%s"""
                my_v=current_e
                my_cursor.execute(my_q,(my_v,)) 
                password_true=''
                for i in my_cursor:
                    password_true=i[0] 
                if(current_p==password_true):
                    def intro():
                        i = tk.Toplevel() 
                        i.title("Stock Market Prediction: Introduction")
                        i.state('zoomed')
                        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                        i.iconphoto(False, photo)
                        pho = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\intro.png"))
                        lab=tk.Label(i,image=pho)
                        lab.image=pho
                        lab.place(x=0,y=0) 

                        def openc(): 
                            c = tk.Toplevel() 
                            c.title("Stock Market Prediction: Company")
                            c.state('zoomed')
                            var = tk.IntVar()
                            photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                            c.iconphoto(False, photo)
                            photo4 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\companycover.png"))
                            label3=tk.Label(c,image=photo4)
                            label3.image=photo4
                            label3.place(x=0,y=0) 
                            
                            company = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                            company['values'] = ('TATASTEEL',  
                                            'RELIANCE',
                                            'HDFCBANK',
                                            'TITAN',
                                            'WIPRO',
                                            'CIPLA',
                                            'INFY',
                                            'ITC',
                                            'COALINDIA',
                                            'NESTLEIND',
                                            'BRITANNIA',
                                            'ONGC',
                                            'BPCL',
                                            'TCS',
                                            'GAIL')
                            company.place(x=520,y=155)
                            def callbackFunc1(event):
                                global cname
                                cname=company.get()
                                #print("You selected: ",cname)
                                f=open("com.txt","w")
                                f.write(str(cname))
                                f.close()
                                return(cname)
                            company.bind("<<ComboboxSelected>>", callbackFunc1)
                            
                            startdate = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                            startdate['values'] = ('2008-01-15',
                                                '2009-01-15',
                                                '2010-01-15',
                                                '2011-01-15',
                                                '2012-01-15',
                                                '2013-01-15',
                                                '2014-01-15',
                                                '2015-01-15',
                                                '2016-01-15',
                                                '2017-01-15',
                                                '2018-01-15',)
                            startdate.place(x=520,y=398)
                            def callbackFunc2(event):
                                global sdate
                                sdate=startdate.get()
                                #print("You selected: ",sdate)
                                f=open("start.txt","w")
                                f.write(str(sdate))
                                f.close()
                                return sdate
                            startdate.bind("<<ComboboxSelected>>", callbackFunc2)                        
                            
                            enddate = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                            enddate['values'] = ('2019-01-15','2020-01-15',
                                            '2021-01-15',
                                            '2022-01-15',
                                            '2023-01-15',
                                            '2024-01-15',
                                            '2025-01-15',
                                            '2026-01-15',
                                            '2027-01-15',
                                            '2028-01-15',
                                            '2029-01-15') 
                            enddate.place(x=520,y=493)
                            def callbackFunc3(event):
                                global edate
                                edate=enddate.get()
                                #print("You selected: ",edate)
                                f=open("end.txt","w")
                                f.write(str(edate))
                                f.close()
                                return edate
                            enddate.bind("<<ComboboxSelected>>", callbackFunc3)

                            def num(): 
                                n = tk.Toplevel() 
                                n.title("Stock Market Prediction: Stocks")
                                n.state('zoomed')
                                photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                                n.iconphoto(False, photo)
                                ph = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\number.png").resize((1280, 700), Image.ANTIALIAS))
                                label4=tk.Label(n,image=ph)
                                label4.image=ph
                                label4.place(x=0,y=0) 
                                label4.pack()

                                e= tk.Entry(n, width = 30, font=("Calibri",16)) 
                                e.place(x = 490, y = 270, width = 300,height=50) 

                                button = tk.Button(n, text='Back', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=openc) 
                                button.place(x=450, y=600)
                                butto = tk.Button(n, text='Set', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=lambda: [var.set(1)]) 
                                butto.place(x=600, y=600)
                                butto.wait_variable(var)

                                stocknum=str(e.get())
                                f=open("stock_no.txt","w")
                                f.write(str(stocknum))
                                f.close()

                                f1=open("com.txt","r")
                                Cname=f1.read()

                                f2=open("start.txt","r")
                                StartDate=f2.read()

                                f3=open("end.txt","r")
                                EndDate=f3.read()

                                f4=open("stock_no.txt","r")
                                stocks_no=float(f4.read())

                                f1.close()
                                f2.close()
                                f3.close()
                                f4.close()


                                quandl.ApiConfig.api_key = 'yMZqmgK7D_ypZYdJvPZu'
                                stock_data = quandl.get('NSE/'+Cname, start_date=StartDate, end_date=EndDate)
                                df = pd.DataFrame(stock_data)
                                df = df.rename(columns = {'Total Trade Quantity': 'Total_Trade_Quantity', 'Turnover (Lacs)': 'Turnover_Lacs'}, inplace = False)
                                data=df

                                hostname="localhost"
                                dbname="stocks"
                                uname="root"
                                pwd="mysql"
                                engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                                .format(host=hostname, db=dbname, user=uname, pw=pwd))
                                df.to_sql('history', engine, index=False)

                                data.head()
                                data.isnull().sum()
                                x = data.loc[:,'High':'Turnover_Lacs']
                                y = data.loc[:,'Open']


                                #print("No. of stocks purchased at ",Cname,": ",stocks_no)
                                #print("Predicted value at which the stock market will open per stock at Rs.",prediction)

                                def get_Nifty(EndDate):
                                    list1=[]
                                    date=str(EndDate)
                                    for i in range(data.index.size):
                                        str1=str(data.index.values[i])
                                        str2=str1.split('T')
                                        list1.append(str2[0])

                                    date0=pd.to_datetime('today')
                                    date1=str(date0)
                                    r_date=date1.split(' ')
                                    recent_date=str(r_date[0])

                                    a = dt.strptime(date, "%Y-%m-%d")
                                    b = dt.strptime(recent_date, "%Y-%m-%d")

                                    n=data.shape[0]
                                    nifty=data.iloc[[n-1],[4]]
                                    word=str(nifty.index.values)
                                    word1=word.split('T')
                                    ddate=str(word1[0])
                                    p=ddate.split("'")
                                    q=str(p[1])
                                    r = dt.strptime(q, "%Y-%m-%d")

                                    if r<a:
                                        Nifty_o=data.loc[q]['Open']
                                        Nifty_h=data.loc[q]['High']
                                        Nifty_lo=data.loc[q]['Low']
                                        Nifty_la=data.loc[q]['Last']
                                        Nifty_c=data.loc[q]['Close']
                                        Nifty_ttq=data.loc[q]['Total_Trade_Quantity']
                                        Nifty_tl=data.loc[q]['Turnover_Lacs']
                                        return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                    if a<b:
                                        if date in list1:
                                            Nifty_o=data.loc[EndDate]['Open']
                                            Nifty_h=data.loc[EndDate]['High']
                                            Nifty_lo=data.loc[EndDate]['Low']
                                            Nifty_la=data.loc[EndDate]['Last']
                                            Nifty_c=data.loc[EndDate]['Close']
                                            Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                            Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                            return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl


                                        else:
                                            x=date.split('-')
                                            d=int(x[2])
                                            d=d-1

                                            if d<10:
                                                EndDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                            
                                            else:
                                                EndDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                            if EndDate in list1:
                                                Nifty_o=data.loc[EndDate]['Open']
                                                Nifty_h=data.loc[EndDate]['High']
                                                Nifty_lo=data.loc[EndDate]['Low']
                                                Nifty_la=data.loc[EndDate]['Last']
                                                Nifty_c=data.loc[EndDate]['Close']
                                                Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                                Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                                return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                            else:
                                                x=date.split('-')
                                                d=int(x[2])
                                                d=d-2
                                            
                                                if d<10:
                                                    EndDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                            
                                                else:
                                                    EndDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                                Nifty_o=data.loc[EndDate]['Open']
                                                Nifty_h=data.loc[EndDate]['High']
                                                Nifty_lo=data.loc[EndDate]['Low']
                                                Nifty_la=data.loc[EndDate]['Last']
                                                Nifty_c=data.loc[EndDate]['Close']
                                                Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                                Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                                return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                    
                                    else:
                                        n=data.shape[0]
                                        nifty=data.iloc[[n-1],[4]]
                                        word=str(nifty.index.values)
                                        word1=word.split('T')
                                        ddate=str(word1[0])
                                        p=ddate.split("'")
                                        q=p[1]
                                        Nifty_o=data.loc[q]['Open']
                                        Nifty_h=data.loc[q]['High']
                                        Nifty_lo=data.loc[q]['Low']
                                        Nifty_la=data.loc[q]['Last']
                                        Nifty_c=data.loc[q]['Close']
                                        Nifty_ttq=data.loc[q]['Total_Trade_Quantity']
                                        Nifty_tl=data.loc[q]['Turnover_Lacs']
                                        return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                
                                Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl=get_Nifty(EndDate)
                                x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.05,random_state = 101)
                                Classifier = DecisionTreeRegressor()
                                Classifier.fit(x_train,y_train)
                                test = [[Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl]]
                                prediction1 = Classifier.predict(test)
                                prediction=float(prediction1[0])

                                def get_Revenue(Cname):
                                    if Cname=='TATASTEEL':
                                        Revenue= 157668.0
                                    if Cname=='RELIANCE':
                                        Revenue= 659205.0
                                    if Cname=='HDFCBANK':
                                        Revenue= 147068.27
                                    if Cname=='TITAN':
                                        Revenue= 20010.0
                                    if Cname=='WIPRO':
                                        Revenue= 63862.6
                                    if Cname=='CIPLA':
                                        Revenue= 17476.19
                                    if Cname=='INFY':
                                        Revenue= 93594.0
                                    if Cname=='ITC':
                                        Revenue= 52035.0
                                    if Cname=='COALINDIA':
                                        Revenue= 140603.0
                                    if Cname=='NESTLEIND':
                                        Revenue= 12615.78
                                    if Cname=='BRITANNIA':
                                        Revenue= 10672.97
                                    if Cname=='ONGC':
                                        Revenue= 433532.97
                                    if Cname=='BPCL':
                                        Revenue= 286501.23
                                    if Cname=='TCS':
                                        Revenue= 161541.0
                                    if Cname=='GAIL':
                                        Revenue= 74054.85
                                    return Revenue

                                def Outcome(num_stocks,prediction,StartDate):
                                    list1=[]
                                    date=str(StartDate)

                                    for i in range(data.index.size):
                                        str1=str(data.index.values[i])
                                        str2=str1.split('T')
                                        list1.append(str2[0])

                                    a = dt.strptime(date, "%Y-%m-%d")
                                    
                                    nifty=data.iloc[[0],[0]]
                                    word=str(nifty.index.values)
                                    word1=word.split('T')
                                    ddate=str(word1[0])
                                    p=ddate.split("'")
                                    q=str(p[1])
                                    r = dt.strptime(q, "%Y-%m-%d")

                                    if a>=r:
                                        if date in list1:
                                            Open_Nifty=data.loc[StartDate]['Open']
                                        
                                        else:
                                            x=date.split('-')
                                            d=int(x[2])
                                            d=d+1

                                            if d<10:
                                                StartDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                            
                                            else:
                                                StartDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                            if StartDate in list1:
                                                Open_Nifty=data.loc[StartDate]['Open']
                                            
                                            else:
                                                x=date.split('-')
                                                d=int(x[2])
                                                d=d+2
                                            
                                                if d<10:
                                                    StartDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                                    Open_Nifty=data.loc[StartDate]['Open']
                                            
                                                else:
                                                    StartDate=str(x[0])+'-'+str(x[1])+'-'+str(d)
                                                    Open_Nifty=data.loc[StartDate]['Open']
    
                                    else:
                                        nifty=data.iloc[[0],[0]]
                                        word=str(nifty.index.values)
                                        word1=word.split('T')
                                        ddate=str(word1[0])
                                        p=ddate.split("'")
                                        q=p[1]
                                        Open_Nifty=data.loc[q]['Open']
                                    
                                    result=prediction-Open_Nifty
                                    
                                    if result<0:
                                        loss=-(result)
                                        outcome=loss*num_stocks
                                        return outcome,-1,Open_Nifty
                                    else:
                                        gain=result
                                        outcome=gain*num_stocks
                                        return outcome,1,Open_Nifty

                                Revenue= float(get_Revenue(Cname))
                                outcome,b,Open_Nifty=Outcome(stocks_no,prediction,StartDate)
                                f=open("opennifty.txt","w")
                                f.write(str(Open_Nifty))
                                f.close()
                                # if b<0:
                                #     print("Loss is expected! Total loss expected by ",EndDate," is: ",round(outcome,2))
                                # else:
                                #     print("Profit is expected! Total profit expected by ",EndDate," is: ",round(outcome,2))
                                mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="mysql",
                                database="stocks" )

                                mycursor = mydb.cursor()
                                
                                Revenue= float(get_Revenue(Cname))
                                mycursor.execute("CREATE TABLE prediction(C_Name varchar(15) not null, StartDate date primary key not null, EndDate date not null,Prediction_Value float,foreign key(C_Name) references Company(C_Name))")
                                mycursor.execute("CREATE TABLE market(C_Name varchar(15) not null,E_Date date primary key not null,Nifty float,Revenue double, foreign key (C_Name) references Company(C_Name))")

                                sql1="INSERT INTO prediction VALUES(%s,%s,%s,%s)"
                                val1=(Cname,StartDate,EndDate,prediction)
                                mycursor.execute(sql1,val1)
                                mydb.commit()
                                Nif=float(Nifty_c)

                                sql2="INSERT INTO market VALUES(%s,%s,%s,%s)"
                                val2=(Cname,EndDate,Nif,Revenue)
                                mycursor.execute(sql2,val2)
                                mydb.commit()

                                f0=open("email.txt","r")
                                Email=f0.read()

                                f1=open("com.txt","r")
                                C_Name=f1.read()

                                f2=open("start.txt","r")
                                Sdate=f2.read()

                                f3=open("end.txt","r")
                                Edate=f3.read()

                                f4=open("stock_no.txt","r")
                                stocks_no=float(f4.read())

                                f5=open("opennifty.txt","r")
                                Open_Nifty=float(f5.read())

                                f0.close()
                                f1.close()
                                f2.close()
                                f3.close()
                                f4.close()
                                f5.close()

                                mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="mysql",
                                database="stocks" )

                                mycursor = mydb.cursor()

                                valuation=stocks_no*Open_Nifty
                                sql11="INSERT INTO Log VALUES(%s,%s,%s,%s,%s,%s)"
                                val11=(Email,C_Name,Sdate,Edate,stocks_no,valuation)
                                mycursor.execute(sql11,val11)
                                mydb.commit()

                                # sql5="SELECT * FROM market"
                                # mycursor.execute(sql5)
                                # myresult = mycursor.fetchall()
                                # for x in myresult:
                                #     print(x)
                                # print('\n')
                                # sql6="SELECT * FROM prediction"
                                # mycursor.execute(sql6)
                                # myresult = mycursor.fetchall()
                                # for x in myresult:
                                #     print(x)
                                # print('\n')
                                # f5=open("com.txt","r")
                                # Cname=str(f5.read())
                                # f5.close()
                                # sql9 = """SELECT * FROM Company WHERE C_Name ='%s'"""%(Cname)
                                # mycursor.execute(sql9)
                                # myresult = mycursor.fetchall()
                                # for x in myresult:
                                #     print(x)
                                
                                engine.dispose()
                                # #GRAPH START#
                                # plt.figure(figsize=(12,10), dpi= 70)
                                # sns.heatmap(data.corr(), xticklabels=data.corr().columns, yticklabels=data.corr().columns, cmap='spring', center=0, annot=True)
                                # plt.title('Correlogram of Chosen Stock Market Indices',fontsize=22)
                                # plt.xticks(fontsize=9)
                                # plt.yticks(fontsize=9)
                                # plt.show(block=False)
                                # input('press <ENTER> to continue')
                                # #GRAPH END#

                                def final(): 
                                    f = tk.Toplevel() 
                                    f.title("Stock Market Prediction")
                                    f.state('zoomed')
                                    photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                                    f.iconphoto(False, photo)
                                    ph = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\final.png"))
                                    label4=tk.Label(f,image=ph)
                                    label4.image=ph
                                    label4.place(x=0,y=100) 
                                    f.config(bg='#f89b50')
                                    stno="No. of stocks purchased at "+str(Cname)+": "+str(stocks_no)
                                    predict="Predicted value at which the stock market will open at Rs."+str(prediction)
                                    if b<0:
                                        str3="Loss is expected! Total loss expected by "+str(EndDate)+" is: "+str(round(outcome,2))
                                    else:
                                        str3="Profit is expected! Total profit expected by "+str(EndDate)+" is: "+str(round(outcome,2))
                                    T=tk.Text(f, height=3, width=150, font="Calibri 20", cursor='none')
                                    T.pack()
                                    T.insert(tk.END, stno+"\n")
                                    T.insert(tk.END, predict+"\n")
                                    T.insert(tk.END, str3)
                                    mycursor = mydb.cursor()
                                    mycursor.execute("SELECT * FROM market")
                                    tree=ttk.Treeview(f,height=1, style="mystyle.Treeview")
                                    style = ttk.Style()
                                    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                    style.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                    tree['show']='headings'
                                    tree["columns"]=("Cname","EndDate","Nifty","Revenue")
                                    tree.column("Cname", width=200,anchor=tk.CENTER)
                                    tree.column("EndDate", width=200,anchor=tk.CENTER)
                                    tree.column("Nifty", width=200,anchor=tk.CENTER)
                                    tree.column("Revenue", width=200,anchor=tk.CENTER)
                                    tree.heading("Cname", text="Company Name",anchor=tk.CENTER)
                                    tree.heading("EndDate", text="End Date",anchor=tk.CENTER)
                                    tree.heading("Nifty", text="Nifty Value",anchor=tk.CENTER)
                                    tree.heading("Revenue", text="Revenue",anchor=tk.CENTER)
                                    i=0
                                    for ro in mycursor:
                                        tree.insert('',i,text='',values=(ro[0],ro[1],ro[2],ro[3]))
                                        i=i+1
                                    tree.pack()
                                    tree.place(x=260,y=200)

                                    mycursor.execute("SELECT * FROM prediction")
                                    tree1=ttk.Treeview(f, height=1, style="mystyle.Treeview")
                                    tree1['show']='headings'
                                    style1 = ttk.Style()
                                    style.theme_use("classic")
                                    style1.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                    style1.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                    style1.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                    tree1["columns"]=("Cname","StartDate","EndDate","prediction")
                                    tree1.column("Cname", width=200,  anchor=tk.CENTER)
                                    tree1.column("StartDate", width=200,anchor=tk.CENTER)
                                    tree1.column("EndDate", width=200, anchor=tk.CENTER)
                                    tree1.column("prediction", width=200,anchor=tk.CENTER)
                                    tree1.heading("Cname", text="Company Name",anchor=tk.CENTER)
                                    tree1.heading("StartDate", text="Start Date",anchor=tk.CENTER)
                                    tree1.heading("EndDate", text="End Date",anchor=tk.CENTER)
                                    tree1.heading("prediction", text="Prediction",anchor=tk.CENTER)
                                    i=0
                                    for ro in mycursor:
                                        tree1.insert('',i,values=(ro[0],ro[1],ro[2],ro[3]))
                                        i=i+1
                                    tree1.pack()
                                    tree1.place(x=260,y=300)

                                    mycursor = mydb.cursor()
                                    mycursor.execute("""SELECT * FROM Company WHERE C_Name ='%s'"""%(Cname))
                                    tree2=ttk.Treeview(f,height=1, style="mystyle.Treeview")
                                    style2 = ttk.Style()
                                    style2.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                    style2.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                    style2.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                    tree2['show']='headings'
                                    tree2["columns"]=("ISN_ID","C_Name","Found_Date","Industry")
                                    tree2.column("ISN_ID", width=200,anchor=tk.CENTER)
                                    tree2.column("C_Name", width=200,anchor=tk.CENTER)
                                    tree2.column("Found_Date", width=200,anchor=tk.CENTER)
                                    tree2.column("Industry", width=200,anchor=tk.CENTER)
                                    tree2.heading("ISN_ID", text="NSE ID",anchor=tk.CENTER)
                                    tree2.heading("C_Name", text="Company Name",anchor=tk.CENTER)
                                    tree2.heading("Found_Date", text="Founded",anchor=tk.CENTER)
                                    tree2.heading("Industry", text="Industry",anchor=tk.CENTER)
                                    i=0
                                    for ro in mycursor:
                                        tree2.insert('',i,text='',values=(ro[0],ro[1],ro[2],ro[3]))
                                        i=i+1
                                    tree2.pack()
                                    tree2.place(x=260,y=400)
                                    
                                    def l(): 
                                        l = tk.Toplevel() 
                                        l.title("Stock Market Prediction: Graph")
                                        l.state('zoomed')
                                        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                                        l.iconphoto(False, photo)
                                        l.config(bg='#f89b50')
                                        def create_plot():
                                            sns.set(style="whitegrid")
                                            corr = data.corr()
                                            f=plt.figure(figsize=(12,10), dpi= 70)
                                            cmap = sns.diverging_palette(220, 10, as_cmap=True)
                                            sns.heatmap(corr,vmax=.3,square=True,xticklabels=data.corr().columns, yticklabels=data.corr().columns, cmap=cmap, center=0, annot=True)
                                            plt.title('Correlogram of Chosen Stock Market Indices',fontsize=22)
                                            plt.xticks(fontsize=9)
                                            plt.yticks(fontsize=9)
                                            #plt.show(block=False)
                                            #input('press <ENTER> to continue')
                                            return f
                                        fig = create_plot()
                                        canvas = FigureCanvasTkAgg(fig, master=l)  
                                        canvas.draw()
                                        canvas.get_tk_widget().pack()


                                    buttong = tk.Button(f, text='View Graph', width=15, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=l) 
                                    buttong.place(x=570, y=600)

                                button4 = tk.Button(n, text='Go!', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=final) 
                                button4.place(x=760, y=600)

                            button4 = tk.Button(c, text='Next', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=num) 
                            button4.place(x=660, y=600)
                            button = tk.Button(c, text='Back', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=intro) 
                            button.place(x=510, y=600)
                        button = tk.Button(i, text='Next', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000',font="Monospace 14", command=openc) 
                        button.place(x=570, y=600)  
                    intro()    
                else:
                    messagebox.showinfo("Error","Wrong password") 
                    
            else:
                messagebox.showinfo("Error","Wrong email") 
            
        button3 = tk.Button(l, text='Log in', width=15, height=2, bg='#ffffff',activebackground='#f56933',foreground='#000000',font="Monospace 14", command=login) 
        button3.place(x=550, y=550)
        

    def opens(): 
        s = tk.Toplevel() 
        s.title("Stock Market Prediction: Signup")
        s.state('zoomed')
        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
        s.iconphoto(False, photo)
        photo3 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\signupcover.png"))
        label2=tk.Label(s,image=photo3)
        label2.image=photo3
        label2.place(x=0,y=0) 
  
        e1 = tk.Entry(s, width = 35, font=("Calibri",16)) 
        e1.place(x = 500, y = 250, width = 300,height=50) 
  
        p1 = tk.Entry(s, width = 35, font=("Calibri",16)) 
        p1.place(x = 500, y = 335, width = 300,height=50)

        pn = tk.Entry(s, width = 35, font=("Calibri",16)) 
        pn.place(x = 500, y = 430, width = 300,height=50)

        def signup():                                                                                                     
            e_id=e1.get()  
            pwd=p1.get()
            pno=pn.get()
            f=open("email.txt","w")
            f.write(str(e_id))
            f.close()
            if(len(pno)!=10 or (not pno.isdigit())):
                messagebox.showinfo("Error","Ivalid phone number")
            else:
                my_q="""insert into user(email,password,Phone_No) values (%s,%s,%s)"""
                my_cursor.execute(my_q,(e_id,pwd,pno))
                mydb.commit()

                def intro():
                    i = tk.Toplevel() 
                    i.title("Stock Market Prediction: Introduction")
                    i.state('zoomed')
                    photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                    i.iconphoto(False, photo)
                    pho = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\intro.png"))
                    lab=tk.Label(i,image=pho)
                    lab.image=pho
                    lab.place(x=0,y=0) 

                    def openc(): 
                        c = tk.Toplevel() 
                        c.title("Stock Market Prediction: Company")
                        c.state('zoomed')
                        var = tk.IntVar()
                        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                        c.iconphoto(False, photo)
                        photo4 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\companycover.png"))
                        label3=tk.Label(c,image=photo4)
                        label3.image=photo4
                        label3.place(x=0,y=0) 
                        
                        company = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                        company['values'] = ('TATASTEEL',  
                                        'RELIANCE',
                                        'HDFCBANK',
                                        'TITAN',
                                        'WIPRO',
                                        'CIPLA',
                                        'INFY',
                                        'ITC',
                                        'COALINDIA',
                                        'NESTLEIND',
                                        'BRITANNIA',
                                        'ONGC',
                                        'BPCL',
                                        'TCS',
                                        'GAIL')
                        company.place(x=520,y=155)
                        def callbackFunc1(event):
                            global cname
                            cname=company.get()
                            #print("You selected: ",cname)
                            f=open("com.txt","w")
                            f.write(str(cname))
                            f.close()
                            return(cname)
                        company.bind("<<ComboboxSelected>>", callbackFunc1)
                        
                        startdate = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                        startdate['values'] = ('2008-01-15',
                                            '2009-01-15',
                                            '2010-01-15',
                                            '2011-01-15',
                                            '2012-01-15',
                                            '2013-01-15',
                                            '2014-01-15',
                                            '2015-01-15',
                                            '2016-01-15',
                                            '2017-01-15',
                                            '2018-01-15')
                        startdate.place(x=520,y=398)
                        def callbackFunc2(event):
                            global sdate
                            sdate=startdate.get()
                            #print("You selected: ",sdate)
                            f=open("start.txt","w")
                            f.write(str(sdate))
                            f.close()
                            return sdate
                        startdate.bind("<<ComboboxSelected>>", callbackFunc2)                        
                        
                        enddate = ttk.Combobox(c, width = 18, height=10,font="Monospace 16") 
                        enddate['values'] = ('2019-01-15','2020-01-15',
                                            '2021-01-15',
                                            '2022-01-15',
                                            '2023-01-15',
                                            '2024-01-15',
                                            '2025-01-15',
                                            '2026-01-15',
                                            '2027-01-15',
                                            '2028-01-15',
                                            '2029-01-15')
                        enddate.place(x=520,y=493)
                        def callbackFunc3(event):
                            global edate
                            edate=enddate.get()
                            #print("You selected: ",edate)
                            f=open("end.txt","w")
                            f.write(str(edate))
                            f.close()
                            return edate
                        enddate.bind("<<ComboboxSelected>>", callbackFunc3)

                        def num(): 
                            n = tk.Toplevel() 
                            n.title("Stock Market Prediction: Stocks")
                            n.state('zoomed')
                            photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                            n.iconphoto(False, photo)
                            ph = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\number.png").resize((1280, 700), Image.ANTIALIAS))
                            label4=tk.Label(n,image=ph)
                            label4.image=ph
                            label4.place(x=0,y=0) 
                            label4.pack()

                            e= tk.Entry(n, width = 30, font=("Calibri",16)) 
                            e.place(x = 490, y = 270, width = 300,height=50) 

                            button = tk.Button(n, text='Back', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=openc) 
                            button.place(x=450, y=600)
                            butto = tk.Button(n, text='Set', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=lambda: [var.set(1)]) 
                            butto.place(x=600, y=600)
                            butto.wait_variable(var)

                            stocknum=str(e.get())
                            f=open("stock_no.txt","w")
                            f.write(str(stocknum))
                            f.close()

                            f1=open("com.txt","r")
                            Cname=f1.read()

                            f2=open("start.txt","r")
                            StartDate=f2.read()

                            f3=open("end.txt","r")
                            EndDate=f3.read()

                            f4=open("stock_no.txt","r")
                            stocks_no=float(f4.read())

                            f1.close()
                            f2.close()
                            f3.close()
                            f4.close()

                            quandl.ApiConfig.api_key = 'yMZqmgK7D_ypZYdJvPZu'
                            stock_data = quandl.get('NSE/'+Cname, start_date=StartDate, end_date=EndDate)
                            df = pd.DataFrame(stock_data)
                            df = df.rename(columns = {'Total Trade Quantity': 'Total_Trade_Quantity', 'Turnover (Lacs)': 'Turnover_Lacs'}, inplace = False)
                            data=df

                            hostname="localhost"
                            dbname="stocks"
                            uname="root"
                            pwd="mysql"
                            engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                            .format(host=hostname, db=dbname, user=uname, pw=pwd))
                            df.to_sql('history', engine, index=False)

                            data.head()
                            data.isnull().sum()
                            x = data.loc[:,'High':'Turnover_Lacs']
                            y = data.loc[:,'Open']
                            #print("No. of stocks purchased at ",Cname,": ",stocks_no)
                            #print("Predicted value at which the stock market will open per stock at Rs.",prediction)

                            def get_Nifty(EndDate):
                                list1=[]
                                date=str(EndDate)
                                for i in range(data.index.size):
                                    str1=str(data.index.values[i])
                                    str2=str1.split('T')
                                    list1.append(str2[0])

                                date0=pd.to_datetime('today')
                                date1=str(date0)
                                r_date=date1.split(' ')
                                recent_date=str(r_date[0])

                                a = dt.strptime(date, "%Y-%m-%d")
                                b = dt.strptime(recent_date, "%Y-%m-%d")

                                n=data.shape[0]
                                nifty=data.iloc[[n-1],[4]]
                                word=str(nifty.index.values)
                                word1=word.split('T')
                                ddate=str(word1[0])
                                p=ddate.split("'")
                                q=str(p[1])
                                r = dt.strptime(q, "%Y-%m-%d")

                                if r<a:
                                    Nifty_o=data.loc[q]['Open']
                                    Nifty_h=data.loc[q]['High']
                                    Nifty_lo=data.loc[q]['Low']
                                    Nifty_la=data.loc[q]['Last']
                                    Nifty_c=data.loc[q]['Close']
                                    Nifty_ttq=data.loc[q]['Total_Trade_Quantity']
                                    Nifty_tl=data.loc[q]['Turnover_Lacs']
                                    return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                if a<b:
                                    if date in list1:
                                        Nifty_o=data.loc[EndDate]['Open']
                                        Nifty_h=data.loc[EndDate]['High']
                                        Nifty_lo=data.loc[EndDate]['Low']
                                        Nifty_la=data.loc[EndDate]['Last']
                                        Nifty_c=data.loc[EndDate]['Close']
                                        Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                        Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                        return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                                    else:
                                        x=date.split('-')
                                        d=int(x[2])
                                        d=d-1

                                        if d<10:
                                            EndDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                        
                                        else:
                                            EndDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                        if EndDate in list1:
                                            Nifty_o=data.loc[EndDate]['Open']
                                            Nifty_h=data.loc[EndDate]['High']
                                            Nifty_lo=data.loc[EndDate]['Low']
                                            Nifty_la=data.loc[EndDate]['Last']
                                            Nifty_c=data.loc[EndDate]['Close']
                                            Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                            Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                            return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl
                                    
                                        else:
                                            x=date.split('-')
                                            d=int(x[2])
                                            d=d-2
                                        
                                            if d<10:
                                                EndDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                        
                                            else:
                                                EndDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                            Nifty_o=data.loc[EndDate]['Open']
                                            Nifty_h=data.loc[EndDate]['High']
                                            Nifty_lo=data.loc[EndDate]['Low']
                                            Nifty_la=data.loc[EndDate]['Last']
                                            Nifty_c=data.loc[EndDate]['Close']
                                            Nifty_ttq=data.loc[EndDate]['Total_Trade_Quantity']
                                            Nifty_tl=data.loc[EndDate]['Turnover_Lacs']
                                            return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl
                                
                                else:
                                    n=data.shape[0]
                                    nifty=data.iloc[[n-1],[4]]
                                    word=str(nifty.index.values)
                                    word1=word.split('T')
                                    ddate=str(word1[0])
                                    p=ddate.split("'")
                                    q=p[1]
                                    Nifty_o=data.loc[q]['Open']
                                    Nifty_h=data.loc[q]['High']
                                    Nifty_lo=data.loc[q]['Low']
                                    Nifty_la=data.loc[q]['Last']
                                    Nifty_c=data.loc[q]['Close']
                                    Nifty_ttq=data.loc[q]['Total_Trade_Quantity']
                                    Nifty_tl=data.loc[q]['Turnover_Lacs']
                                    return Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl

                            Nifty_o,Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl=get_Nifty(EndDate)
                            x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.05,random_state = 101)
                            Classifier = DecisionTreeRegressor()
                            Classifier.fit(x_train,y_train)
                            test = [[Nifty_h,Nifty_lo,Nifty_la,Nifty_c,Nifty_ttq,Nifty_tl]]
                            prediction1 = Classifier.predict(test)
                            prediction=float(prediction1[0])

                            def get_Revenue(Cname):
                                if Cname=='TATASTEEL':
                                    Revenue= 157668.0
                                if Cname=='RELIANCE':
                                    Revenue= 659205.0
                                if Cname=='HDFCBANK':
                                    Revenue= 147068.27
                                if Cname=='TITAN':
                                    Revenue= 20010.0
                                if Cname=='WIPRO':
                                    Revenue= 63862.6
                                if Cname=='CIPLA':
                                    Revenue= 17476.19
                                if Cname=='INFY':
                                    Revenue= 93594.0
                                if Cname=='ITC':
                                    Revenue= 52035.0
                                if Cname=='COALINDIA':
                                    Revenue= 140603.0
                                if Cname=='NESTLEIND':
                                    Revenue= 12615.78
                                if Cname=='BRITANNIA':
                                    Revenue= 10672.97
                                if Cname=='ONGC':
                                    Revenue= 433532.97
                                if Cname=='BPCL':
                                    Revenue= 286501.23
                                if Cname=='TCS':
                                    Revenue= 161541.0
                                if Cname=='GAIL':
                                    Revenue= 74054.85
                                return Revenue

                            def Outcome(num_stocks,prediction,StartDate):
                                list1=[]
                                date=str(StartDate)

                                for i in range(data.index.size):
                                    str1=str(data.index.values[i])
                                    str2=str1.split('T')
                                    list1.append(str2[0])


                                a = dt.strptime(date, "%Y-%m-%d")
                                
                                nifty=data.iloc[[0],[0]]
                                word=str(nifty.index.values)
                                word1=word.split('T')
                                ddate=str(word1[0])
                                p=ddate.split("'")
                                q=str(p[1])
                                r = dt.strptime(q, "%Y-%m-%d")


                                if a>=r:
                                    if date in list1:
                                        Open_Nifty=data.loc[StartDate]['Open']
                                    
                                    else:
                                        x=date.split('-')
                                        d=int(x[2])
                                        d=d+1

                                        if d<10:
                                            StartDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                        
                                        else:
                                            StartDate=str(x[0])+'-'+str(x[1])+'-'+str(d)

                                        if StartDate in list1:
                                            Open_Nifty=data.loc[StartDate]['Open']
                                        
                                        else:
                                            x=date.split('-')
                                            d=int(x[2])
                                            d=d+2
                                        
                                            if d<10:
                                                StartDate=str(x[0])+'-'+str(x[1])+'-0'+str(d)
                                                Open_Nifty=data.loc[StartDate]['Open']
                                        
                                            else:
                                                StartDate=str(x[0])+'-'+str(x[1])+'-'+str(d)
                                                Open_Nifty=data.loc[StartDate]['Open']

                                else:
                                    nifty=data.iloc[[0],[0]]
                                    word=str(nifty.index.values)
                                    word1=word.split('T')
                                    ddate=str(word1[0])
                                    p=ddate.split("'")
                                    q=p[1]
                                    Open_Nifty=data.loc[q]['Open']
                                
                                result=prediction-Open_Nifty
                                
                                if result<0:
                                    loss=-(result)
                                    outcome=loss*num_stocks
                                    return outcome,-1,Open_Nifty
                                else:
                                    gain=result
                                    outcome=gain*num_stocks
                                    return outcome,1,Open_Nifty
         
                            
                            Revenue= float(get_Revenue(Cname))
                            outcome,b,Open_Nifty=Outcome(stocks_no,prediction,StartDate)
                            f=open("opennifty.txt","w")
                            f.write(str(Open_Nifty))
                            f.close()
                            mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="mysql",
                            database="stocks" )

                            mycursor = mydb.cursor()

                            
                            Revenue= float(get_Revenue(Cname))

                            mycursor.execute("CREATE TABLE prediction(C_Name varchar(15) not null, StartDate date primary key not null, EndDate date not null,Prediction_Value float,foreign key(C_Name) references Company(C_Name))")
                            mycursor.execute("CREATE TABLE market(C_Name varchar(15) not null,E_Date date primary key not null,Nifty float,Revenue double, foreign key (C_Name) references Company(C_Name))")
                            sql1="INSERT INTO prediction VALUES(%s,%s,%s,%s)"
                            val1=(Cname,StartDate,EndDate,prediction)
                            mycursor.execute(sql1,val1)
                            mydb.commit()
                            Nif=float(Nifty_c)

                            sql2="INSERT INTO market VALUES(%s,%s,%s,%s)"
                            val2=(Cname,EndDate,Nif,Revenue)
                            mycursor.execute(sql2,val2)
                            mydb.commit()

                            f0=open("email.txt","r")
                            Email=f0.read()

                            f1=open("com.txt","r")
                            C_Name=f1.read()

                            f2=open("start.txt","r")
                            Sdate=f2.read()

                            f3=open("end.txt","r")
                            Edate=f3.read()

                            f4=open("stock_no.txt","r")
                            stocks_no=float(f4.read())

                            f5=open("opennifty.txt","r")
                            Open_Nifty=float(f5.read())

                            f0.close()
                            f1.close()
                            f2.close()
                            f3.close()
                            f4.close()
                            f5.close()

                            mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="mysql",
                            database="stocks" )

                            mycursor = mydb.cursor()

                            valuation=stocks_no*Open_Nifty
                            sql11="INSERT INTO Log VALUES(%s,%s,%s,%s,%s,%s)"
                            val11=(Email,C_Name,Sdate,Edate,stocks_no,valuation)
                            mycursor.execute(sql11,val11)
                            mydb.commit()
                            
                            engine.dispose()

                            def final(): 
                                f = tk.Toplevel() 
                                f.title("Stock Market Prediction")
                                f.state('zoomed')
                                photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                                f.iconphoto(False, photo)
                                ph = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\final.png"))
                                label4=tk.Label(f,image=ph)
                                label4.image=ph
                                label4.place(x=0,y=100) 
                                f.config(bg='#f89b50')
                                stno="No. of stocks purchased at "+str(Cname)+": "+str(stocks_no)
                                predict="Predicted value at which the stock market will open at Rs."+str(prediction)
                                if b<0:
                                    str3="Loss is expected! Total loss expected by "+str(EndDate)+" is: "+str(round(outcome,2))
                                else:
                                    str3="Profit is expected! Total profit expected by "+str(EndDate)+" is: "+str(round(outcome,2))
                                T=tk.Text(f, height=3, width=150, font="Calibri 20", cursor='none')
                                T.pack()
                                T.insert(tk.END, stno+"\n")
                                T.insert(tk.END, predict+"\n")
                                T.insert(tk.END, str3)
                                mycursor = mydb.cursor()
                                mycursor.execute("SELECT * FROM market")
                                tree=ttk.Treeview(f,height=1, style="mystyle.Treeview")
                                style = ttk.Style()
                                style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                style.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                tree['show']='headings'
                                tree["columns"]=("Cname","EndDate","Nifty","Revenue")
                                tree.column("Cname", width=200,anchor=tk.CENTER)
                                tree.column("EndDate", width=200,anchor=tk.CENTER)
                                tree.column("Nifty", width=200,anchor=tk.CENTER)
                                tree.column("Revenue", width=200,anchor=tk.CENTER)
                                tree.heading("Cname", text="Company Name",anchor=tk.CENTER)
                                tree.heading("EndDate", text="End Date",anchor=tk.CENTER)
                                tree.heading("Nifty", text="Nifty Value",anchor=tk.CENTER)
                                tree.heading("Revenue", text="Revenue",anchor=tk.CENTER)
                                i=0
                                for ro in mycursor:
                                    tree.insert('',i,text='',values=(ro[0],ro[1],ro[2],ro[3]))
                                    i=i+1
                                tree.pack()
                                tree.place(x=260,y=200)

                                mycursor.execute("SELECT * FROM prediction")
                                tree1=ttk.Treeview(f, height=1, style="mystyle.Treeview")
                                tree1['show']='headings'
                                style1 = ttk.Style()
                                style.theme_use("classic")
                                style1.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                style1.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                style1.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                tree1["columns"]=("Cname","StartDate","EndDate","prediction")
                                tree1.column("Cname", width=200,  anchor=tk.CENTER)
                                tree1.column("StartDate", width=200,anchor=tk.CENTER)
                                tree1.column("EndDate", width=200, anchor=tk.CENTER)
                                tree1.column("prediction", width=200,anchor=tk.CENTER)
                                tree1.heading("Cname", text="Company Name",anchor=tk.CENTER)
                                tree1.heading("StartDate", text="Start Date",anchor=tk.CENTER)
                                tree1.heading("EndDate", text="End Date",anchor=tk.CENTER)
                                tree1.heading("prediction", text="Prediction",anchor=tk.CENTER)
                                i=0
                                for ro in mycursor:
                                    tree1.insert('',i,values=(ro[0],ro[1],ro[2],ro[3]))
                                    i=i+1
                                tree1.pack()
                                tree1.place(x=260,y=300)

                                mycursor = mydb.cursor()
                                mycursor.execute("""SELECT * FROM Company WHERE C_Name ='%s'"""%(Cname))
                                tree2=ttk.Treeview(f,height=1, style="mystyle.Treeview")
                                style2 = ttk.Style()
                                style2.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=40) 
                                style2.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                                style2.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                                tree2['show']='headings'
                                tree2["columns"]=("ISN_ID","C_Name","Found_Date","Industry")
                                tree2.column("ISN_ID", width=200,anchor=tk.CENTER)
                                tree2.column("C_Name", width=200,anchor=tk.CENTER)
                                tree2.column("Found_Date", width=200,anchor=tk.CENTER)
                                tree2.column("Industry", width=200,anchor=tk.CENTER)
                                tree2.heading("ISN_ID", text="NSE ID",anchor=tk.CENTER)
                                tree2.heading("C_Name", text="Company Name",anchor=tk.CENTER)
                                tree2.heading("Found_Date", text="Founded",anchor=tk.CENTER)
                                tree2.heading("Industry", text="Industry",anchor=tk.CENTER)
                                i=0
                                for ro in mycursor:
                                    tree2.insert('',i,text='',values=(ro[0],ro[1],ro[2],ro[3]))
                                    i=i+1
                                tree2.pack()
                                tree2.place(x=260,y=400)

                                def l(): 
                                    l = tk.Toplevel() 
                                    l.title("Stock Market Prediction: Graph")
                                    l.state('zoomed')
                                    photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                                    l.iconphoto(False, photo)
                                    l.config(bg='#f89b50')
                                    def create_plot():
                                        sns.set(style="whitegrid")
                                        corr = data.corr()
                                        f=plt.figure(figsize=(12,10), dpi= 70)
                                        cmap = sns.diverging_palette(220, 10, as_cmap=True)
                                        sns.heatmap(corr,vmax=.3,square=True,xticklabels=data.corr().columns, yticklabels=data.corr().columns, cmap=cmap, center=0, annot=True)
                                        plt.title('Correlogram of Chosen Stock Market Indices',fontsize=22)
                                        plt.xticks(fontsize=9)
                                        plt.yticks(fontsize=9)
                                        return f
                                    fig = create_plot()
                                    canvas = FigureCanvasTkAgg(fig, master=l)  
                                    canvas.draw()
                                    canvas.get_tk_widget().pack()

                                buttong = tk.Button(f, text='View Graph', width=15, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=l) 
                                buttong.place(x=570, y=600)

                            button4 = tk.Button(n, text='Go!', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=final) 
                            button4.place(x=760, y=600)

                        button4 = tk.Button(c, text='Next', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=num) 
                        button4.place(x=660, y=600)
                        button = tk.Button(c, text='Back', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=intro) 
                        button.place(x=510, y=600)
                    button = tk.Button(i, text='Next', width=10, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000',font="Monospace 14", command=openc) 
                    button.place(x=570, y=600)
                intro() 
        button3 = tk.Button(s, text='Sign up', width=15, height=2, bg='#ffffff',activebackground='#f56933',foreground='#000000',font="Monospace 14", command=signup) 
        button3.place(x=550, y=550)

    def alog():
        a = tk.Toplevel() 
        a.title("Stock Market Prediction: Admin")
        a.state('zoomed')
        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
        a.iconphoto(False, photo)
        photo3 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\adlog.png"))
        label2=tk.Label(a,image=photo3)
        label2.image=photo3
        label2.place(x=0,y=0) 
  
        u = tk.Entry(a, width = 35, font=("Calibri",16)) 
        u.place(x = 530, y = 227, width = 300,height=50) 
  
        p = tk.Entry(a, width = 35, show="*", font=("Calibri",16)) 
        p.place(x = 530, y = 350, width = 300,height=50)

        def alogin():
            current_u=u.get()  
            current_p=p.get()     

            my_q1="select Name from admin"
            my_cursor.execute(my_q1)
            x=[]
            for i in my_cursor:
                x.append(i[0])      
            if(current_u in x):   
                my_q="""select Password from admin where Name=%s"""
                my_v=current_u
                my_cursor.execute(my_q,(my_v,)) 
                password_true=''
                for i in my_cursor:
                    password_true=i[0] 
                if(current_p==password_true):  
                    def admin():
                        d = tk.Toplevel() 
                        d.title("Stock Market Prediction: Admin")
                        d.state('zoomed')
                        photo = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\stats.png"))
                        d.iconphoto(False, photo)
                        photo3 = ImageTk.PhotoImage(Image.open(r"C:\Users\jeevita\OneDrive\Desktop\stock\ad.png"))
                        label2=tk.Label(d,image=photo3)
                        label2.image=photo3
                        label2.place(x=0,y=0) 
                        
                        mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="mysql",
                        database="stocks" )

                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT * FROM Log")
                        tree1=ttk.Treeview(d, style="mystyle.Treeview")
                        tree1['show']='headings'
                        style1 = ttk.Style()
                        style1.theme_use("classic")
                        style1.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15), rowheight=30) 
                        style1.configure("mystyle.Treeview.Heading", font=('Calibri', 16,'bold'),background="#5884c4",fieldbackground="#5884c4", foreground="white",rowheight=40)
                        style1.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
                        tree1["columns"]=("U_Email","C_Name","Sdate","Edate","stocks_no","Valuation")
                        tree1.column("U_Email", width=200,  anchor=tk.CENTER)
                        tree1.column("C_Name", width=170,  anchor=tk.CENTER)
                        tree1.column("Sdate", width=140,anchor=tk.CENTER)
                        tree1.column("Edate", width=150, anchor=tk.CENTER)
                        tree1.column("stocks_no", width=150,  anchor=tk.CENTER)
                        tree1.column("Valuation", width=150,anchor=tk.CENTER)
                        tree1.heading("U_Email", text="Email",anchor=tk.CENTER)
                        tree1.heading("C_Name", text="Company Name",anchor=tk.CENTER)
                        tree1.heading("Sdate", text="Start Date",anchor=tk.CENTER)
                        tree1.heading("Edate", text="End Date",anchor=tk.CENTER)
                        tree1.heading("stocks_no", text="No of stocks",anchor=tk.CENTER)
                        tree1.heading("Valuation", text="Valuation",anchor=tk.CENTER)
                        i=0
                        for ro in mycursor:
                            tree1.insert('',i,values=(ro[0],ro[1],ro[2],ro[3],ro[4],ro[5]))
                            i=i+1
                        tree1.pack()
                        tree1.place(x=200,y=150)
                        # sql55="SELECT * FROM Log"
                        # mycursor.execute(sql55)
                        # myresult = mycursor.fetchall()
                        # for x in myresult:
                        #     print(x)
                        # print('\n')
                        def graph():
                            conn = pymysql.connect("localhost", "root", "mysql", "stocks")
                            sql1 = pd.read_sql_query('''select*from Log''', conn)
                            df = pd.DataFrame(sql1, columns=['U_Email', 'C_Name', 'Sdate','Edate','stocks_no','Valuation'])

                            df2 = pd.DataFrame(data=df.groupby(['C_Name'],as_index=False).sum()) 

                            fig, axes = plt.subplots(1, 2, figsize=(20, 10), sharey=False)
                            fig.suptitle('Current Stats')

                            sns.barplot(ax=axes[0], x='C_Name', y='stocks_no',data=df2)
                            axes[0].set_title('No. of Stocks Purchased per Company')

                            sns.barplot(ax=axes[1], x='C_Name', y='Valuation',data=df2)
                            axes[1].set_title('Current Valuation per Company')
                            fig.subplots_adjust(wspace=0.5)
                            plt.show()
                        buttong = tk.Button(d, text='View Graph', width=15, height=1, bg='#ffffff',activebackground='#f56933',foreground='#000000', font="Monospace 14",command=graph) 
                        buttong.place(x=570, y=600)
                    admin()
            else:
                messagebox.showinfo("Error","Invalid username or password")

        button3 = tk.Button(a, text='Log in', width=15, height=2, bg='#ffffff',activebackground='#f56933',foreground='#000000',font="Monospace 14", command=alogin) 
        button3.place(x=580, y=490)

    myFont = font.Font(family='Monospace')
    button1 = tk.Button(r, text='Log in', width=23, height=2, bg='#ffffff',activebackground='#f56933',foreground='#000000', command=openl) 
    button1.place(x=200, y=250)
    button1['font'] = myFont
    button2 = tk.Button(r, text='Sign up', width=23, height=2, bg='#ffffff',activebackground='#f56933',foreground='#000000', command=opens) 
    button2.place(x=200, y=400)
    button2['font'] = myFont
    photo = PhotoImage(file = r"C:\Users\jeevita\OneDrive\Desktop\stock\admin.png") 
    photoimage = photo.subsample(1, 1) 
    button3 = tk.Button(r, text='Admin Log in',image = photo, width=40, height=40, bg='#ffffff',activebackground='#f56933',foreground='#000000', command=alog) 
    button3.place(x=20, y=20)
    button3['font'] = myFont
r.mainloop()
