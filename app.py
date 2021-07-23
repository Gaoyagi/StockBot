import os
from dotenv import load_dotenv
import requests
import alpaca_trade_api as tradeapi
import pandas as pd

if __name__ == '__main__':
    """
    With the Alpaca API, you can check on your daily profit or loss by
    comparing your current balance to yesterday's balance.
    """
    load_dotenv()
    # First, open the API connection
    api = tradeapi.REST(
        os.getenv('APCA_API_KEY_ID'),
        os.getenv('APCA_API_SECRET'),
        'https://paper-api.alpaca.markets'
    )

    # Get account info
    account = api.get_account()

    if account.trading_blocked:
        print('Account is currently restricted from trading.')
    
    print('${} is available as buying power.'.format(account.buying_power))
