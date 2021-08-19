import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def signal_message(msg):
    account_sid = 'AC02a3fcc5d16857c0b417d5f854a007e9'
    auth_token = '14e061a30b23cb9821d11365496fffc2'
    client1 = Client(account_sid, auth_token)

    message = client1.messages.create(
        from_='+15094040805',
        body=msg,
        to='+919677480457'
    )


def EMA(df, base, target, period, alpha=False):

    con = pd.concat([df[:period][base].rolling(
        window=period).mean(), df[period:][base]])

    if (alpha == True):
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df


def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):

    atr = 'ATR_' + str(period)
    df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
    df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
    df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())
    df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)
    df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)
    EMA(df, 'TR', atr, period, alpha=True)

    return df


def SuperTrend(df, period, multiplier, ohlc=['Open', 'High', 'Low', 'Close']):
    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST_' + str(period) + '_' + str(multiplier)
    stx = 'STX_' + str(period) + '_' + str(multiplier)

    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i -
                                                                                                    1] or df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i -
                                                                                                    1] or df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else df['final_lb'].iat[i - 1]

    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] <= df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= df['final_lb'].iat[i] else \
            df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i -
                                                                             1] and df[ohlc[3]].iat[i] < df['final_lb'].iat[i] else 0.00

    df[stx] = np.where((df[st] > 0.00), np.where(
        (df[ohlc[3]] < df[st]), 'down',  'up'), np.NaN)

    df.drop(['basic_ub', 'basic_lb', 'final_ub',
             'final_lb'], inplace=True, axis=1)

    df.fillna(0, inplace=True)

    return df


def RSI(series, rsi_period):
    chg = series.diff(1)
    gain = chg.mask(chg < 0, 0)
    data = pd.DataFrame()
    data['gain'] = gain
    loss = chg.mask(chg > 0, 0)
    data['loss'] = loss
    avg_gain = data['gain'].mean(axis=0, skipna=True)
    avg_loss = data['loss'].mean(axis=0, skipna=True)
    rs = abs(avg_gain/avg_loss)
    rsi = 100-(100/(1+rs))
    return rsi


def macd(df, m1, m2, s1):
    df.reset_index(level=0, inplace=True)
    df.columns = ['ds', 'y']
    exp1 = df.y.ewm(span=m1, adjust=False).mean()
    exp2 = df.y.ewm(span=m2, adjust=False).mean()
    macd2 = exp1-exp2
    exp3 = macd2.ewm(span=s1, adjust=False).mean()
    return macd2, exp3

def sma(df,period):
    values=df['Close'].to_numpy()
#     print(values)

    value2=values[-period-1:-1]
#     print(value2,len(value2))
    sma = np.mean(values)
    return sma


