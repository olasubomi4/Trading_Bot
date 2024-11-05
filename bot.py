import requests
from bs4 import BeautifulSoup
import time
import os
from binance.client import Client


API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
client = Client(API_KEY, API_SECRET)

def get_crypto_price(crypto='bitcoin'):
    url = f'https://coinmarketcap.com/currencies/{crypto}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    price_tag = soup.find('span', class_='sc-65e7f566-0 WXGwg base-text')
    if price_tag:
        price = price_tag.text.replace('$', '').replace(',', '')
        return float(price)
    else:
        print("Could not find the price.")
        return None

def purchase_crypto(symbol, amount):
    try:
        order = client.order_market_buy(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=amount
        )
        if order and order['status'] == 'FILLED':
            print("Purchase successful:", order)
        else:
            print("Purchase not successful:", order)
    except Exception as e:
        print("An error occurred while purchasing:", e)

def get_balance(asset):
    try:
        balance = client.get_asset_balance(asset)
        return balance
    except Exception as e:
        print("An error occurred while fetching the balance:", e)
        return None


def main():
    crypto = 'bitcoin'
    threshold = 68000.0  # Set your desired threshold price
    amount_to_purchase = 0.01  # Amount of crypto to purchase
    print("Your balance is %s" %get_balance("BTC"))

    while True:
        price = get_crypto_price(crypto)
        if price is not None:
            print(f"Current {crypto} price: ${price}")

            if price <= threshold:
                purchase_crypto('BTCUSDT', amount_to_purchase)
                break

        time.sleep(1)

if __name__ == "__main__":
    main()