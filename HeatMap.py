import tkinter, webbrowser
import tkinter as tk
from nsepython import *
import time

import Autoscheduler
import tickerSymbol
from datetime import datetime as dt
import yfinance as yf
import squeeze


#creating a dictionary to store ticker and pChange
dict = {}
ticker = []
stocklist = []
tup = None
timeframe = None

# setting up the UI using tkinter
MainF = tkinter.Tk()
MainF.title("NSE HeatMap       Market {}".format(nse_marketStatus().get('marketState')[0].get('marketStatus')))
MainF.geometry('1500x1000')
MainF.configure(background='white')

# This is for Button Frame , top of the main Frame
ButtonF = tkinter.Frame(MainF)
ButtonF.grid(row=0, column=0)

# This is the Ticker Frame , second frame to MainFrame
tickerF = tkinter.Frame(MainF)
tickerF.grid(row=1, column=0)

# For spacing between the buttons
padx = 20
pady=0


#Create Buttons on top of the frame
B1= tkinter.Button(ButtonF, text="N50", command=lambda: (refreshClick(), run('N50'), deletetuple()),font=('Calibri',16), bd=30)
B1.grid(row=0, column=1,padx = padx, pady = pady)
B2 = tkinter.Button(ButtonF, text="N100", command=lambda: (refreshClick(), run('N100'), deletetuple()),font=('Calibri',16), bd=30)
B2.grid(row=0, column=2,padx = padx, pady = pady)
B3 = tkinter.Button(ButtonF, text="N200", command=lambda: (refreshClick(), run('N200'), deletetuple()),font=('Calibri',16), bd=30)
B3.grid(row=0, column=3,padx = padx, pady = pady)
B4 = tkinter.Button(ButtonF, text="BroadMarket", command=lambda: (refreshClick(), run('BroadMarketIndices'), deletetuple()),
                    font=('Calibri',16), bd=30)
B4.grid(row=0, column=4,padx = padx, pady = pady)
B5 = tkinter.Button(ButtonF, text="Sectoral", command=lambda: (refreshClick(), run('SectoralIndices'), deletetuple()),
                    font=('Calibri',16), bd=30)
B5.grid(row=0, column=5,padx = padx, pady = pady)
B6 = tkinter.Button(ButtonF, text="LoserGainer", command=lambda: (refreshClick(), run('TopGainersLosers')),
                    font=('Calibri',16), bd=30)
B6.grid(row=0, column=6,padx = padx, pady = pady)
B7 = tkinter.Button(ButtonF, text="MostActive", command=lambda: (refreshClick(), run('MostActive'),deletetuple()),font=('Calibri',16), bd=30)
B7.grid(row=0, column=7,padx = padx, pady = pady)
B8 = tkinter.Button(ButtonF, text="InSqueeze", command=lambda: (refreshClick(), run('SqueezeScanner'),deletetuple()),font=('Calibri',14), bd=30)
B8.grid(row=0, column=8,padx = padx, pady = pady)
B9 = tkinter.Button(ButtonF, text="SellScanner", command=lambda: (refreshClick(), run('SellScanner'),deletetuple()),font=('Calibri',14), bd=30)
B9.grid(row=0, column=9,padx = padx, pady = pady)
B10 = tkinter.Button(ButtonF, text="TimeFrame", command=lambda: (refreshClick(), TimeFrame(),deletetuple()),font=('Calibri',14), bd=30)
B10.grid(row=0, column=10)



def get_companyName(symbol):
    return nse_eq(symbol)['info']['companyName']


def get_lastPrice(symbol):
    ticker = yf.Ticker(symbol+".NS")
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0],1)


def get_IndexLastPrice(symbol):
    return nse_get_index_quote(symbol)['last']


def get_IndexPercentChange(symbol):
    return nse_get_index_quote(symbol)['percChange']


def get_percentChange(symbol):
    ticker = yf.Ticker(symbol+".NS")
    todays_data = ticker.history(period='1d')
    Inc = todays_data['Close'][0] - todays_data['Open'][0]
    pChange = (Inc / todays_data['Open'][0])*100
    return round(pChange,1)


def refreshClick():
    #Destroy the Frame for ticker
    global tickerF
    tickerF.destroy()
    tickerF = tkinter.Frame(MainF)
    tickerF.grid(row=1, column=0)
    print("Refresh Clicked")