def indicator(tk, ltp, ohlc, ltp_df, ltp_f, le_t, se_t, Rmin1, Rhr1, Shr1, Smin1, Mhr1, Mmin1, data1, data2, data3, signal, dict1,
              dict2, leflag, lxflag, seflag, sxflag, flag4, chtime, lsigflag, ssigflag, sigmin, Rlen, Slen, Mlen, codes_nse, codes_mcx, hlist_nse, hlist_mcx, hlist_mcx_m, hlist_mcx_e, dict3):
    T2 = datetime.now()
    hr2 = int(T2.hour)
    min2 = int(T2.minute)
    # tk=ticks[i]['instrument_token']
    code = dict1[tk]
    loop = dict2[tk]
    ltp_f[loop] = ltp
    day = T2.weekday()
    T4 = str(T2).split(' ')[0]
    flag2 = 1
    if(True):
        if(Rlen == 60):
            if(Rhr1[loop]+1 == hr2 and Rmin1[loop] >= 15):
                print("RSI of "+str(code)+" updated at "+str(T2))
                data1[loop] = data1[loop].append(ltp_df, ignore_index=True)
                Rhr1[loop] = Rhr1[loop]+1

            elif(Rlen == 30):
                if(Rmin1[loop] == 15):
                    if(Rhr1[loop] == hr2 and min2 >= 45):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 45
                elif(Rmin1[loop] == 45):
                    if(Rhr1[loop]+1 == hr2 and min2 >= 15):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rhr1[loop] = Rhr1[loop]+1
                        Rmin1[loop] = 15

            elif(Rlen == 15):
                if(Rmin1[loop] == 15):
                    if(Rhr1[loop] == hr2 and min2 >= 30):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 30
                elif(Rmin1[loop] == 30):
                    if(Rhr1[loop] == hr2 and min2 >= 45):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 45
                elif(Rmin1[loop] == 45):
                    if(Rhr1[loop]+1 == hr2 and min2 >= 0 and min2 < 15):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rhr1[loop] = Rhr1[loop]+1
                        Rmin1[loop] = 0
                elif(Rmin1[loop] == 0):
                    if(Rhr1[loop] == hr2 and min2 >= 15):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 15
            elif(Rlen == 10):
                if(Rhr1[loop] == hr2):
                    if(Rmin1[loop]+10 <= min2):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = Rmin1[loop]+10
                else:
                    if(min2 >= 5):
                        print("RSI of "+str(code)+" updated at "+str(T2))
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 5
            elif(Rlen == 5):
                if(Rhr1[loop] == hr2):
                    if(Rmin1[loop]+5 <= min2):
                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = Rmin1[loop]+5
                else:
                    if(min2 >= 0):

                        data1[loop] = data1[loop].append(
                            ltp_df, ignore_index=True)
                        Rmin1[loop] = 0

            close1 = data1[loop][['Close']][-26:-1]
            close1 = close1.append(ltp_df, ignore_index=True)
            close2 = close1['Close']
            # print(close2)
            RSI1 = RSI(close2, 25)
            # print(RSI)
            v1 = RSI1
            close11 = data1[loop]['Close'][-27:-1]
            close12 = data1[loop]['Close'][-28:-2]
            close13 = data1[loop]['Close'][-29:-3]
            close14 = data1[loop]['Close'][-30:-4]
            close15 = data1[loop]['Close'][-31:-5]
            v11 = RSI(close11, 25)
            v12 = RSI(close12, 25)
            v13 = RSI(close13, 25)
            v14 = RSI(close14, 25)
            v15 = RSI(close15, 25)
            if(Mlen == 60):
                if(Mhr1[loop]+1 == hr2 and Mmin1[loop] == min2):
                    print("MACD of "+str(code)+" updated at "+str(T2))
                    data3[loop] = data3[loop].append(ltp_df, ignore_index=True)
                    Mhr1[loop] = Mhr1[loop]+1

            elif(Mlen == 30):
                if(Mmin1[loop] == 15):
                    if(Mhr1[loop] == hr2 and min2 == 45):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = 45
                elif(Mmin1[loop] == 45):
                    if(Mhr1[loop]+1 == hr2 and min2 == 15):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mhr1[loop] = Mhr1[loop]+1
                        Mmin1[loop] = 15

            elif(Mlen == 15):
                if(Mmin1[loop] == 15):
                    if(Mhr1[loop] == hr2 and min2 == 30):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = 30
                elif(Mmin1[loop] == 30):
                    if(Mhr1[loop] == hr2 and min2 == 45):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = 45
                elif(Mmin1[loop] == 45):
                    if(Mhr1[loop]+1 == hr2 and min2 == 0):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mhr1[loop] = Mhr1[loop]+1
                        Mmin1[loop] = 0
                elif(Mmin1[loop] == 0):
                    if(Mhr1[loop] == hr2 and min2 == 15):
                        print("MACD of "+str(code)+" updated at "+str(T2))
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = 15

            elif(Mlen == 5):
                if(Mhr1[loop] == hr2):
                    if(Mmin1[loop]+5 <= min2):
                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = Mmin1[loop]+5
                else:
                    if(min2 >= 0):

                        data3[loop] = data3[loop].append(
                            ltp_df, ignore_index=True)
                        Mmin1[loop] = Mmin1[loop]+5

            dff = data3[loop][['Close']]
            dff = dff.append(ltp_df, ignore_index=True)
            macd3, sig3 = macd(dff, 12, 26, 9)
            vm1 = macd3.iloc[-1]
            vm2 = macd3.iloc[-2]
            vm3 = macd3.iloc[-3]
            vm4 = macd3.iloc[-4]
            vm5 = macd3.iloc[-5]
            vm6 = macd3.iloc[-6]
            vs1 = sig3.iloc[-1]
            vs2 = sig3.iloc[-2]
            vs3 = sig3.iloc[-3]
            vs4 = sig3.iloc[-4]
            vs5 = sig3.iloc[-5]
            vs6 = sig3.iloc[-6]
            v5 = 'No Cross-Over'
            v21 = 0
            v22 = 0
            v23 = 0
            v24 = 0
            v25 = 0
            if vm1 > 0 and vs1 > 0:
                if vm1 > vs1 and vm2 < vs2:
                    v21 = 1
                    v5 = "Cross-Over above line"
            if vm2 > 0 and vs2 > 0:
                if vm2 > vs2 and vm3 < vs3:
                    v22 = 1
                    v5 = "Cross-Over above line"
            if vm3 > 0 and vs3 > 0:
                if vm3 > vs3 and vm4 < vs4:
                    v23 = 1
                    v5 = "Cross-Over above line"
            if vm4 > 0 and vs4 > 0:
                if vm4 > vs4 and vm5 < vs5:
                    v24 = 1
                    v5 = "Cross-Over above line"
            if vm5 > 0 and vs5 > 0:
                if vm5 > vs5 and vm6 < vs6:
                    v25 = 1
                    v5 = "Cross-Over above line"

            v61 = 0
            v62 = 0
            v63 = 0
            v64 = 0
            v65 = 0
            if vm1 < 0 and vs1 < 0:
                if vm1 > vs1 and vm2 < vs2:
                    v61 = 1
                    v5 = "Cross-Over below line"
            if vm2 < 0 and vs2 < 0:
                if vm2 > vs2 and vm3 < vs3:
                    v62 = 1
                    v5 = "Cross-Over below line"
            if vm3 < 0 and vs3 < 0:
                if vm3 > vs3 and vm4 < vs4:
                    v63 = 1
                    v5 = "Cross-Over below line"
            if vm4 < 0 and vs4 < 0:
                if vm4 > vs4 and vm5 < vs5:
                    v64 = 1
                    v5 = "Cross-Over below line"
            if vm5 < 0 and vs5 < 0:
                if vm5 > vs5 and vm6 < vs6:
                    v65 = 1
                    v5 = "Cross-Over below line"

            ohlc2 = {}
            ohlc2['Open'] = ohlc['open']
            ohlc2['High'] = ohlc['high']
            ohlc2['Low'] = ohlc['low']
            ohlc2['Close'] = ohlc['close']
            if(Slen == 60):
                if(Shr1[loop]+1 == hr2 and Smin1[loop] == min2):
                    print("STRD of "+str(code)+" updated at "+str(T2))
                    data2[loop] = data2[loop].append(ohlc2, ignore_index=True)
                    Shr1[loop] = Shr1[loop]+1

            elif(Slen == 30):
                if(Smin1[loop] == 15):
                    if(Shr1[loop] == hr2 and min2 == 45):
                        print("STRD of "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Smin1[loop] = 45
                elif(Smin1[loop] == 45):
                    if(Shr1[loop]+1 == hr2 and min2 == 15):
                        print("STRD of "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Shr1[loop] = Shr1[loop]+1
                        Smin1[loop] = 15

            elif(Slen == 15):
                if(Smin1[loop] == 15):
                    if(Shr1[loop] == hr2 and min2 == 30):
                        print("STRDof "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Smin1[loop] = 30
                elif(Smin1[loop] == 30):
                    if(Shr1[loop] == hr2 and min2 == 45):
                        print("STRD of "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Smin1[loop] = 45
                elif(Smin1[loop] == 45):
                    if(Shr1[loop]+1 == hr2 and min2 == 0):
                        print("STRD of "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Shr1[loop] = Shr1[loop]+1
                        Smin1[loop] = 0
                elif(Smin1[loop] == 0):
                    if(Shr1[loop] == hr2 and min2 == 15):
                        print("STRD of "+str(code)+" updated at "+str(T2))
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Smin1[loop] = 15

            elif(Slen == 5):
                if(Shr1[loop] == hr2):
                    if(Smin1[loop]+5 <= min2):
                        data2[loop] = data2[loop].append(
                            ohlc2, ignore_index=True)
                        Smin1[loop] = Smin1[loop]+5
                else:
                    if(min2 >= 0):

                        data3[loop] = data3[loop].append(
                            ohlc2, ignore_index=True)
                        Mmin1[loop] = Mmin1[loop]+5

            strd = data2[loop].iloc[-24:]
            strd = strd.append(ohlc2, ignore_index=True)
            ans2 = SuperTrend(strd, 15, 1.5)
            v3 = ans2['STX_15_1.5'].iloc[-1]
            v4 = ans2['ST_15_1.5'].iloc[-1]
            v31 = ans2['STX_15_1.5'].iloc[-2]
            v32 = ans2['STX_15_1.5'].iloc[-3]
            v33 = ans2['STX_15_1.5'].iloc[-4]
            v34 = ans2['STX_15_1.5'].iloc[-5]
            v35 = ans2['STX_15_1.5'].iloc[-6]
            val = ''
            if (v3 == "up" and v1 > 55 and (v21 == 1 or v22 == 1 or v23 == 1 or v24 == 1 or v25 == 1) and (not leflag[loop]) and (not seflag[loop])) or lsigflag[loop] == 1:
                val = 'In-LE-For-A-While'
                if((v31 == "down" or v32 == "down" or v33 == "down" or v34 == "down" or v35 == "down") and (v11 <= 55 or v12 <= 55 or v13 <= 55 or v14 <= 55 or v15 <= 55)) or lsigflag[loop] == 1:
                    print("check-1", v3, v1, v5,
                          ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                    if lsigflag[loop] == 0:
                        sigmin[loop] = int(min2)
                        lsigflag[loop] = 1
                        val = "Might-Give-A-LE-Signal"
                        print("LE-flag value at might= ",
                              lsigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                    elif lsigflag[loop] == 1 and sigmin[loop]+chtime <= int(min2):
                        print("check-2", v3, v1, v5,
                              ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                        if (v3 == "up" and v1 > 55 and (v21 == 1 or v22 == 1 or v23 == 1 or v24 == 1 or v25 == 1) and (not leflag[loop]) and (not seflag[loop])):
                            val = "LE"
                            message1 = "signal detected at " + \
                                str(T2)+"\n Long Entry for " + \
                                code+" at INR "+str(ltp)
                            signal_message(message1)
                            leflag[loop] = True
                            lxflag[loop] = False
                            le_t.append(loop)
                            lsigflag[loop] = 0
                            sigmin[loop] = 0
                        else:
                            val = "LE-failed"
                            lsigflag[loop] = 0
                            sigmin[loop] = 0
                    else:
                        val = "Waiting-for-LE"
                        print("LE-flag value at wait= ",
                              lsigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)

            elif v3 == "down" and (not lxflag[loop]):
                val = "LX"
                message1 = "signal detected at " + \
                    str(T2)+"\n Long Exit for "+code+" at INR "+str(ltp)
                signal_message(message1)
                leflag[loop] = False
                lxflag[loop] = True
            elif (v3 == "down" and v1 < 45 and (v61 == 1 or v62 == 1 or v63 == 1 or v64 == 1 or v65 == 1) and (not leflag[loop]) and (not seflag[loop])) or ssigflag[loop] == 1:
                val = 'In-SE-For-A-While'
                if ((v31 == "up" or v32 == "up" or v33 == "up" or v34 == "up" or v35 == "up") and (v11 >= 45 or v12 >= 45 or v13 >= 45 or v14 >= 45 or v15 >= 45)) or ssigflag[loop] == 1:
                    print("check-1", v3, v1, v5,
                          ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                    if ssigflag[loop] == 0:
                        sigmin[loop] = int(min2)
                        ssigflag[loop] = 1
                        val = "Might-Give-A-SE-Signal"
                        print("SE-flag value at might= ",
                              ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                    if ssigflag[loop] == 1 and sigmin[loop]+chtime <= int(min2):
                        print("check-2", v3, v1, v5,
                              ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
                        if (v3 == "down" and v1 < 45 and (v61 == 1 or v62 == 1 or v63 == 1 or v64 == 1 or v65 == 1) and (not leflag[loop]) and (not seflag[loop])):
                            val = "SE"
                            message1 = "signal detected at " + \
                                str(T2)+"\n Short Entry for " + \
                                code+" at INR "+str(ltp)
                            signal_message(message1)
                            seflag[loop] = True
                            sxflag[loop] = False
                            se_t.append(loop)
                            ssigflag[loop] = 0
                            sigmin[loop] = 0
                        else:
                            val = "SE-Failed"
                            ssigflag[loop] = 0
                            sigmin[loop] = 0
                    else:
                        val = "Waiting-for-SE"
                        print("SE-flag value at wait= ",
                              ssigflag[loop], sigmin[loop], dict1[dict3[loop]], T2)
            elif v3 == "up" and (not sxflag[loop]):
                val = "SX"
                message1 = "signal detected at " + \
                    str(T2)+"\n Short Exit for "+code+" at INR "+str(ltp)
                signal_message(message1)
                seflag[loop] = False
                sxflag[loop] = True
            else:
                if (leflag[loop] == True):
                    val = "buy already"

                elif (seflag[loop] == True):
                    val = "short already"
                else:
                    val = "NO-TRADE"

            if(val != signal[loop] and val != "NO-TRADE") or (val == "LE") or (val == "SE"):
                signal[loop] = val
                file1 = open("MACD_Added_LiveTest_Results.txt", "a+")
                res = str(code)+" "+str(val)+" "+"LTP="+str(ltp)+" "+" RSI="+str(v1)+" " + \
                    " SUPERTEND="+str(v4)+" "+str(v3)+" " + \
                    "MACD= "+v5+" TIMESTAMP="+str(T2)+"\n"
                print(res)
                file1.write(res)
                file1.close()
            for j in range(len(dict3)):
                if lsigflag[j] == 1:
                    if sigmin[j]+chtime < int(min2):
                        print(
                            "Flag of "+str(dict1[dict3[j]])+" is made 0 ", sigmin[j], min2)
                        lsigflag[j] = 0
                        sigmin[j] = 0
                if ssigflag[j] == 1:
                    if sigmin[j]+chtime < int(min2):
                        print(
                            "Flag of "+str(dict1[dict3[j]])+" is made 0", sigmin[j], min2)
                        ssigflag[j] = 0
                        sigmin[j] = 0
    return le_t, se_t, ltp_f, lxflag, sxflag
