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
    
    print('${} is available as buying power.'.format(account.buying_power))
    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')

    #Get all active NASDAQ assets.
    active_assets = api.list_assets(status='active')
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    for asset in nasdaq_assets:
        print(asset)
  

    
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

# def build_df(assets):
#     df = pd.DataFrame()
