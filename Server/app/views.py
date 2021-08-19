import sys
sys.path.append('D:/QuantAlgo/quant-app/Server/app')
from .serializers import ImageSerializer
from .models import BackTest, ProfileDB
from strategyBuilding import *
from papertrade import paperTrade, prePaperTrade
from dashboard import onticks
from webbot import Browser
from twilio.rest import Client
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from pandas import json_normalize
from kiteconnect import KiteConnect, KiteTicker
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import talib as ta
import talib
import socketio
import requests
import pandas as pd
import numpy as np
import eventlet
from datetime import datetime, timedelta
import time
import pickle
import os
import logging
import itertools
import asyncio



# import datetime


# import django
# django.setup()


async_mode = None
basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(cors_allowed_origins='*', async_mode=async_mode)


def access_token(api_secret, request_token, kite):
    user = pd.DataFrame()
    try:
        user = kite.generate_session(request_token, api_secret)
        print("Access token ->" + user["access_token"])
        acc_key = user["access_token"]

    except Exception as e:
        print("Authentication failed", str(e))
        raise

    print(user["user_name"], "has successfully signed in.")
    return user


def accesskey():

    user_name = "RK2267"
    password = "Sbi@2023"
    pin = "369741"
    # user_name = "SY5140"
    # password = "Sbi@2021"
    # pin = "489222"
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disble-dev-shm-usage')
    driver = webdriver.Chrome(
        'C:/Users/Dell/Documents/QuantQAlgo/chromedriver')
    # driver = webdriver.Chrome(options=options)
    driver.get("https://kite.trade/connect/login?api_key=pv2830q1vbrhu1eu&v=3")
    time.sleep(1)
    element = driver.find_element_by_id("userid")
    element.send_keys(user_name)
    element = driver.find_element_by_id("password")
    element.send_keys(password)
    element.send_keys(Keys.RETURN)
    time.sleep(1)
    element = driver.find_element_by_id("pin")
    element.send_keys(pin)
    element.send_keys(Keys.RETURN)
    time.sleep(1)
    # element.close()
    url = driver.current_url.split("request_token=")[1].split("&")[0]
    print(url, "new url")
    driver.quit()

    # web = Browser()
    # web.go_to('https://kite.trade/connect/login?api_key=pv2830q1vbrhu1eu&v=3')
    # time.sleep(1)
    # web.type('RK2267', into='User ID', id='userid')
    # web.type('Sbi@2021', into='Password', id='password')
    # web.click('Login')
    # time.sleep(1)
    # web.type('489111', into='PIN', id='pin')
    # web.click('Continue')
    # time.sleep(1)
    # webbot_result_url = web.get_current_url()
    # print(webbot_result_url)
    # url = webbot_result_url
    # url = url.split('request_token=')[1]
    # url = url.split('&')[0]
    # print(url, "url")
    # web.quit()

    my_api_key = "pv2830q1vbrhu1eu"
    kite = KiteConnect(api_key=my_api_key)
    req_key = url
    user_details = access_token(
        "8h662dsfl0ut8sh72g89ni52m60s267c", req_key, kite)
    acc_key = user_details["access_token"]
    print("Access token ->" + acc_key)
    return acc_key


def on_connect(ws, response):
    # dict3 = [895745, 256265, 260105, 264969]
    global dict3
    for i in range(len(dict3)):
        ws.subscribe([dict3[i]])
        ws.set_mode(ws.MODE_FULL, [dict3[i]])
    print("Trading Started....")


def on_close(ws, code, reason):

    # kws.enable_reconnect(reconnect_interval=5, reconnect_tries=50)
    # print("reconnecting...")
    logging.info(
        "Connection closed: {code} - {reason}".format(code=code, reason=reason))
    # ws.stop()


def on_error(ws, code, reason):
    logging.info(
        "123456Connection error: {code} - {reason}".format(code=code, reason=reason))


