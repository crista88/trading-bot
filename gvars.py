# encoding: utf-8

# REST API params

API_KEY = "PK1R56HAKWASE75FQNMS"
API_SECRET_KEY = "vkVpLuJjbfCafoQQ6QTNDh4jtMsdoq8fDa89ABcs"
API_URL = "https://paper-api.alpaca.markets/v2"

stopLossMargin = 0.05  # percentage margin for stop loss
    # example : 10 - (10*0.05) = 9.5 means that my stop loss is at 9.5 $

takeProfitMargin = 0.1 # percentage margin for take profit
    #example : 10 + (10*0.1) = 11 means that my take profit is at 11 $

maxSpendEquity = 1000 # $ total equity to spend in a single operation

# attempt = 1 #starting point of attempts for dif functions

# Max attempts section :
maxAttemptsCP = 5  # max attempts for Check Position function
maxAttemptsGCP = 5 # max attempts for Get Current Price function
maxAttemptsGT = 10 # ! total time = maxAttempts for general trend* 60 sec as implemented, // max attempts for Get General Trend function
maxAttemptsIT = 10 # ! total time = maxAttempts for instant trend  * 10 sec as implemented, // max attempts for Get Instant Trend function
maxAttemptsRSI = 10 # ! total time = maxAttempts for RSI * 20 sec as implemented, // max attempts for Get RSI function
maxAttemptsSTH = 20 # ! total time = maxAttempts for STOCHASTIC* 20 sec as implemented, // max attempts for Get STHOCASTIC function
maxAttemptEPM = 1440  # calculate 7-8 h how long the market is opened 8*60*60  / 20 , // max attempts for Enter Position Mode function

# Sleep time section:
sleepTimeCP = 5 # sleep time for Check Position
sleepTimeGCP = 5  # sleep time for Get Current Price function