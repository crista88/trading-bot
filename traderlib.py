# enconding: utf-8
from logger import * 
#import alpaca_trade_api as tradeapi
import sys, time, os, pytz
import tulipy as ti
#import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from math import ceil
import gvars
from enum import Enum
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import yfinance as yf

class TimeFrame(Enum):
    Day = "1Day"
    Hour = "1Hour"
    Minute = "1Min"
    Sec = "1Sec"

class Trader:

    def __init__(self, ticker, api):
        lg.info("Trader initialized with ticker %s" % ticker)
        self.ticker = ticker
        self.api = api

    
    def is_tradable(self, ticker):
        # check if tradable : ask the API/broker if "asset" is tradable
            # IN: asset as string 
            # OUT :True(if trtadeble) /False( not tradeble)
        try:
            # get asset from alpaca wrapper (.tradable)
            if not ticker.tradable:
                lg.info("The asset %s is not tradable" % ticker)
                return False
            else:
                lg.info("The asset %s is  tradable" % ticker)
                return True
        except: 
            lg.error("The asset %s is not answering well" % ticker)
            return False

    def set_stopLoss(self, entryPrice, trend):
        # takes an entry price as input and set the stoplose (direction)
            # IN : entry price, direction (long/short)
            # OUT : stop loss
         
        try:
            if trend == "long":
                # example 10 - (10*0.05) = 9.5
                stopLoss = entryPrice - (entryPrice * gvars.stopLossMargin)
                return stopLoss
            elif trend == "short": 
                # example 10 + (10*0.05) = 10.5
                stopLoss = entryPrice + (entryPrice * gvars.stopLossMargin)
                return stopLoss
            else:
                raise ValueError
            
        except Exception as e:
            lg.error("The direction value is not understood: %s" % str(trend))
            sys.exit()
      
    def set_takeProfit(self, entryPrice, trend):
        # takes an entry price as input and set the take profit (direction)
            # IN : entry price, direction (long/short)
            # OUT : take profit
        
        try:
            if trend == "long":
                # example 10 + (10*0.1) = 11
                takeProfit = entryPrice + (entryPrice * gvars.takeprofitMargin)
                lg.info("tale profit set for long at %.2f" % takeProfit)
                return takeProfit
            elif trend == "short": 
                # example 10 - (10*0.1) = 9
                takeProfit = entryPrice - (entryPrice * gvars.takeprofitMargin)
                lg.info("tale profit set for short at %.2f" % takeProfit)
                return takeProfit
            else:
                raise ValueError
            
        except Exception as e:
            lg.error("The direction value is not understood: %s" % str(trend))
            sys.exit()
      
    def load_historical_data(self, ticker, interval, period):
        #load the historical stocks data: content from API and gives us a valid array. I put it here because i want to make some checks before put it in the algorithm
            # IN: api, ticker, interval(window length- aggregation 1Day, 1Hour, 15Min, 1Min), entry limit
            # OUT: array with stock data(OHCL data)   OHCL = open high close low data 
        
        try:
            ticker = yf.Ticker(ticker)
            data = ticker.history(interval, period)

        except Exception as e:
            lg.error("Something happend while loading historical data")
            lg.error(e)
            sys.exit()

        return data

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

    def submit_order(self, type, trend, ticker, sharesQty, currentPrice, exit=False):
        # IN : order data(nr of shares), order type(if is a limit order or market order)
        # OUT : boolean (True = order went through, False = order did not get through)
        lg.info("Submitting %s order for %s" % (trend, ticker))

        if trend == "long" and not exit:
            side = "buy"
            limitPrice = round(currentPrice + currentPrice*gvars.maxVar,2)
        elif trend == "short" and not exit:
            side = "sell"
            limitPrice = round(currentPrice - currentPrice*gvars.maxVar,2)
        elif trend == "long" and exit:
            side = "sell"
        elif trend == "short" and exit:
            side = "buy"
        else:
            lg.error("Trend was not understood")
            sys.exit()

        try:
            if type == "limit":
                lg.info("Current price: %.2f // Limit Price: %.2f" % (currentPrice, limitPrice))
                order = self.api.submit_order(
                    symbol=ticker,
                    qty=sharesQty,
                    side=side,
                    type=type,
                    time_in_force="gtc",
                    limit_price=limitPrice
                )
            elif type == "market":
                lg.info("Current price: %.2f" % currentPrice)
                order = self.api.submit_order(
                    symbol=ticker,
                    qty=sharesQty,
                    side=side,
                    type=type,
                    time_in_force="gtc"
                )
            else:
                lg.error("Type of order was not understood")
                sys.exit()

            self.orderId = order.id

            lg.info("%s order submitted correctly!" % trend)
            lg.info("%d shares %s for %s" % (sharesQty, side, ticker))
            lg.info("Client order id: %s" %self.orderId)
            return True

        except Exception as e:
            lg.error("Something happend when submitting order")
            lg.error(e)
            # sys.exit()    # not sure if needed  or return False !!!  double check after testing if i want to get out or to return false
            return False
        
    def cancel_order(self):
    #cancel order : cancels our order (retry)
        #IN: orer id
        #OUT: boolean (True =  order cancelled, False = order not cancelled)
        return ("To be made!!")
    
    def check_position(self, ticker, doNotFind=False):
        #check position : check if the position has open or not
            # IN: ticker, doNotFind (means that i dont want to find!)
            # OUT: boolean (True = order is there, False = order not there)
        attempt = 1

        while attempt <= gvars.maxAttemptsCP:
            try:
                position = self.api.get_position(ticker)
                self.currentPrice = position.current_price
                lg.info("The position was found. Current price is: %.2f" %self.currentPrice)
                return True
            except:
                if doNotFind:
                    lg.info("Position not found, this is good!")
                    return False  # with this is we skip the retry below if we DONT WANT TO FIND THIS
                #i want to retry
                lg.info("Position not found, waiting for it...")
                time.sleep(gvars.sleepTimeCP)  #wait 5 sec and retry
                attempt += 1

        lg.info("Position not found for %s, not waiting any more" % ticker)
        return False

    def get_shares_amount(self, assetPrice):
        # we will calc the number of shares that we will put in the next order depending on the total amount that we have available
        # In: assetprice
        # OUT: number of shares

        lg.info("Getting shares ammount)")

        try:
        
            #get the total equity available
            totalEquity = " ask Alpaca wrapper for available equity"
            #calculate the number of shares
            sharesQuantity = int(gvars.maxSpendEquity / assetPrice)
            lg.info("Total shares to operate with: %d" % sharesQuantity)
            return sharesQuantity
        
        except Exception as e:
            lg.error("Something happend at get shares ammount")
            lg.error(e)
            sys.exit()

    def get_current_price(self, ticker):
        #get the current price of an asset with a position open
            # IN: ticker
            # OUT: price $
        
        attempt = 1

        while attempt <= gvars.maxAttemptsGCP:
            try:
                position = None #ask alpaca wrapper for a position
                self.currentPrice = position.current_price
                lg.info("The position was checked. Current price is: %.2f" %self.currentPrice)
                return self.currentPrice
            except:
                #i want to retry
                lg.info("Position not found, cannot check price waiting for it...")
                time.sleep(gvars.sleepTimeGCP)  
                attempt += 1

        lg.error("Position not found for %s, not waiting any more" % ticker)
        return False

    def get_avg_entry_price(self, ticker):
        # get the current price of an ticker with a position open
            # IN: ticker
            # OUT: price $
        attempt = 1

        while attempt <= gvars.maxAttemptsGAEP:
            try:
                position = self.api.get_position(ticker)
                avgEntryPrice = float(position.avg_entry_price)
                lg.info("The position was checked. Current price is: %.2f" % avgEntryPrice)
                return avgEntryPrice
            except:
                lg.info("Position not found, cannot check price, waiting for it...")
                time.sleep(gvars.sleepTimeGAEP)
                attempt += 1

        lg.error("Position not found for %s, not waiting any more" % ticker)
        return False
    
    def get_general_trend(self, ticker):
        # get general trend
            # IN : asset, i will get 30 min candle data (i will see what from the data i will need,  probably the last value that it had-close data)-load historical data fc 
            # OUT : UP islong /DOWN is short/false if no trend as strings  if no trend we go back to asset
                # IF NO TREND GO BACK TO POINT ECHO
        lg.info("GENERAL TREND ANALYSIS entered")

        attempt = 1

        try:
            while True:
                #ask for 30 min candles  , period = 50 samples *30 min = 1500 but 1 day has 8 working hours and every week 5 working days, 
                #that is why period = 5d to skip weekends day, but 8 working hour have 16 windoes that why 50samples *16 windows = 5 days
                data = self.load_historical_data(ticker, interval="30m", period="5d")
                #close = data.Close.values

                # calculate the EMAs
                ema9 = ti.ema(data.Close.values, 9)[-1]
                ema26 = ti.ema(data.Close.values, 26)[-1]
                ema50 = ti.ema(data.Close.values, 50)[-1]

                lg.info("%s general trend EMAs: [%.2f,%.2f,%.2f]" % (ticker,ema9,ema26,ema50))
                        
                #cheking the EMAs relative position
                if (ema50 > ema26) and (ema26 > ema9):
                    lg.info("Trend detected for %s: long" % ticker)
                    return "long"
                elif (ema50 < ema26) and (ema26 < ema9):
                    lg.info("Trend detected for %s: short" % ticker)
                    return "short"
                elif attempt <= gvars.maxAttemptsGT:
                    lg.info("Trend not clear for %s, waiting" % ticker)
                    attempt += 1
                    time.sleep(gvars.sleepTimeGT*gvars.maxAttemptsGT)
                else:
                    lg.info("Trend not detected and timeout reached for %s" % ticker)
                    return False
                
        except Exception as e:
            lg.error("Something went wrong at the get general trend")
            lg.error(e)
            sys.exit()

    def get_instant_trend(self, ticker, trend):
        # get instant trend: # confirm the trend detected by general trend analyses
            # IN : asset, trend(long/short)
            # OUT : True as trend confirmed or False as not confirmed-not a good moment to enter
        lg.info("INSTANT TREND ANALYSIS entered")

        attempt = 1

        try:
            while True:
                # period = 50 samples of 5 mi = 1day
                data = self.load_historical_data(ticker, interval="5m", period="1d")
                close = data.Close.values

                # calculate the EMAs
                ema9 = ti.ema(data.close, 9)[-1]
                ema26 = ti.ema(data.close, 26)[-1]
                ema50 = ti.ema(data.close, 50)[-1]

                lg.info("%s instant trend EMAs: [%.2f,%.2f,%.2f]" % (ticker,ema9,ema26,ema50))

                if (trend == "long") and (ema9 > ema26) and (ema26 > ema50):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (ema9 < ema26) and (ema26 < ema50):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= gvars.maxAttemptsIT:
                    lg.info("Trend not clear for %s, waiting" % ticker)
                    attempt += 1
                    time.sleep(30)  # ?? adjust the sec if needed 30 or mayby 20 ??
                else:
                    lg.info("Trend not detected and timeout reached for %s" % ticker)
                    return False
        except Exception as e:
            lg.error("Something went wrong at the get instant trend")
            lg.error(e)
            sys.exit()

    def get_rsi(self, ticker, trend):
        # get rsi: 
            # IN : asset, trend (5 min candle data (i will see what from the data i will need,  probably the last value that it had-close data))
            # OUT : True as confirmed or False as not confirmed
        lg.info("RSI  ANALYSIS entered")   

        attempt = 1

        try:
            while True:
                data = self.load_historical_data(ticker, interval="5m", period="1d")

                # calculate the RSI
                rsi = ti.rsi(data.Close.values, 14)[-1]  # it uses 14 samples window

                lg.info("%s rsi = %.2f" % (ticker,rsi))

                if (trend == "long") and (rsi > 50) and (rsi < 80):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (rsi < 50) and (rsi > 20):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= gvars.maxAttemptsRSI:
                    lg.info("Trend not clear for %s, waiting" % ticker)
                    attempt += 1
                    time.sleep(gvars.sleepTimeRSI)  
                else:
                    lg.info("Trend not detected and timeout reached for %s" % ticker)
                    return False
                
        except Exception as e:
            lg.error("Something went wrong at the get rsi analysis")
            lg.error(e)
            sys.exit()

    def get_stochastic(self, ticker, trend):
        # get stochastic:
            # IN: asset, trend - 5 min candle(OHLC all the data for every candle)
            # OUT : True as confirmed or False as not confirmed
        lg.info("STOCHASTIC  ANALYSIS entered")   

        attempt = 1

        try:
            while True:
                data = self.load_historical_data(ticker, interval="5m", period="1d")

                # calculate the STOCHASTIC  stoch_k = fast curve, stoch_d = slow curve
                stoch_k, stoch_d = ti.stoch(data.High.values, data.Low.values, data.Close.values, 9, 6, 9)  # OPEN HIGH LOW AND CLOSE VALUE
                stoch_k = stoch_k[-1]
                stoch_d = stoch_d[-1]
                #here our data can be either the closing price-close or the highest price-high or the lowest-low
                #! in the other function our data = opening price - from OPEN HIGH LOW AND CLOSE VALUE (OHLC) but in this fc can be any of the other 3 but not the first

                lg.info("%s stochastic = [%.2f, %.2f]" % (ticker,stoch_k,stoch_d))

                if (trend == "long") and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80):
                    lg.info("Long trend confirmed for %s" % ticker)
                    return True
                elif (trend == "short") and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20):
                    lg.info("Short trend confirmed for %s" % ticker)
                    return True
                elif attempt <= gvars.maxAttemptsSTH:
                    lg.info("Trend not clear for %s, waiting" % ticker)
                    attempt += 1
                    time.sleep(gvars.sleepTimeSTC)  # ?? adjust the sec if needed 30 or mayby 20 ??
                else:
                    lg.info("Trend not detected and timeout reached for %s" % ticker)
                    return False
                
        except Exception as e:
            lg.error("Something went wrong at the get stochastic analysis")
            lg.error(e)
            sys.exit()  
    
    def check_stochastic_crossing(self, ticker, trend):
        #check if the stichastic curves have crossed or not
        #depending on the trend
            # IN: asset, trend
            # OUT : True if crossed/ False if not crossed
        lg.info("Checking stochastic crossing...")

        #period = 50 samples of 5 min = 1 day
        data = self.load_historical_data(ticker, interval="5m", period="1d")
        
        # get stochastic values
        stoch_k, stoch_d = ti.stoch(data.High.values, data.Low.values, data.Close.values, 9, 6, 9)  # OPEN HIGH LOW AND CLOSE VALUE
        stoch_k = stoch_k[-1]
        stoch_d = stoch_d[-1]
        lg.info("%s stochastic = [K_FAST:%.2f,D_SLOW:%.2f]" % (ticker,stoch_k,stoch_d))

        # logic
        try:
            if (trend == "long") and (stoch_k <= stoch_d):
                lg.info("Stochastic curves crossed: long, k=%.2f, d=%.2f" % (stoch_k, stoch_d))
                return True
            elif (trend == "short") and (stoch_k >= stoch_d):
                lg.info("Stochastic curves crossed: short, k=%.2f, d=%.2f" % (stoch_k, stoch_d))
                return True
            else:
                lg.info("Stochastic curves have not crossed")
                return False
        
        except Exception as e:
            lg.error("Something went wrong at check stochastic crossing")
            lg.error(e)
            return True # return True becasue this is the way to force the closing of the possition, if false it will loop infinite

    def enter_position_mode(self, ticker, trend):
        # enter position mode: check the filters in parallel (inside the positions)so if ay of them is cheked out we GET OUT

        attempt = 1

        entryPrice = " ask the Alpaca API for the entry price"
        # set take profit
        takeProfit = self.set_takeProfit(entryPrice, trend)
        #set stop loss
        stopLoss = self.set_stopLoss(entryPrice, trend)

        try:
            while True:

                self.currentPrice = self.get_current_price(ticker)

                # CHECK IF TAKE PROFIT IS MET: -> if true CLOSE POSITION
                # LONG or UP version
                if (trend == "long") and (self.currentPrice >= takeProfit):
                    lg.info("Take profit met at %.2f.Current price is %.2f getting out..." % (takeProfit, self.currentPrice))
                    return True
                # SHORT or DOWN version
                elif (trend == "short") and (self.currentPrice <= takeProfit):
                    lg.info("Take profit met at %.2f.Current price is %.2f getting out..." % (takeProfit, self.currentPrice))
                    return True
                
                #CHECK IF STOP LOSS IS MET
                #LONG or UP version
                elif (trend == "long") and (self.currentPrice <= stopLoss):
                    lg.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss, self.currentPrice))  
                    return False             
                #SHORT or DOWN version
                elif (trend == "short") and (self.currentPrice <= stopLoss):
                    lg.info("Stop loss met at %.2f. Current price is %.2f" % (stopLoss, self.currentPrice))  
                    return False  
                
                # ELIF check stochastic crossing.Here we could be gaining or loosing. using fc above for check_stochastic_data
                elif self.check_stochastic_crossing(): # here posibil error because this function takes input the trend and i dont have it here ?? check later
                    lg.info("Stochastic curves crossed.Current price is %.2f" % self.currentPrice)
                    return True
                
                #else we wait
                elif attempt <= gvars.maxAttemptEPM:
                    lg.info("Still waiting inside the position, attempt#%d" % attempt)
                    lg.info("stop loss %.2f <-- current price %.2f --> take profit %.2f" % (stopLoss, self.currentPrice, takeProfit))
                    time.sleep(gvars.sleepTimeEPM)

                # get out , time is out
                else:
                    lg.info("Timeout reached at enter position, too late")
                    return False
                
        except Exception as e:
            lg.error("Something happend at enter position function")
            lg.error(e)
            return True
                

    def run(self, ticker): 
        # LOOP UNTIL TIMEOUT REACHED (EX 2H)

        while True:
            # POINT ECHO: INITIAL CHECK

            #ask the API/broker if we have an open position with "asset"
                
            if self.check_position(self.ticker, doNotFind=True):
                lg.info("There is already an open position with that asset! Aborting...")
                return False  # abort execution of the remaining code here if the position is found


            # POINT DELTA
            while True:
                # get general trend : find a trend
                trend = self.get_general_trend(self.ticker)
                if not trend:
                    lg.info("No general trend found for %s! Going out" % self.ticker)
                    return False # abort execution of the remaining code here if general trend  is not found
                            

                # get instant trend
                if not self.get_instant_trend(self.ticker, trend):
                    lg.info("Instant trend was not confirmed. Going back.")
                    # if failed go back to POINT DELTA   
                    continue

                # get rsi - fc from above
                if not self.get_rsi(self.ticker, trend):
                    lg.info("RSI was not confirmed. Going back.")
                    # if failed go back to POINT DELTA   
                    continue

                # get stochastic - fc from above
                if not self.get_stochastic(self.ticker, trend):
                    lg.info("Stochastic was not confirmed. Going back.")
                    # if failed go back to POINT DELTA   
                    continue

                lg.info("All filters passed, continue with the order!")
                break # get out of the loop
            
            # get_current_price before submit the order to be sure
            self.currentPrice = round(float(self.load_historical_data(ticker, interval="1m", period="1d").Close.values)[-1], 2)
            

            # get_shares_amount
                # decide how much money/nr of shares we want to invest .but we have to check if we have the funds becouse we will have other open positions in that time!
            sharesQty = self.get_shares_amount(self.currentPrice)
            lg.info("Desired Entry Price: %.2f" % self.currentPrice)
            # SUBMIT ORDER- this is a limit order - FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED
                # if false abort, OR go back to POINT ECHO
            succes = self.submit_order(
                "limit",
                trend,
                ticker,
                sharesQty,
                self.currentPrice
            )

            # CHECK POSITION: see if the position exists-FUNCTION DEFINED ABOVE IN THE CLASS TO BE CALLED
            if not self.check_position(self.ticker):
                # cancel the order fUNCTION ABOVE DEFINED
                continue # go back to POINT ECHO if we failed in finding the position (the order did not went through) or we continue if we found it
            
            # ENTER POSITION MODE function # check the filters in parallel so if ay of them is cheked out we GET OUT
            succesfullOperation = self.enter_position_mode(self.ticker, trend) # it return true once we have to get out
                
            # GET OUT
            while True:               # loop until succes

                # SUBMIT ORDER(market)

                #check the position if is cleared
                if not self.check_position(self.ticker, doNotFind=True):
                    break  # if we dont find a position we break this while
                    
                time.sleep(10)  # wait 10 sec   

            # end / back to beggining
            return succesfullOperation    
                 

      