def on_reconnect(ws, attempts_count):
    logging.info("123456Reconnecting: {}".format(attempts_count))


def on_noreconnect(ws):
    logging.info("123456Reconnect failed.")


def on_ticks(ws, ticks):
    logging.debug("Ticks: {}".format(ticks))
    global nltp, ntime, sltp, stime, bltp, btime, iltp, itime, s, allltp, close, papercapital, slots, le_t, se_t, ltp_f, lxflag, sxflag
    close, allltp, s, nltp, ntime, sltp, stime, bltp, btime, iltp, itime, le_t, se_t, ltp_f, lxflag, sxflag = onticks(ticks, close, allltp, s, nltp, ntime, sltp, stime, bltp, btime, iltp, itime, ltp_f, le_t, se_t, Rmin1, Rhr1, Shr1, Smin1, Mhr1, Mmin1, data1, data2, data3, signal, dict1,
                                                                                                                      dict2, leflag, lxflag, seflag, sxflag, flag4, chtime, lsigflag, ssigflag, sigmin, Rlen, Slen, Mlen, codes_nse, codes_mcx, hlist_nse, hlist_mcx, hlist_mcx_m, hlist_mcx_e, dict3)

    s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}
    invst = papercapital/slots
    global size, trade_name, pnl, entry_val, trade_ltp, trade_tokens
    papercapital, size, trade_name, pnl, entry_val, trade_ltp, trade_tokens = paperTrade(papercapital,
                                                                                         trade_flag, le_t, se_t, dict3, trade_tokens, invst, ltp_f, dict1, trade_name, entry_val, size, slots, pnl, trade_ltp, lxflag, dict2, sxflag)
    # print(trade_name)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    # print("hi")
    kws.connect(threaded=True, disable_ssl_verification=False)
    while True:
        t2 = (datetime.now())
        if count % 120 == 1:
            print(count)
            if(len(nltp) != 0):
                if str(t2.time()) < "15:31:00" and str(t2.time()) >= "09:15:00":
                    niftiltp.append(nltp[0])
                    niftitime.append(ntime)
                    sensexltp.append(sltp[0])
                    sensextime.append(stime)
                    bankltp.append(bltp[0])
                    banktime.append(btime)
                    indialtp.append(iltp[0])
                    indiatime.append(itime)
                # print(nltp, ntime)
                # print(niftiltp)
                sio.emit('niftidata', niftiltp)
                sio.emit('niftitime', niftitime)

                sio.emit('sensexdata', sensexltp)
                sio.emit('sensextime', sensextime)

                sio.emit('bankdata', bankltp)
                sio.emit('banktime', banktime)

                sio.emit('indiadata', indialtp)
                sio.emit('indiatime', indiatime)
        k = list(s)

        sio.emit('paper', round(papercapital))
        sio.emit('size', size)
        sio.emit('tradename',  trade_name)
        sio.emit('pnl', [round(num) for num in pnl])
        sio.emit('entryval', [round(num) for num in entry_val])
        sio.emit('tradeltp', [round(num) for num in trade_ltp])
        sio.emit('tradetoken', trade_tokens)
        if k != []:
            loosersName = []
            loosersltp = []
            for i in range(5):
                loosersName.append(dict1[k[i]])
                loosersltp.append(
                    [round(s[k[i]], 2), allltp[k[i]][0], allltp[k[i]][1]])
            gainersName = []
            gainersltp = []
            g = k[-5:]
            for i in range(5):
                gainersName.append(dict1[g[i]])
                gainersltp.append(
                    [round(s[g[i]], 2), allltp[g[i]][0], allltp[g[i]][1]])
            sio.emit('loosers', loosersName)
            sio.emit('gainers', gainersName)
            sio.emit('loosersltp', loosersltp)
            sio.emit('gainersltp', gainersltp)
        sio.emit('nltp', nltp)
        sio.emit('sltp', sltp)
        sio.emit('bltp', bltp)
        sio.emit('bltp', bltp)
        sio.emit('iltp', iltp)
        sio.emit('iltp', iltp)
        count += 1
        sio.sleep(1)


