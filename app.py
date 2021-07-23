import os
from dotenv import load_dotenv
import requests
import alpaca_trade_api as tradeapi
import pandas as pd

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

    #Get all active NASDAQ assets.
    active_assets = api.list_assets(status='active')
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    
    print("which stocks would  ")

  

    # Get daily price data for AAPL over the last 5 trading days.
    # barset = api.get_barset('AAPL', 'day', limit=5)
    # aapl_bars = barset['AAPL']

    # # See how much AAPL moved in that timeframe.
    # week_open = aapl_bars[0].o
    # week_close = aapl_bars[-1].c
    # percent_change = (week_close - week_open) / week_open * 100
    # print('AAPL moved {}% over the last 5 days'.format(percent_change))

    # Submit a market order to buy 1 share of Apple at market price
    # api.submit_order(
    #     symbol='AAPL',
    #     qty=1,
    #     side='buy',
    #     type='market',
    #     time_in_force='gtc'
    # )      



# def trade_bot(trading_dict):
#     for j in range(len(trading_dict)):
#         holding_df = holdings_df[holdings_df.ticker == list(trading_dict.keys())[j]]
#         if holding_df['percent_change'].astype('float32')[0] <= list(trading_dict.values())[j][0]:
#             buy_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
#             print(buy_string)
#             r.orders.order_buy_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
#         else:
#             print('Nothing to buy')

#         if holding_df['percent_change'].astype('float32')[0] >= list(trading_dict.values())[j][1]:
#             sell_string = 'Buying ' + str(holding_df['ticker'][0]) + ' at ' + time.ctime()
#             print(sell_string)
#             r.orders.order_sell_market(holding_df['ticker'][0],1,timeInForce= 'gfd')
#         else:
#             print('Nothing to sell')


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

def build_df(assets):
    df = pd.DataFrame()
    for asset in assests:
        print(assest.keys())
