import datetime as dt
import random
from smtplib import SMTP, SMTPAuthenticationError

MY_EMAIL = ""
MY_PASSWORD = ""
RECEIVER_EMAIL = ""

now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:
    with open("quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)

    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()

        try:
            connection.login(MY_EMAIL, MY_PASSWORD)
        except SMTPAuthenticationError:
            print("Invalid credentials")
        else:
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=RECEIVER_EMAIL,
                msg=f"Subject:Monday Motivation\n\n{quote}"
            )
