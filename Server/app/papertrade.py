import requests
from datetime import datetime, timedelta
import pandas as pd


def prePaperTrade(dict3, data1, data2, data3, Rhr1, Rmin1, Shr1, Smin1, Mhr1, Mmin1, Rlen, acc_key,Slen,Mlen):
    for i in range(len(dict3)):

        t2 = (datetime.now())
        t1 = (datetime.now() - timedelta(days=10))
        # print(t1)
        t1 = str(t1)
        t2 = str(t2)
        t1 = t1.split(" ")
        t3 = t1[1].split(':')
        t3[0] = '09'
        t3[1] = '15'
        t3 = t3[0]+':'+t3[1]+':'+t3[2]
        t1 = t1[0]+"+"+t3
        t2 = t2.split(" ")
        t2 = t2[0]+"+"+t2[1]
        url1 = "https://api.kite.trade/instruments/historical/" + \
            str(dict3[i])+"/" + str(Rlen)+"minute?from="+t1+"&to="+t2
        print(url1)
        HEADERS = {"X-Kite-Version": "3",
                   "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}
        res1 = requests.get(url1, headers=HEADERS)
        data1[i] = res1.json()
        data1[i] = data1[i]["data"]["candles"]
        data1[i] = pd.DataFrame(data1[i])
        data1[i] = data1[i].rename(
            columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        t2 = (datetime.now())
        t1 = (datetime.now() - timedelta(days=10))
        # print(t1)
        t1 = str(t1)
        t2 = str(t2)
        t1 = t1.split(" ")
        t3 = t1[1].split(':')
        t3[0] = '09'
        t3[1] = '15'
        t3 = t3[0]+':'+t3[1]+':'+t3[2]
        t1 = t1[0]+"+"+t3
        t2 = t2.split(" ")
        t2 = t2[0]+"+"+t2[1]
        # print(t1)
        # print(t2)
        url2 = "https://api.kite.trade/instruments/historical/" + \
            str(dict3[i])+"/" + str(Slen)+"minute?from="+t1+"&to="+t2
        print(url2)
        HEADERS = {"X-Kite-Version": "3",
                   "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}

        res2 = requests.get(url2, headers=HEADERS)
        data2[i] = res2.json()
        data2[i] = data2[i]["data"]["candles"]
        data2[i] = pd.DataFrame(data2[i])
        data2[i] = data2[i].rename(
            columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
        pd.set_option("display.max_rows", None, "display.max_columns", None)

        t2 = (datetime.now())
        t1 = (datetime.now() - timedelta(days=10))
        print(t1)
        t1 = str(t1)
        t2 = str(t2)
        t1 = t1.split(" ")
        t3 = t1[1].split(':')
        t3[0] = '09'
        t3[1] = '15'
        t3 = t3[0]+':'+t3[1]+':'+t3[2]
        t1 = t1[0]+"+"+t3
        t2 = t2.split(" ")
        t2 = t2[0]+"+"+t2[1]
        url2 = "https://api.kite.trade/instruments/historical/" + \
            str(dict3[i])+"/" + str(Mlen)+"minute?from="+t1+"&to="+t2
        print(url2)
        HEADERS = {"X-Kite-Version": "3",
                   "Authorization": "token pv2830q1vbrhu1eu:"+acc_key}

        res2 = requests.get(url2, headers=HEADERS)
        data3[i] = res2.json()
        data3[i] = data3[i]["data"]["candles"]
        data3[i] = pd.DataFrame(data3[i])
        data3[i] = data3[i].rename(
            columns={0: 'Time', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Close', 5: 'Volume'})
    TR1 = data1[0]['Time'].iloc[-1]
    TR1 = TR1.split('T')[1]
    for i in range(len(dict3)):
        Rhr1[i] = int(TR1.split(':')[0])
        Rmin1[i] = int(TR1.split(':')[1])

    TS1 = data2[0]['Time'].iloc[-1]
    # print(TS1)
    TS1 = TS1.split('T')[1]
    for i in range(len(dict3)):
        Shr1[i] = int(TS1.split(':')[0])
        Smin1[i] = int(TS1.split(':')[1])

    TM1 = data3[0]['Time'].iloc[-1]
    # print(TS1)
    TM1 = TM1.split('T')[1]
    for i in range(len(dict3)):
        Mhr1[i] = int(TM1.split(':')[0])
        Mmin1[i] = int(TM1.split(':')[1])
    return data1, data2, data3, Rhr1, Rmin1, Shr1, Smin1, Mhr1, Mmin1


def paperTrade(papercapital, trade_flag, le_t, se_t, dict3, trade_tokens, invst, ltp_f, dict1, trade_name, entry_val, size, slots, pnl, trade_ltp, lxflag, dict2, sxflag):
    if 0 in trade_flag:
        pos = trade_flag.index(0)
        if len(le_t) > 0:
            token1 = dict3[le_t[-1]]
        if len(se_t) > 0:
            token2 = dict3[se_t[-1]]
            print(token2)

        if len(le_t) > 0 or len(se_t) > 0:
            if token1 not in trade_tokens:
                sizep = invst//ltp_f[le_t[-1]]
                if sizep >= 1:
                    trade_flag[pos] = 1
                    trade_tokens[pos] = token1
                    trade_name[pos] = dict1[token1]
                    entry_val[pos] = ltp_f[le_t[-1]]
                    size[pos] = invst//entry_val[pos]
                    print("trade opened")
                    print(trade_name[pos], trade_flag[pos],
                          entry_val[pos], size[pos])
                    le_t.pop()
            elif token2 not in trade_tokens:
                sizep = invst//ltp_f[le_t[-1]]
                if sizep >= 1:
                    trade_flag[pos] = 2
                    trade_tokens[pos] = token2
                    trade_name[pos] = dict1[token2]
                    entry_val[pos] = ltp_f[se_t[-1]]
                    size[pos] = invst//entry_val[pos]
                    print("trade opened")
                    print(trade_name[pos], trade_flag[pos],
                          entry_val[pos], size[pos])
                    se_t.pop()
    if slots > len(trade_flag):
        for i in range(slots-len(trade_flag)):
            trade_tokens.append(0)
            trade_flag.append(0)
            trade_name.append('')
            entry_val.append(0)
            pnl.append(0)
            size.append(0)
            trade_ltp.append(0)

    for i in range(slots):
        if trade_flag[i] != 0:
            if trade_flag[i] == 1:
                loop = dict2[trade_tokens[i]]
                if lxflag[loop] == False:
                    trade_ltp[i] = ltp_f[loop]
                    pnl1 = (ltp_f[loop]-entry_val[i])*size[i]
                    if pnl1 != pnl[i]:
                        papercapital = papercapital-pnl[i]
                        pnl[i] = pnl1
                        papercapital = papercapital+pnl[i]
                        print("trade updated")
                        print(trade_name[i], trade_flag[i], entry_val[i],
                              size[i], trade_ltp[i], pnl[i], papercapital)
                else:
                    trade_flag[i] = 0
                    print("trade closed")
                    print(trade_name[i], pnl[i])
            elif trade_flag[i] == 2:
                loop = dict2[trade_tokens[i]]
                if sxflag[loop] == False:
                    trade_ltp[i] = ltp_f[loop]
                    pnl1 = (entry_val[i]-ltp_f[loop])*size[i]
                    if pnl1 != pnl[i]:
                        papercapital = papercapital-pnl[i]
                        pnl[i] = pnl1
                        papercapital = papercapital+pnl[i]
                        print("trade updated")
                        print(trade_name[i], trade_flag[i], entry_val[i],
                              size[i], trade_ltp[i], pnl[i], papercapital)
                else:
                    trade_flag[i] = 0
                    print("trade closed")
                    print(trade_name[i], pnl[i])
    return papercapital, size, trade_name, pnl, entry_val, trade_ltp, trade_tokens
