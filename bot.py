# enconding: utf-8

# import needed libraries
from traderlib import *
from logger import *
import sys
import gvars
import alpaca_trade_api as tradeapi



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
    import pdb; pdb.set_trace()
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