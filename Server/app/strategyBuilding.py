# his_months=3
# his_time= 30*his_months

# data1=[['' for i in range(int(his_time/60))] for i in range(len(dict3))]
# data2=[[pd.DataFrame() for i in range(len(dict3))]]
# data3=['' for i in range(len(dict3))]
# data4=['' for i in range(len(dict3))]
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from indicator import sma


def StrategyBuilding(dict1, dict2, dict3, his_time, acc_key):
    data1 = [['' for i in range(int(his_time/60))] for i in range(len(dict3))]
    data2 = [[pd.DataFrame() for i in range(len(dict3))]]
    data3 = ['' for i in range(len(dict3))]
    data4 = ['' for i in range(len(dict3))]
    for i in range(len(dict3)):
        print(i)
        for j in range(int(his_time/60)):
            if(i != 0):
                t2 = (datetime.now() - timedelta(days=j*60))
            else:
                t2 = (datetime.now() - timedelta(days=j*60+1))
            t1 = (datetime.now() - timedelta(days=(j+1)*60))
            print(t1)
            print(t2)
            t1 = str(t1)
            t2 = str(t2)
            t1 = t1.split(" ")
            t3 = t1[1].split(':')
            t3[0] = '9'
            t3[1] = '00'
            t3 = t3[0]+':'+t3[1]+':'+t3[2]
            t1 = t1[0]+"+"+t3
            t2 = t2.split(" ")
            t3 = t2[1].split(':')
            t3[0] = '15'
            t3[1] = '30'
            t3 = t3[0]+':'+t3[1]+':'+t3[2]
            t2 = t2[0]+"+"+t3

            url1 = "https://api.kite.trade/instruments/historical/" + \
                str(dict3[i])+"/minute?from="+t1+"&to="+t2
            # print(url1)
            HEADERS = {"X-Kite-Version": "3",
                       "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
            res1 = requests.get(url1, headers=HEADERS)
            # print(res1.json())
            data1[i][j] = res1.json()
        #     print(data1[i][j])
            data1[i][j] = data1[i][j]["data"]["candles"]
            data1[i][j] = pd.DataFrame(data1[i][j])
            data1[i][j] = data1[i][j].rename(
                columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
            pd.set_option("display.max_rows", None,
                          "display.max_columns", None)
            # print((data1[i][j]).head())
            # print((data1[i][j]).tail())
    indicator_index = [3]
    period_sma = 14
    cd_interval = 15

    rs_t = ['' for i in range(len(dict3))]
    rs_o = [0 for i in range(len(dict3))]
    rs_h = [0 for i in range(len(dict3))]
    rs_l = [0 for i in range(len(dict3))]
    rs_c = [0 for i in range(len(dict3))]
    pnl = [0 for i in range(len(dict3))]
    entry_val = [0 for i in range(len(dict3))]
    quant = [1000 for i in range(len(dict3))]
    le_flag = [False for i in range(len(dict3))]

    rs_data2 = [pd.DataFrame() for i in range(len(dict3))]

    for i in range(len(data1)):
        l = len(data1[i])
        for j in range(l):
            print("j=", j)
            for k in range(len(data1[i][l-1-j])):
                if(k == 0):
                    ltp_prev = 0
                else:
                    ltp_prev = float(data1[i][l-1-j]['Close'].iloc[k-1])
                ltp = float(data1[i][l-1-j]['Close'].iloc[k])
                ltp_df = {}
                ltp_df['Close'] = ltp
                tk = dict3[i]
                code = dict1[tk]

                TR1 = data1[i][l-1-j]['Time'].iloc[k]
                TR2 = TR1.split('T')[1]

                dt = str(TR1.split('T')[0])

                v_hr = int(TR2.split(':')[0])
                v_min = int(TR2.split(':')[1])
    #             if(v_hr==9 and v_min==15):
    #                 rsd_o[i]=data1[i][l-1-j]['Open'].iloc[k]
    #                 dayflag[i]=True

                if(cd_interval == 15):
                    if(v_min % 15 == 0):
                        rs_t[i] = data1[i][l-1-j]['Time'].iloc[k]
                        rs_o[i] = data1[i][l-1-j]['Open'].iloc[k]
                        rs_h[i] = data1[i][l-1-j]['High'].iloc[k]
                        rs_l[i] = data1[i][l-1-j]['Low'].iloc[k]

                    if(v_min % 15 >= 1 and v_min % 15 <= 14):
                        if(data1[i][l-1-j]['High'].iloc[k] > rs_h[i]):
                            rs_h[i] = data1[i][l-1-j]['High'].iloc[k]
                        if(data1[i][l-1-j]['Low'].iloc[k] < rs_l[i]):
                            rs_l[i] = data1[i][l-1-j]['Low'].iloc[k]

                    if(v_min % 15 == 14):
                        rs_c[i] = data1[i][l-1-j]['Close'].iloc[k]
                        ohlc2 = {}
                        ohlc2['Time'] = str(rs_t[i])
                        ohlc2['Open'] = rs_o[i]
                        ohlc2['High'] = rs_h[i]
                        ohlc2['Low'] = rs_l[i]
                        ohlc2['Close'] = rs_c[i]
                        rs_data2[i] = rs_data2[i].append(
                            ohlc2, ignore_index=True)
    #                     print(rs_data2[i])

                        switcher = {
                            1: "RSI",
                            2: "February",
                            3: sma(rs_data2[i], period_sma)
                        }

                        for p in indicator_index:
                            sma_val = switcher.get(p, "Invalid month")
    #                         print(sma_val,ltp)

                    if(len(rs_data2[i]) > 15):
                        #                     print(sma_val,ltp)
                        # SMA isabove Close
                        if(sma_val > ltp) and le_flag[i] == False:
                            print("entered at", TR2, ltp)
                            entry_val[i] = ltp
                            tg1 = ltp*(1.02)  # TARGET = 2%
                            sl1 = ltp*(0.99)  # STOPLOSS = 1%
                            le_flag[i] = True
                        if(le_flag[i] == True):
                            if(ltp > tg1):
                                le_flag[i] = False
                                profit = (ltp-entry_val[i])*quant[i]
                                pnl[i] = pnl[i]+profit
                                print("exit by target at",
                                      TR2, ltp, profit, pnl[i])
                            if(ltp < sl1):
                                le_flag[i] = False
                                loss = (entry_val[i]-ltp)*quant[i]
                                pnl[i] = pnl[i]-loss
                                print("exit by stoploss at",
                                      TR2, ltp, loss, pnl[i])