def run(Var):
    global stocklist, tup
    switcher = { 'N50':tickerSymbol.N50 ,
        'N100':tickerSymbol.N100,
        'N200':tickerSymbol.N200,
        'BroadMarketIndices':tickerSymbol.BroadMarketIndices,
        'ThematicIndices':tickerSymbol.ThematicIndices,
        'SectoralIndices':tickerSymbol.SectoralIndices,
        'MostActive':getMostActive(),
        'TopGainersLosers':getGainLose(),
        'SellScanner':SellScanner()
        #'SqueezeScanner':SqueezeScanner()
    }
    row = 0
    column = 0
    print(type(switcher.get(Var)))
    for item in switcher.get(Var):
        if "Indices" in Var:
            tup = (item, nse_get_index_quote(item)['last'],float(nse_get_index_quote(item)['percChange']))
        else:
            tup = (item, get_lastPrice(item), get_percentChange(item))

        symbol,lastPrice, Change = tup

        data = ("{}\n{}\n{}%".format(symbol, lastPrice, Change))

        print(data)

        stocklist.append(tuple(tup))

        dynamicColor, textcolor = getDynamicColor(Change)
        L1 = tkinter.Label(tickerF, text=data, bg=dynamicColor, fg=textcolor, width=12,highlightbackground='black')
        L1.grid(row=row, column=column)
        L1.config(borderwidth=2,relief="solid",font=("VERDANA", 12),wraplength=150)
        MainF.update()

        column +=1
        if column >= 12:
            row += 1
            column = 0
    # row = 0
    # column = 0
    # for i in sorted(stocklist, key=lambda x: x[2], reverse=True):
    #     sy , pr, ch = i
    #     print(i)
    #     data2 = "{}\n{}\n{}%".format(sy, pr , ch)
    #     dc, tc = getDynamicColor(ch)
    #     L2 = tkinter.Label(tickerF, text=data2, bg=dc, fg=tc, width=12,highlightbackground='black')
    #     L2.grid(row=row, column=column)
    #     L2.config(borderwidth=2,relief="solid",font=("VERDANA", 12))
    #     lurl = tickerSymbol.URL+sy
    #     print(lurl)
    #     L2.bind("<Button-1>", lambda url:(webbrowser.open_new(lurl)))
    #     L2.update()
    #     column +=1
    #     if column > 11:
    #         row += 1
    #         column = 0
    # MainF.update()
    # stocklist = []


def getDynamicColor(change):
    try:
        dynamicColor = 'white'
        textcolor = 'black'
        if(float(change)>=3):
            dynamicColor = 'darkgreen'
            textcolor = 'white'
        elif(1<float(change)<3):
            dynamicColor = 'olivedrab'
            textcolor ='white'
        elif(0<float(change)<=1):
            dynamicColor = 'gold'
            textcolor ='black'
        elif(float(change)==0):
            dynamicColor = 'orange'
            textcolor ='black'
        elif(0>float(change)>-1):
            dynamicColor ='rosy brown1'
            textcolor ='black'
        elif(-1>float(change)>-3):
            dynamicColor ='light coral'
            textcolor ='black'
        elif(float(change)<=-3):
            dynamicColor ='IndianRed3'
            textcolor ='black'
    except:
        dynamicColor = 'white'
        textcolor = 'black'

    return (dynamicColor,textcolor)


def deletetuple():
    global tup
    del tup

def getMostActive():
    mostActive = []
    lst = nse_most_active(type="securities",sort="volume")['symbol'].values
    for i in range(0,lst.size):
        mostActive.append(lst[i])
    return mostActive

def getGainLose():
    gainlose = []
    gain = nse_get_top_gainers()['symbol'].values
    lose = nse_get_top_losers()['symbol'].values
    for i in range(0,gain.size):
        gainlose.append(gain[i])
    for j in range(0, lose.size):
        gainlose.append(lose[j])

    return gainlose


def DownloadData():
    OPTIONS = [
        "Day",
        "Hour",
        "Minute"
    ]
    variable = tkinter.StringVar()
    variable.set(OPTIONS[0]) # default value

    w = tkinter.OptionMenu(MainF, variable, *OPTIONS)
    w.grid(row=0, column=11)
    B12 = tkinter.Button(ButtonF, text="Select", command=lambda:show(),font=('Calibri',10), bd=30)
    B12.grid(row=0, column=12,padx = padx, pady = pady)
    def show():
        B13= tkinter.Label(ButtonF, text="Loading...")
        B13.grid(row=1, column=1,padx = padx, pady =pady)
        ButtonF.update()
        Autoscheduler.downloadData(variable.get())
        B13.destroy()


def SellScanner(timeframe):
    B9.configure(fg="Red")
    ButtonF.update()
    sell, sqz = squeeze.Scrapper()
    print('Sell {}'.format(sell))
    return (type(sell))

# def SqueezeScanner():
#     B8.configure(fg="Red")
#     ButtonF.update()
#     sell, sqz = squeeze.Scrapper()
#     return (sqz)

MainF.mainloop()