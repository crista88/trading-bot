# define asset
    # IN : keyboard
    # OUT: string

# LOOP UNTIL TIMEOUT REACHED (EX 2H)
    # POINT ECHO: INITIAL CHECK
    # check the position : ask the API/broker if we have an open position with "asset"
        # will be function with IN: asset as string // OUT :True(if exists) /False(does not exists)

    # check if tradable : ask the API/broker if "asset" is tradable
        # will be function with IN: asset as string // OUT :True(if exists) /False(does not exists)

    # GENERAL TREND
    # load 30 min data/candles: demand API the 30 min candles
        # IN: asset (what the PI needs like time range for ex or candle size)
        # OUT: 30 min candle(OHLC all the data for every candle)

    # perform general trend analysis : analyse if the trend is fav(detect interesting trend find if the trend is UP or DOWN or NO TREND)
        # IN : 30 min candle data (i will see what from the data i will need,  probably the last value that it had-close data)
        # OUT : UP/DOWN/NO TREND as strings  if no trend we go back to asset
        # IF NO TREND GO BACK TO POINT ECHO

    # LOOP until timeout reached(ex 30 min)
        #POINT DELTA
        # this loop will be as serial every condition has to be filled in cascade,
        # this loop is part of a bigger loop that includes DEFINE ASSET+INITIAL CHECK+GENERAL TREND

    # STEP 1: load 5 min data/candle
        # IN: asset (what the PI needs like time range for ex or candle size)
        # OUT: 5 min candle(OHLC all the data for every candle)
        # if failed go back to POINT DELTA

    # STEP 2: perfom instant trend analysis : we know what are we looking for regardind the direction of the trend up/down/no trend//
                                    # confirm the trend detected by general trend analyses
        # IN : 5 min candle data (i will see what from the data i will need,  probably the last value that it had-close data)
        # OUT : True as confirmed or False as not confirmed
        # if failed go back to POINT DELTA

    # STEP 3: perfom RSI analysis
        # IN : 5 min candle data (i will see what from the data i will need,  probably the last value that it had-close data)
        # OUT : True as confirmed or False as not confirmed
        # if failed go back to POINT DELTA

    # STEP 4: perfom stochastic analysis
        # IN: 5 min candle(OHLC all the data for every candle)
        # OUT : True as confirmed or False as not confirmed
        # if failed go back to POINT DELTA


# SUBMIT ORDER- this is a limit order
# submit the order : interact with broker API
    # IN: number of shares that we want to operate with from the asset, desired price
    # OUT: True as confirmed / False as not confirmed , we should get out position ID
    # if false abort, OR go back to POINT ECHO

# check position: see if the position exists
    # IN : pass the position ID
    # OUT : True as confirmed / False as not confirmed
    # if false abort, OR  go back to POINT ECHO

# ENTER POSITION MODE - LOOP UNTIL TIMEOUT REACHED EX 7-8 H # check the filters in parallel so if ay of them is cheked out we GET OUT
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


# GET OUT
    # SUBMIT ORDER- closing position/ sell what we have/ market order
    # submit the order : interact with broker API
        # IN: number of shares that we want to operate with from the asset, position id that we want to close because is a closing pos actualy
        # OUT: True as confirmed / False as not confirmed , we should get out position ID
        # if false retry until it workes because we want to sell
    # check position: see if the position exists
        # IN : pass the position ID
        # OUT : True as still exists / False as not exists
        # if false abort, OR  go back to submit order


# wait 15 min

# end / back to beggining
