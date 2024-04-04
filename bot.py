# enconding: utf-8

# import needed libraries
from traderlib import *
from logger import *
import sys
import gvars
import alpaca_trade_api as tradeapi


# API_KEY = "PK1R56HAKWASE75FQNMS"
# API_SECRET_KEY = "vkVpLuJjbfCafoQQ6QTNDh4jtMsdoq8fDa89ABcs"
# API_URL = "https://paper-api.alpaca.markets/v2"

# check our trading account(blocked? total amount)
def check_account_ok():
    try: 
        #get account info
        print("Cheking")
    except Exception as e:
        lg.error("Could not get account info")
        lg.info(str(e))
        sys.exit()

# close current orders (doublecheck)
def clean_open_orders():
    #get list of open orders
    lg.info("List of open orders")
    lg.info(str(open_orders))

    for order in open_orders:
        #close order
        lg.info("Order %s closed" % str(order.id))
    
    lg.info("Closing orders complete")


# execute trading bot this function is the main and will ex all the algorithm from traderlib.py
def main():
    
    api= tradeapi.REST(key_id=gvars.API_KEY, secret_key=gvars.API_SECRET_KEY, base_url=gvars.API_URL, api_version="v2")

    #import pdb; pdb.set_trace()
    breakpoint()
    # initialize the logger (imported from logger)
    initialize_logger()
    # check if the account is ok
    check_account_ok()
    # close current order
    clean_open_orders()
    #define asset insert the value/ get the ticker
    ticker = input("Write the ticker you want to operate with")

    trader = Trader(ticker) #initialize trading bot
    tradingSuccess = trader.run() #run trading bot library 
    #run trading bot it's going to be a function from traderlib
        # in: string (ticker)
        # OUT: boolean (Tru = succes / False = failure)
    if not tradingSuccess:
        lg.info("Trading was not successful, locking asset")
        # wait some time

if __name__ == "__main__":
    main()