@sio.event
def connect(sid, environ):
    print('Client connected', sid)
    # sio.start_background_task()
    sio.start_background_task(background_thread)
    # sio.emit('message', 123)


@sio.event
def disconnect(sid):
    print('Client disconnected')


def prevdata(token, acc_key):
    t2 = (datetime.now())
    t1 = (datetime.now())
    if str(t1.time()) < "09:15:00":
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        t1 = str(yesterday)+"+"+"09:15:00"
        t2 = str(yesterday)+"+"+"15:30:00"
    else:
        today = datetime.utcnow().date()
        t1 = str(today)+"+"+"09:15:00"
        if str(t2.time()) < "15:31:00":
            t2 = str(today)+"+"+str(t2.time())
        else:
            t2 = str(today)+"+"+str("15:31:00")
    print(t1)
    print(t2)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(token)+"/15minute?from="+t1+"&to="+t2
    print(url2)
    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    dat2 = res2.json()
    dat2 = dat2["data"]["candles"]

    # print(data2)
    # print(data2)
    timestamp = []
    close1 = []
    for i in range(len(dat2)):
        # print(dat2[i][0])
        d = dat2[i][0].split("T")
        d = d[1].split("+")
        timestamp.append(d[0][:5])
        close1.append(dat2[i][4])
    return timestamp, close1


with open('app/tokens.p', 'rb') as fp:
    dict3 = pickle.load(fp)
with open('app/instruments.p', 'rb') as fp:
    dict1 = pickle.load(fp)


dict3[137] = 256265
dict3[138] = 265
dict3[139] = 260105
dict3[140] = 264969
dict1[256265] = '"NIFTI"'
dict1[265] = '"SENSEX"'
dict1[260105] = '"NIFTI BANK"'
dict1[264969] = '"INDIA VIX"'
# dict1={57648135:'GOLD-21JAN' ,56744455: 'CRUDEOIL21JAN', 57445383 : 'ZINC21JAN'  }
# dict2={57648135 : 0 , 56744455:1 , 2:57445383}
# dict3={0 : 57648135 , 1:56744455, 57445383:2}
# dict3 = {}
# dict1 = {}
# dict3[0] = 256265
# dict3[1] = 265
# dict3[2] = 260105
# dict3[3] = 264969
# dict3[4] = 56407303
# dict3[5] = 56551687
# dict3[6] = 57062151
# dict3[7] = 57059847
# dict1[256265] = '"NIFTY"'
# dict1[265] = '"SENSEX"'
# dict1[260105] = '"NIFTY BANK"'
# dict1[264969] = '"INDIA VIX"'
# dict1[56407303] = '"COTTON"'
# dict1[56551687] = '"CRUDEOIL21JAN"'
# dict1[57062151] = '"ZINC21JAN"'
# dict1[57059847] = '"ALUMINIUM"'


# dict3 = dict(itertools.islice(dict3.items(), 100))
# dict1 = dict(itertools.islice(dict1.items(), 100))
codes_nse = np.load(
    'D:/QuantAlgo/quant-app/Server/app/tokens.p', allow_pickle=True)
codes_mcx = np.load(
    'D:/QuantAlgo/quant-app/Server/app/mcxtokens.p', allow_pickle=True)
print(codes_nse)
print(codes_mcx)
dict2 = {v: k for k, v in dict3.items()}

acc_key = accesskey()
niftiltp = []
niftitime = []
nltp = []
ntime = ''
paperNames = []

sensexltp = []
sensextime = []
sltp = []
stime = ''

bankltp = []
banktime = []
bltp = []
btime = ''

indialtp = []
indiatime = []
iltp = []
itime = ''

close = {}
s = {}
allltp = {}

ltp_f = [0 for i in range(len(dict3))]
le_t = []
se_t = []

