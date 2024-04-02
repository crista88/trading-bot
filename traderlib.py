# enconding: utf-8
from logger import * 
import alpaca_trade_api as tradeapi
import sys, time, os, pytz
import tulipy as ti
import numpy as np
import pandas as pd
from datetime import datetime
from math import ceil


class Trader:

    def __init__(self, ticker):
        lg.info("Trader initialized with ticker" % ticker)

    
    def is_tradable(self, ticker):
        # check if tradable : ask the API/broker if "asset" is tradable
            # IN: asset as string 
            # OUT :True(if trtadeble) /False( not tradeble)
        try:
            # get asset from alpaca wrapper (.tradable)
            if not asset.tradable:
                lg.info("The asset %s is not tradable" % ticker)
                return False
            else:
                lg.info("The asset %s is  tradable" % ticker)
                return True
        except: 
            lg.error("The asset %s is not answering well" % ticker)
            return False

    def set_stoploss(self, entryPrice, direction):
        # takes an entry price as input and set the stoplose (direction)
            # IN : entry price, direction (long/short)
            # OUT : stop loss
        stopLossMargin = 0.05  # percentage margin 

        try:
            if direction == "long":
                # example 10 - (10*0.05) = 9.5
                stopLoss = entryPrice - (entryPrice * stopLossMargin)
                return stopLoss
            elif direction == "short": 
                # example 10 + (10*0.05) = 10.5
                stopLoss = entryPrice + (entryPrice * stopLossMargin)
                return stopLoss
            else:
                raise ValueError
            
        except Exception as e:
            lg.error("The direction value is not understood: %s" % str(direction))
            sys.exit()
      
    def set_takeProfit(self, entryPrice, direction):
        # takes an entry price as input and set the take profit (direction)
            # IN : entry price, direction (long/short)
            # OUT : take profit
        takeProfitMargin = 0.1 # percentage margin

        try:
            if direction == "long":
                # example 10 + (10*0.1) = 11
                takeProfit = entryPrice + (entryPrice * takeProfitMargin)
                return takeProfit
            elif direction == "short": 
                # example 10 - (10*0.1) = 9
                takeProfit = entryPrice - (entryPrice * takeProfitMargin)
                return takeProfit
            else:
                raise ValueError
            
        except Exception as e:
            lg.error("The direction value is not understood: %s" % str(direction))
            sys.exit()
      
     
    #load the historical stocks data: content from API and gives us a valid array. I put it here because i want to make some checks before put it in the algorithm
        # IN: ticker, interval, entry limit
        # OUT: array with stock data(OHCL data)   OHCL = open high close low data   

    def get_open_positions(self, assetId):  # i use assetId and not ticker because dif markets can have same ticker for an asset but for sure different assetId so i want to be precise
        # get open position, a fc that check if we have a position with that ticker
            # IN: assetId (unique identifier)
            # OUT: boolean (True = already open, False = not open)
        
        positions = {}   #ask alpaca wrapper for the list with open positions
        for position in positions:
            if position.symbol == assetId:
                return True
            else:
                return False

  
    #submit order:gets our order through the API (retry)
        # IN : order data, order type(if is a limit order or market order)
        # OUT : boolean (True = order went through, False = order did not get through)


    #cancel order : cancels our order (retry)
        #IN: orer id
        #OUT: boolean (True =  order cancelled, False = order not cancelled)

    def check_position(self, asset):
        #check position : check if the position has open or not
            # IN: ticker
            # OUT: boolean (True = order is there, False = order not there)
        maxAttempts = 5
        attempt = 1

        while attempt <= maxAttempts:
            try:
                position = None #ask alpaca wrapper for a position
                currentPrice = position.current_price
                lg.info("The position was checked. Current price is: %.2f" %currentPrice)
                return True
            except:
                #i want to retry
                lg.info("Position not found, waiting for it...")
                time.sleep(5)  #wait 5 sec and retry
                attempt += 1

        lg.info("Position not found for %s, not waiting any more" % asset)
        return False

    def get_general_trend(self, asset):
        # get general trend
            # IN : asset, i will get 30 min candle data (i will see what from the data i will need,  probably the last value that it had-close data)-load historical data fc 
            # OUT : UP islong /DOWN is short/NO TREND as strings  if no trend we go back to asset
                # IF NO TREND GO BACK TO POINT ECHO
        lg.info("GENERAL TREND ANALYSIS entered")

        attempt = 1
        maxAttempts = 10 # ! total time = maxAttempts * 60 sec as implemented

        try:
            while True:
                data = "ask Alpaca wrapper for 30 min candles  ? candles to be determined"

                # calculate the EMAs
                ema9 = ti.ema(data, 9)
                ema26 = ti.ema(data, 26)
                ema50 = ti.ema(data, 50)

                lg.info("%s general trend EMAs: [%.2f,%.2f,%.2f]" % (asset,ema9,ema26,ema50))
                        
                #cheking the EMAs relative position
                if (ema50 > ema26) and (ema26 > ema9):
                    lg.info("Trend detected for %s: long" % asset)
                    return "long"
                elif (ema50 < ema26) and (ema26 < ema9):
                    lg.info("Trend detected for %s: short" % asset)
                    return "short"
                elif attempt <= maxAttempts:
                    lg.info("Trend not clear for %s, waiting" % asset)
                    attempt += 1
                    time.sleep(60)
                else:
                    lg.info("Trend not detected and timeout reached for %s" % asset)
                    return "no trend"
                
        except Exception as e:
            lg.error("Something went wrong at the get general trend")
            lg.error(e)
            sys.exit()

    def get_instant_trend(self, asset, trend):
        # get instant trend: # confirm the trend detected by general trend analyses
            # IN : asset, trend(long/short)
            # OUT : True as trend confirmed or False as not confirmed-not a good moment to enter
        lg.info("INSTANT TREND ANALYSIS entered")

        attempt = 1
        maxAttempts = 10 # ! total time = maxAttempts * 10 sec as implemented

        try:
            while True:
                data = "ask Alpaca wrapper for 5 min candles  ? candles to be determined"

                # calculate the EMAs
                ema9 = ti.ema(data, 9)
                ema26 = ti.ema(data, 26)
                ema50 = ti.ema(data, 50)

                lg.info("%s instant trend EMAs: [%.2f,%.2f,%.2f]" % (asset,ema9,ema26,ema50))

                if (trend == "long") and (ema9 > ema26) and (ema26 > ema50):
                    lg.info("Long trend confirmed for %s" % asset)
                    return True
                elif (trend == "short") and (ema9 < ema26) and (ema26 < ema50):
                    lg.info("Short trend confirmed for %s" % asset)
                    return True
                elif attempt <= maxAttempts:
                    lg.info("Trend not clear for %s, waiting" % asset)
                    attempt += 1
                    time.sleep(30)  # ?? adjust the sec if needed 30 or mayby 20 ??
                else:
                    lg.info("Trend not detected and timeout reached for %s" % asset)
                    return False
        except Exception as e:
            lg.error("Something went wrong at the get instant trend")
            lg.error(e)
            sys.exit()

    def get_rsi(self, asset, trend):
        # get rsi: 
            # IN : asset, trend (5 min candle data (i will see what from the data i will need,  probably the last value that it had-close data))
            # OUT : True as confirmed or False as not confirmed
        lg.info("RSI  ANALYSIS entered")   

        attempt = 1
        maxAttempts = 10 # ! total time = maxAttempts * 20 sec as implemented

        try:
            while True:
                data = "ask Alpaca wrapper for 5 min candles  ? candles to be determined"

                # calculate the RSI
                rsi = ti.rsi(data, 14)  # it uses 14 samples window

                lg.info("%s rsi = %.2f" % (asset,rsi))

                if (trend == "long") and (rsi > 50) and (rsi < 80):
                    lg.info("Long trend confirmed for %s" % asset)
                    return True
                elif (trend == "short") and (rsi < 50) and (rsi > 20):
                    lg.info("Short trend confirmed for %s" % asset)
                    return True
                elif attempt <= maxAttempts:
                    lg.info("Trend not clear for %s, waiting" % asset)
                    attempt += 1
                    time.sleep(20)  # ?? adjust the sec if needed 30 or mayby 20 ??
                else:
                    lg.info("Trend not detected and timeout reached for %s" % asset)
                    return False
                
        except Exception as e:
            lg.error("Something went wrong at the get rsi analysis")
            lg.error(e)
            sys.exit()

    def get_stochastic(self, asset, trend):
        # get stochastic:
            # IN: asset, trend - 5 min candle(OHLC all the data for every candle)
            # OUT : True as confirmed or False as not confirmed
        lg.info("STOCHASTIC  ANALYSIS entered")   

        attempt = 1
        maxAttempts = 20 # ! total time = maxAttempts * 20 sec as implemented

        try:
            while True:
                data = "ask Alpaca wrapper for 5 min candles  ? candles to be determined"

                # calculate the STOCHASTIC  stoch_k = fast curve, stoch_d = slow curve
                stoch_k, stoch_d = ti.stoch(high, low, close, 9, 6, 9)  # OPEN HIGH LOW AND CLOSE VALUE
                #here our data can be either the closing price-close or the highest price-high or the lowest-low
                #! in the other function our data = opening price - from OPEN HIGH LOW AND CLOSE VALUE (OHLC) but in this fc can be any of the other 3 but not the first

                lg.info("%s stochastic = [%.2f, %.2f]" % (asset,stoch_k,stoch_d))

                if (trend == "long") and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80):
                    lg.info("Long trend confirmed for %s" % asset)
                    return True
                elif (trend == "short") and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20):
                    lg.info("Short trend confirmed for %s" % asset)
                    return True
                elif attempt <= maxAttempts:
                    lg.info("Trend not clear for %s, waiting" % asset)
                    attempt += 1
                    time.sleep(10)  # ?? adjust the sec if needed 30 or mayby 20 ??
                else:
                    lg.info("Trend not detected and timeout reached for %s" % asset)
                    return False
                
        except Exception as e:
            lg.error("Something went wrong at the get stochastic analysis")
            lg.error(e)
            sys.exit()  

    # enter position mode: check the filters in parallel (inside the positions)so if ay of them is cheked out we GET OUT
         # IF check take profit: -> if true CLOSE POSITION
                # IN: current gains (earning $)
                # OUT: True/False

            # ELIF check stop loss->if true CLOSE POSITION
                # IN: current losses (loosing $)
                # OUT: True/False

            # ELIF check stochastic crossing.Here we could be gaining or loosing. Pull 5 min data(OHLC)-> if true CLOSE POSITION
                #STEP 1: pull 5 min OHLC data
                    # in: asset
                    #out: OHLC data (5 min candle)
                #STEP 2: calculate sthocastic, see if the stochastic curves are crossing
                    #in :OHLC data (5 min candle)
                    #out : TRUE / FALSE if thei cross as TRUE we get out

    def run():
        # LOOP UNTIL TIMEOUT REACHED (EX 2H)
            # POINT ECHO: INITIAL CHECK
            # CHECK POSITION : ask the API/broker if we have an open position with "asset"
                # will be function with IN: asset as string // OUT :True(if exists) /False(does not exists)


            # TREND ANALYSES - FUNCTION HISTORICAL DATA FUNCTION FROM ABOVE INTERVAL 30 MIN
            # load 30 min data/candles: demand API the 30 min candles

            # GENERAL TREND analysis : FUNCTION GENERAL TREND analyse if the trend is fav(detect interesting trend find if the trend is UP or DOWN or NO TREND)

            # LOOP until timeout reached(ex 30 min)
                #POINT DELTA
                # this loop will be as serial every condition has to be filled in cascade,
                # this loop is part of a bigger loop that includes DEFINE ASSET+INITIAL CHECK+GENERAL TREND

            # STEP 1: FUNCTION LOAD HISTORICAL DATA -load 5 min data/candle 
                # if failed go back to POINT DELTA

            # STEP 2: FUNCTION INSTANT TREND analysis : we know what are we looking for regardind the direction of the trend up/down/no trend//
                # if failed go back to POINT DELTA

            # STEP 3: FUNCTION RSI analysis - fc from above
                # if failed go back to POINT DELTA

            # STEP 4: FUNCTION stochastic analysis - fc from above
                # if failed go back to POINT DELTA


        # SUBMIT ORDER- this is a limit order - FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED
            # if false abort, OR go back to POINT ECHO

        # CHECK POSITION: see if the position exists-FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED
            # if false abort, OR  go back to POINT ECHO

        # LOOP UNTIL TIMEOUT REACHED EX 7-8 H
        # FUNCTION ENTER POSITION MODE  # check the filters in parallel so if ay of them is cheked out we GET OUT
           
        # GET OUT
        # SUBMIT ORDER- closing position/ sell what we have/ market order-FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED interact with broker API
                # if false retry until it workes because we want to sell
        # CHECK POSITION : see if the position exists-FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED
                # if false abort, OR  go back to submit order


        # wait 15 min

        # end / back to beggining
