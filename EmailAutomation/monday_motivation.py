import datetime as dt
import random
import os
from smtplib import SMTP, SMTPAuthenticationError

SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD =  os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)

    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()

        try:
            connection.login(SENDER_EMAIL, SENDER_PASSWORD)
        except SMTPAuthenticationError:
            print("Invalid credentials")
        else:
            connection.sendmail(
                from_addr=SENDER_EMAIL,
                to_addrs=RECEIVER_EMAIL,
                msg=f"Subject:Monday Motivation\n\n{quote}"
            )
