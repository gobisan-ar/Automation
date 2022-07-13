import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

sender = os.environ.get('SENDER_NUMBER')
receiver = os.environ.get('RECEIVER_NUMBER')

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, stock_params)

data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Get yesterday's closing price
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

# Get day before yesterday's closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = float(day_before_yesterday_data["4. close"])

# Closing price difference
difference = yesterday_closing_price - day_before_yesterday_data_closing_price

indicator = None

if difference > 0:
    indicator = "🔺"
else:
    indicator = "🔻"

# Closing price difference percentage
diff_percent = round((difference / yesterday_closing_price)) * 100

# If diff percent is significant get news
if abs(diff_percent) > 0.5:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]

    # first three articles
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {indicator}{diff_percent}%\nHeadline: {article['title']} \nBrief: {article['description']}" for article in three_articles]

    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=sender,
            to=receiver
        )