keys = list(dict1)
close = {}
s = {}
slots = 4
papercapital = 0
trade_tokens = [0 for i in range(slots)]
trade_flag = [0 for i in range(slots)]
trade_name = ['' for i in range(slots)]
entry_val = [0 for i in range(slots)]
pnl = [0 for i in range(slots)]
size = [0 for i in range(slots)]
trade_ltp = [0 for i in range(slots)]
token1 = 0
token2 = 0
stocknumbers = []

today = datetime.utcnow().date()
# print(today)
yesterday = today - timedelta(days=3)
t1 = str(yesterday)+"+"+"14:15:00"
t2 = str(today)+"+"+"04:30:00"

print(t1)
print(t2)
for i in range(len(dict3)):
    print(i)
    url2 = "https://api.kite.trade/instruments/historical/" + \
        str(dict3[i])+"/15minute?from="+t1+"&to="+t2

    HEADERS = {"X-Kite-Version": "3",
               "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
    res2 = requests.get(url2, headers=HEADERS)
    data2 = res2.json()
    data2 = data2["data"]["candles"]
    close[keys[i]] = data2[-1][4]


niftitime, niftiltp = prevdata(256265, acc_key)
sensextime, sensexltp = prevdata(265, acc_key)
banktime, bankltp = prevdata(260105, acc_key)
indiatime, indialtp = prevdata(264969, acc_key)
kws = KiteTicker("pv2830q1vbrhu1eu", acc_key)
kws.on_ticks = on_ticks
kws.on_close = on_close
kws.on_error = on_error
kws.on_connect = on_connect
kws.on_reconnect = on_reconnect
kws.on_noreconnect = on_noreconnect


data1 = ['' for i in range(len(dict3))]
data2 = ['' for i in range(len(dict3))]
data3 = ['' for i in range(len(dict3))]
leflag = [False for i in range(len(dict3))]
seflag = [False for i in range(len(dict3))]
lxflag = [True for i in range(len(dict3))]
sxflag = [True for i in range(len(dict3))]
signal = ['' for i in range(len(dict3))]
flag4 = [1 for i in range(len(dict3))]
sigmin = [0 for i in range(len(dict3))]
lsigflag = [0 for i in range(len(dict3))]
ssigflag = [0 for i in range(len(dict3))]
chtime = 0  # check-time for a signal in minutes
Rlen = 15  # RSI time-period : Allowed - 15,30,60(in minutes)
Slen = 15  # SuperTrend time-period : Allowed - 15,30,60(in minutes)
Mlen = 15  # MACD time-period : Allowed - 15,30,60(in minutes)

hlist_nse = ['2021-01-26', '2021-03-11', '2021-03-29', '2021-04-02', '2021-04-14', '2021-04-21', '2021-05-13',
             '2021-07-21', '2021-08-19', '2021-09-10', '2021-10-15', '2021-11-04', '2021-11-05', '2021-11-19']
hlist_mcx = ['2021-01-01', '2021-03-11', '2021-03-29', '2021-04-02', '2021-04-14',
             '2021-04-21', '2021-05-25', '2021-11-04', '2021-11-05', '2021-11-30']
hlist_mcx_m = ['o', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']
hlist_mcx_e = ['c', 'o', 'o', 'c', 'o', 'o', 'o', 'o', 'o']

Rhr1 = ['' for i in range(len(dict3))]
Rmin1 = ['' for i in range(len(dict3))]
Shr1 = ['' for i in range(len(dict3))]
Smin1 = ['' for i in range(len(dict3))]
Mhr1 = ['' for i in range(len(dict3))]
Mmin1 = ['' for i in range(len(dict3))]


@api_view(['GET', 'POST'])
def papertrade(request):
    global papercapital, stocknumbers, size, trade_name, pnl, entry_val, trade_ltp, trade_tokens, dict3, data1, data2, data3, Rhr1, Rmin1, Shr1, Smin1, Mhr1, Mmin1, Rlen, Slen, Mlen
    print(request.data, "data")
    papercapital = 0
    papercapital = request.data['capital']
    stocknames = request.data['Stocks']

    data1, data2, data3, Rhr1, Rmin1, Shr1, Smin1, Mhr1, Mmin1 = prePaperTrade(
        dict3, data1, data2, data3, Rhr1, Rmin1, Shr1, Smin1, Mhr1, Mmin1, Rlen, acc_key, Slen, Mlen)
    stocknumbers = []
    for i in le_t:
        paperNames.append(dict1[dict3[i]])

    for i in stocknames:
        if type(i) is list:
            for j in i:
                stocknumbers.append(list(dict1.keys())[
                                    list(dict1.values()).index(j)])
        else:
            stocknumbers.append(list(dict1.keys())[
                                list(dict1.values()).index(i)])
    print(stocknumbers, "stocknumbers")

    print(papercapital, "feuh")
    sio.emit('paper', paperNames)

    return Response({"message": papercapital, "Names": paperNames})


@api_view(['GET', 'POST'])
def livetrade(request):
    global papercapital
    print(request.data, "data")
    papercapital = 0
    papercapital = request.data['capital']
    stocknames = request.data['Stocks']
    global stocknumbers
    stocknumbers = []
    global slots
    slots = int(request.data['slot'])
    for i in stocknames:
        if type(i) is list:
            for j in i:
                stocknumbers.append(list(dict1.keys())[
                                    list(dict1.values()).index(j)])
        else:
            stocknumbers.append(list(dict1.keys())[
                                list(dict1.values()).index(i)])
    print(stocknumbers, "stocknumbers")

    print(papercapital, "feuh")
    sio.emit('paper', paperNames)

    return Response({"message": papercapital, "Names": paperNames})


@api_view(['GET', 'POST'])
def signup(request):
    user = User.objects.create_user(username=request.data['email'], first_name=request.data['firstName'],
                                    last_name=request.data['lastName'], password=request.data['password'])
    ProfileDB.objects.create(username=user)
    # to_date=datetime(2015, 10, 9, 23, 55, 59, 342380))
    print(User.objects.all())
    return Response({"sucessful": 1})


@ api_view(['GET', 'POST'])
def profile(request):
    # print(request.data,"request")
    u = User.objects.get(id=request.data['user'])
    p=ProfileDB.objects.get(username=u)
    # print(u.id, "u")
    # global email, firstname, lastname, id1, datejoined
    datejoined = u.date_joined.strftime("%m/%d/%Y")
    email = u.username
    firstname = u.first_name
    lastname = u.last_name
    phone=str(p.phonenumber)
    # address=str(p.address)
    # print(p.address)
    country=p.country
    state=p.state
    description=p.description
    id1 = u.id
    pro = {'email': email, 'firstname': firstname,
           'lastname': lastname, 'id': id1, 'datejoined': datejoined,'phonenumber':phone,'country':country,'state':state,'description':description,'address':p.address}
    # print(pro)
    return Response(pro)


@ api_view(['GET', 'POST'])
def profileUpdate(request):
    print(request.data)
    u = User.objects.get(id=request.data['user'])
    # blog = ProfileDB.objects.get(username=u)
    ProfileDB.objects.filter(username=u).update(phonenumber=request.data['values']['phone'],country = request.data['values']['country'],address = request.data['values']['address'], state = request.data['values']['state'],description = request.data['values']['description'])
    # print(blog)
    # blog.phonenumber= request.data['values']['phone']
    # blog.country = request.data['values']['country']
    # blog.address = request.data['values']['address']
    # blog.state = request.data['values']['state']
    # blog.description = request.data['values']['description']
    # blog.save()
    return Response({"sucessful": 1})


@ api_view(['GET', 'POST'])
def strategyBuilding(request):
    print(request.data)
    his_months = int(request.data['tradeperiod'])
    his_time = 30*his_months
    StrategyBuilding(dict1, dict2, dict3, his_time, acc_key)
    return Response({"sucessful": 1})


# email = ''
# firstname = ''
# lastname = ''
# datejoined = ''
# id1 = ''

address=''
@ api_view(['GET', 'POST'])
def signin(request):
    # print(request, "request")
    user = authenticate(
        username=request.data['email'], password=request.data['password'])
    # print(user)
    u = User.objects.get(username=request.data['email'])

    datejoined = u.date_joined.strftime("%m/%d/%Y")

    email = u.username
    firstname = u.first_name
    lastname = u.last_name
    id1 = u.id
    # datejoined = u.date_joined
    if user is not None:
        print("yes")
        return Response({"sucessful": True, 'id': id1,'firstname':firstname})
    else:
        print("No")
        return Response({"sucessful": False})


class ImageCreateView(CreateAPIView):
    queryset = BackTest.objects.all()
    serializer_class = ImageSerializer

    def __init__(self):
        # self.df2_nifty_CE = pd.read_csv(
        #     "C:/Users/Dell/Desktop/quant-app/Server/app//acc_15min.csv")
        self.df1 = pd.read_csv(
            "app//SBIN_15_min.csv")
        self.lot_size = 0
        self.request = ""

    def post(self, request):
        self.request = request
        x = {"hello": request.data["symbol"]}
        print(self.request.data["symbol"], "helllooo")
        # self.lot_size = int(self.request.data["Quantity"])
        start_date = self.request.data["from_date"]
        date1 = start_date.split("T")
        start_date = date1[0]+" "+date1[1]
        to_date = self.request.data["to_date"]
        date2 = to_date.split("T")
        to_date = date2[0]+" "+date2[1]
        # start_date = "2019-01-06 15:15:00"
        # end_date = "2020-10-30 15:30:00"

        self.df1['PLUS_DI'] = ta.PLUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)
        self.df1['MINUS_DI'] = ta.MINUS_DI(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)

        self.df1['ADX'] = ta.ADX(np.asarray(self.df1['high'], dtype='f8'), np.asarray(
            self.df1['low'], dtype='f8'), np.asarray(self.df1['close'], dtype='f8'), timeperiod=14)
        self.df1['macd'], self.df1['signal'], self.df1['macdhist'] = ta.MACD(np.asarray(
            self.df1['close'], dtype='f8'), fastperiod=12, slowperiod=26, signalperiod=9)
        self.df1['EMA_S'] = ta.EMA(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=8)
        self.df1['EMA_L'] = ta.EMA(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=21)
        self.df1['UPPERBAND'], self.df1['MIDDLEBAND'], self.df1['LOWERBAND'] = ta.BBANDS(np.asarray(
            self.df1['close'], dtype='f8'), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

        # some variables.
        no_of_trades = []
        order = []
        buy_sell = []
        Entry_price = []
        Exit_price = []
        profit = []
        mtm = []

        lot_size = int(self.request.data["Quantity"])
        pro = 0
        trade = 0
        buying_price = 0
        selling_price = 0

        len_df1 = self.df1["close"].size
        buy_flag = False
        sell_flag = True
        buy_flag1 = False

        self.df1["Position"] = 0
        print(self.df1)
        stoploss = 0
        target = 0

        self.df1["ADX_COMP"] = 0
        self.df1["EMA_COMP"] = 0
        self.df1["MACD_COMP"] = 0
        # self.df1.dropna(inplace = True)
        for i in range(len_df1):
            if (i > 1) and (self.df1['PLUS_DI'].iloc[i] > self.df1['MINUS_DI'].iloc[i]) and (self.df1['ADX'].iloc[i] > self.df1['MINUS_DI'].iloc[i]) and (self.df1['ADX'].iloc[i-1] < self.df1['MINUS_DI'].iloc[i-1]):
                self.df1.loc[i, "ADX_COMP"] = 1
            else:
                self.df1.loc[i, "ADX_COMP"] = 0

            if (i > 1) and (self.df1['EMA_S'].iloc[i] > self.df1['EMA_L'].iloc[i]) and (self.df1['EMA_S'].iloc[i-1] < self.df1['EMA_L'].iloc[i-1]):
                self.df1.loc[i, "EMA_COMP"] = 1
            else:
                self.df1.loc[i, "EMA_COMP"] = 0

            if (i > 1) and (self.df1['macd'].iloc[i] > self.df1['signal'].iloc[i]) and (self.df1['macd'].iloc[i-1] < self.df1['signal'].iloc[i-1]):
                self.df1.loc[i, "MACD_COMP"] = 1
            else:
                self.df1.loc[i, "MACD_COMP"] = 0

        for x in range(len_df1):
            pro = 0

            if((self.df1['PLUS_DI'].iloc[x] > self.df1['MINUS_DI'].iloc[x]) and (self.df1['ADX'].iloc[x] > self.df1['MINUS_DI'].iloc[x]) and (self.df1['ADX'].iloc[x-1] < self.df1['MINUS_DI'].iloc[x-1]) or (1 in self.df1['ADX_COMP'].iloc[x-7:x].values)) and ((self.df1['macd'].iloc[x] > self.df1['signal'].iloc[x]) and (self.df1['macd'].iloc[x-1] < self.df1['signal'].iloc[x-1]) or (1 in self.df1['MACD_COMP'].iloc[x-5:x].values)) and ((self.df1['EMA_S'].iloc[x] > self.df1['EMA_L'].iloc[x]) and (self.df1['EMA_S'].iloc[x-1] < self.df1['EMA_L'].iloc[x-1]) or (1 in self.df1['EMA_COMP'].iloc[x-5:x].values)) and (not buy_flag):
                trade += 1
                buying_price = self.df1['close'].iloc[x]

                order.append(-1)
                buy_sell.append("Buy")
                Entry_price.append(buying_price)
                Exit_price.append("")
                mtm.append("Position Taken")
                self.df1["Position"][x+1] = 1
                # print(self.df1["Position"][x+1])

                buy_flag1 = True
                buy_flag = True
                sell_flag = False

            elif(((self.df1['UPPERBAND'].iloc[x-1] < self.df1['close'].iloc[x-1]) and (self.df1['UPPERBAND'].iloc[x] > self.df1['close'].iloc[x]) and (self.df1['ADX'].iloc[x] > self.df1['PLUS_DI'].iloc[x])) or (self.df1['close'].iloc[x] < (0.99 * buying_price))) and (not sell_flag):
                trade += 1
                selling_price = self.df1['close'].iloc[x]
                pro = selling_price - buying_price

                order.append(1)
                buy_sell.append("Sell")
                Entry_price.append("")
                Exit_price.append(selling_price)
                mtm.append("Position closed")

                if buy_flag1 == True:
                    buy_flag1 = False
                buy_flag = False
                sell_flag = True

            else:
                if (buy_flag == True):
                    yy = (self.df1['close'].iloc[x] - buying_price) * lot_size
                else:
                    yy = "0"

                order.append(0)
                buy_sell.append("No Trade")
                Entry_price.append("")
                Exit_price.append("")
                mtm.append(yy)

                if buy_flag1 == True:
                    self.df1["Position"][x] = 1
                    # print(self.df1["Position"][x])

            no_of_trades.append(trade)
            profit.append(pro)
        initial_capital = int(self.request.data["Initial_Capital"])
        self.df1['Returns'] = np.log(
            self.df1["close"] / self.df1["close"].shift(1))
        self.df1['Strategy_Return'] = self.df1['Position'].shift(
            1) * self.df1['Returns']
        self.df1["placed_order"] = order
        self.df1["buy_sell"] = buy_sell
        self.df1["Entry"] = Entry_price
        self.df1["Exit"] = Exit_price
        self.df1['profit'] = profit
        self.df1['profit'] = (self.df1['profit']) * lot_size
        self.df1["mtm"] = mtm
        self.df1["cost"] = (self.df1["placed_order"].multiply(
            self.df1["close"])) * lot_size
        self.df1["Account"] = initial_capital + self.df1["cost"].cumsum()
        self.df1["Trades"] = no_of_trades

        self.df1.set_index('Date', inplace=True)

        risk_free_rate = 0.061/252
        sharpe = np.sqrt(252)*(np.mean(self.df1.Strategy_Return) -
                               (risk_free_rate))/np.std(self.df1.Strategy_Return)

        cumulative_returns = self.df1.Strategy_Return.cumsum().iloc[-1]
        period_in_days = len(self.df1.Strategy_Return)
        CAGR = 100*((cumulative_returns+1)**(252.0/period_in_days)-1)

        self.df1.dropna(inplace=True)
        cum_ret = self.df1.Strategy_Return.cumsum()

        peak = (np.maximum.accumulate(cum_ret) - cum_ret).idxmax()
        trough = cum_ret[:peak].idxmax()
        drawdown = (cum_ret[trough] - cum_ret[peak]) * 100

        buy_records = self.df1[self.df1["buy_sell"] == "Buy"]
        sell_records = self.df1[self.df1["buy_sell"] == "Sell"]

        trade_details = pd.DataFrame(0, index=range(len(buy_records)),
                                     columns=["Entry", "Date",
                                              "Price", "Exit",
                                              "ExDate", "ExPrice"])

        trade_details["Entry"] = buy_records["buy_sell"].values
        trade_details["Date"] = buy_records.index.values  # buy date
        trade_details["Price"] = buy_records["close"].values  # buy price
        trade_details["Exit"] = sell_records["buy_sell"].values
        trade_details["ExDate"] = sell_records.index.values  # sell date
        trade_details["ExPrice"] = sell_records["close"].values  # sell price
        trade_details['% Change'] = (
            trade_details['ExPrice'] / trade_details['Price']) - 1
        trade_details['Profit'] = trade_details['ExPrice'] - \
            trade_details['Price']
        trade_details['% Profit'] = (
            trade_details['ExPrice'] / trade_details['Price']) - 1
        trade_details['Position value'] = trade_details['Price']
        trade_details['Cumm Profit'] = trade_details['Profit'].cumsum()
        trade_details['MAE'] = 0
        trade_details['MFE'] = 0
        trade_details['Scale In / Scale Out'] = 0

        profit = trade_details[trade_details["Profit"] >= 1]
        loss = trade_details[trade_details["Profit"] <= -1]
        trade = trade_details.to_dict()
        print(trade_details)
        output = {}
        output["Trade start date"] = self.df1.index[-1]
        output['Trade end date'] = self.df1.index[0]
        output['Initial_Capital'] = self.df1["Account"].iloc[0]
        output['Ending_Capital'] = self.df1["Account"].iloc[-1]
        output['Total no trades'] = len(buy_records)
        output['Positive_trades'] = len(self.df1[self.df1["profit"] >= 1])
        output['Negative_trades'] = len(self.df1[self.df1["profit"] <= -1])
        output['Total_profit'] = self.df1[self.df1["profit"] >= 1]["profit"].sum()
        output['Total_loss'] = self.df1[self.df1["profit"] <= -1]["profit"].sum()
        output['Net Profit'] = self.df1["Account"].iloc[-1] - \
            self.df1["Account"].iloc[0]
        output['Net Profit (%)'] = (
            (self.df1["Account"].iloc[-1] / self.df1["Account"].iloc[0]) - 1) * 100
        output['Avg. Profit / Loss'] = np.mean(
            profit["Profit"].values) / np.mean(loss["Profit"].values)
        output['Sharpe ratio'] = sharpe
        output['CAGR (%)'] = CAGR
        output['Maximum Drawdown (%)'] = drawdown
        output['CAGR / MDD (%)'] = CAGR / drawdown
        print(output)
        return Response({"output": output, "trade": trade})
