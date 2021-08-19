import requests
from datetime import datetime, timedelta
import pandas as pd
from indicator import *


def onticks(ticks, close, allltp, s, nltp, ntime, sltp, stime, bltp, btime, iltp, itime, ltp_f, le_t, se_t, Rmin1, Rhr1, Shr1, Smin1, Mhr1, Mmin1, data1, data2, data3, signal, dict1,
            dict2, leflag, lxflag, seflag, sxflag, flag4, chtime, lsigflag, ssigflag, sigmin, Rlen, Slen, Mlen, codes_nse, codes_mcx, hlist_nse, hlist_mcx, hlist_mcx_m, hlist_mcx_e, dict3):
    for i in range(len(ticks)):
        c = close[ticks[i]['instrument_token']]
        allltp[ticks[i]['instrument_token']] = [ticks[i]['last_price'], c]
        s[ticks[i]['instrument_token']] = ((ticks[i]['last_price']-c)/c)*100
        if ticks[i]['instrument_token'] == 256265:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)[:5]
            nltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            ntime = time
        if ticks[i]['instrument_token'] == 265:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)[:5]
            sltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            stime = time
        if ticks[i]['instrument_token'] == 260105:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)[:5]
            bltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            btime = time
        if ticks[i]['instrument_token'] == 264969:
            date = ticks[i]['timestamp']
            time = date.time()
            time = str(time)[:5]
            iltp = [ticks[i]['last_price'], ((ticks[i]['last_price']-c)/c)*100]
            itime = time
            # logging.debug("Ticks: {}".format(ticks))
        ltp = ticks[i]['last_price']
        ohlc = ticks[i]['ohlc']
        ltp_df = {'Close': ltp}
        tk = ticks[i]['instrument_token']
        le_t, se_t, ltp_f, lxflag, sxflag = indicator(tk, ltp, ohlc, ltp_df, ltp_f, le_t, se_t, Rmin1, Rhr1, Shr1, Smin1, Mhr1, Mmin1, data1, data2, data3, signal, dict1,
                                                      dict2, leflag, lxflag, seflag, sxflag, flag4, chtime, lsigflag, ssigflag, sigmin, Rlen, Slen, Mlen, codes_nse, codes_mcx, hlist_nse, hlist_mcx, hlist_mcx_m, hlist_mcx_e, dict3)
    return close, allltp, s, nltp, ntime, sltp, stime, bltp, btime, iltp, itime, le_t, se_t, ltp_f, lxflag, sxflag
