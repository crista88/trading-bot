# enconding: utf-8

# import needed libraries
from traderlib import *
from logger import *
import sys
import gvars
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST



# check our trading account(blocked? total amount)
def check_account_ok(api):
    try: 
        #get account info
        
        account = api.get_account()
        if account.status != "ACTIVE":
            lg.error("The account is not AACTIVE, aborting")
            sys.exit()
    except Exception as e:
        lg.error("Could not get account info")
        lg.info(str(e))
        sys.exit()

# close current orders (doublecheck)
def clean_open_orders(api):

    lg.info("Cancelling all orders..")
    
    try:
        api.cancel_all_orders()
        lg.info("Closing orders complete")
    except Exception as e:
        lg.error("Could not cancell all orders")
        lg.error(e)
        sys.exit()

def check_asset_ok(api, ticker):
    # check if the asset is ok for trading
        # IN: ticker
        # OUT: TRUE if exist and is tradable and False otherwise
    lg.info("Checking the asset...")
    try:
        asset = api.get_asset(ticker)
        if asset.tradable:
            lg.info("Asset exists and is tradable")
            return True
        else:
            lg.info("Asset exists but not tradable")
            return False
    except Exception as e:
        lg.error("Asset does not exists or something happend!")
        lg.error(e)
        sys.exit()

# execute trading bot this function is the main and will ex all the algorithm from traderlib.py
def main():
    
    api= tradeapi.REST(key_id=gvars.API_KEY, secret_key=gvars.API_SECRET_KEY, base_url=gvars.API_URL, api_version="v2")

   
    # initialize the logger (imported from logger)
    initialize_logger()

      
    # check if the account is ok
    check_account_ok(api)

     
    # close current order
    clean_open_orders(api)
    #define asset insert the value/ get the ticker
    
    ticker = input("Write the ticker you want to operate with")
    
    check_asset_ok(api, ticker) # we make sure that the asset has a ticker-ex TSLA for tesla, 
                        #not to have a fake ticker or with error because if so the boot will say that it didnt found open pos for that wrong tiker and 
                        #it will run operations for it and we dont want this!


    trader = Trader(ticker, api) #initialize trading bot

    while True:
        tradingSuccess = trader.run(ticker) #run trading bot library 
            # in: string (ticker)
            # OUT: boolean (Tru = succes / False = failure)

        if not tradingSuccess:
            lg.info("Trading was not successful, locking asset")
            time.sleep(gvars.sleepTimeME)
            # wait some time
        else:
            lg.info("Trading was succesful!")
            time.sleep(gvars.sleepTimeME)
            # wait some time


if __name__ == "__main__":
    main()