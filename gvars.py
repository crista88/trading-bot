# encoding: utf-8

# REST API params

API_KEY = "PK1R56HAKWASE75FQNMS"
API_SECRET_KEY = "vkVpLuJjbfCafoQQ6QTNDh4jtMsdoq8fDa89ABcs"
API_URL = "https://paper-api.alpaca.markets"

stopLossMargin = 0.05  # percentage margin for stop loss
    # example : 10 - (10*0.05) = 9.5 means that my stop loss is at 9.5 $

takeProfitMargin = 0.1 # percentage margin for take profit
    #example : 10 + (10*0.1) = 11 means that my take profit is at 11 $

maxSpendEquity = 5000 # $ total equity to spend in a single operation

maxVar = 0.02   ###  5% the ammount that we want to add or substract to the price in calc the limit price for  putting in an order!!! 
                    # in other words max variation percentage when buying/selling
                #check properly what value should have !!! maybe fill have to be 2-3-5 % or can go high..check with tests

# Max attempts section :
maxAttemptsCP = 10  # max attempts for Check Position function
maxAttemptsGCP = 5 # max attempts for Get Current Price function
maxAttemptsGT = 10 # ! total time = maxAttempts for general trend* 60 sec as implemented, // max attempts for Get General Trend function
maxAttemptsIT = 10 # ! total time = maxAttempts for instant trend  * 10 sec as implemented, // max attempts for Get Instant Trend function check also with 20 tries
maxAttemptsRSI = 10 # ! total time = maxAttempts for RSI * 20 sec as implemented, // max attempts for Get RSI function check also with 20 tries
maxAttemptsSTH = 10 # ! total time = maxAttempts for STOCHASTIC* 20 sec as implemented, // max attempts for Get STHOCASTIC function  check also with 20 tries
maxAttemptsEPM = 360  # calculate 7-8 h how long the market is opened 8*60*60  / 20 , // max attempts for Enter Position Mode function 360 OR 1440 ??? CHECK WITH TESTS
maxAttemptsGAEP = 5 # max attempts for Get Avg Entry price function 
maxAttemptsCPO = 5 # max att for closing pending orders

# Sleep time section:  time in sec
sleepTimeCP = 5 # sleep time for Check Position
sleepTimeGCP = 5  # sleep time for Get Current Price function
sleepTimeGAEP = 5 # sleep time for Get Avg Entry Price function
sleepTimeRSI = 30 # for rsi  val 30
sleepTimeSTC = 20 # for stochastic val 20
sleepTimeEPM = 10 # for enter position mode fc val 10
sleepTimeGT = 60 # for general trend val 60
sleepTimeIT = 30 # for instand trend val 30
sleepTimeCPO = 5 # FOR CHECK PENDING POSITION
sleepTimeME = 60*60 # MAIN EXECUTION AFTER FAILING  val ok 60*60

#import pdb; pdb.set_trace()