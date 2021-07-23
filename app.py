import os
from dotenv import load_dotenv
import requests
import alpaca_trade_api as tradeapi
import pandas as pd


# def trade_bot(symbol, drop_tick, raise_tick):
    # holding_df = holdings_df[holdings_df.ticker == list(trading_dict.keys())[j]]
    # if holding_df['percent_change'].astype('float32')[0] <= drop_tick:
    #     buy_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
    #     print(buy_string)
    #     r.orders.order_buy_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
    # else:
    #     print('Nothing to buy')

    # if holding_df['percent_change'].astype('float32')[0] >= raise_tick:
    #     sell_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
    #     print(sell_string)
    #     r.orders.order_sell_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
    # else:
    #     print('Nothing to sell')

# def build_df(assets):
#     df = pd.DataFrame()
#     for asset in assests:
#         print(assest.keys())

#helper function to check if you can trade the desired stock
def can_trade(api, symbol):
    # Check if the market is open now.
    clock = api.get_clock()
    if not clock.is_open:
        print('Market currently closed')
        return False

    # Check if desired stock is tradable
    aapl_asset = api.get_asset(symbol)
    if not aapl_asset.tradable:
        return False

    return True

if __name__ == '__main__':
    load_dotenv()   #load hidden variables
    #Alpaca API connection
    api = tradeapi.REST(
        os.getenv('APCA_API_KEY_ID'),
        os.getenv('APCA_API_SECRET'),
        'https://paper-api.alpaca.markets'
    )

    # Get account info
    account = api.get_account()
    if account.trading_blocked:
        print('Warning: Account currently unable to trade')
    print(account)
    
    print('${} is available as buying power.'.format(account.buying_power))
    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')

    #List out all of our positions.
    print("current portfolio:")
    portfolio = api.list_positions()
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
        #Get daily price data for AAPL over the last 5 trading days.
        barset = api.get_barset(position.symbol, 'day', limit=5)
        bars = barset[position.symbol]

        # See how much AAPL moved in that timeframe.
        week_open = bars[0].o
        week_close = bars[-1].c
        percent_change = (week_close - week_open) / week_open * 100
        print(position.symbol,' moved {}% over the last 5 days'.format(percent_change))

    #Get all active NASDAQ assets.
    active_assets = api.list_assets(status='active')
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    
    will_buy = input("would you like to buy any stocks (yes to buy, anything else to skip)")
    if will_buy.lower() == 'y':
        sym = input("which stocks would like to buy (input the nasdaq stock symbol)")
        if can_trade(api, sym.upper()):
            num = input("how much would you like to buy?")
            api.submit_order(
                symbol=sym.upper(),
                qty=num,
                side='buy',
                type='market',
                time_in_force='gtc'
            )      
        else:
            print("unable to to trade this stock")

    will_sell = input("would you like to sell any stocks (yes to sell, anything else to skip)")
    if will_sell.lower() == 'y':
        sym = input("which stocks would like to buy (input the nasdaq stock symbol)")
        if can_trade(api, sym.upper()):
            num = input("how much would you like to sell?")
            api.submit_order(
                symbol=sym.upper(),
                qty=num,
                side='buy',
                type='market',
                time_in_force='gtc'
            )      
        else:
            print("unable to to trade this stock")



