import requests
import bs4 as bs4
from splinter import Browser
import re
import datetime

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def check(email):
    if(re.search(regex, email)):
        print("Valid Email")
        return True
 
    else:
        print("Invalid Email")
        return False

def ask_email():
    email = 'not an email'
    while not check(email):
        email = input('Enter mail address')
    return email

def ask_date():
    today = datetime.today()
    start_day = 0
    while start_day != 0 and start_day > 31:
     start_day = input('Enter start day:')
    start_month = 0
    while start_month != 0 and start_month > 12:
     start_month = input('Enter start month:')
    start_date = datetime.date(start_day, start_month)
    in_seven_days = today + datetime.timedelta(days=6)
    if in_seven_days < start_date:
        return today, False
    end_date = in_seven_days
    return end_date, True


class Bot(self, **info):
    self.url = 'https://bge.agenda.ch/'
    self.info = info


    def init_browser(self):
        driver = self.info["driver"]
        if driver == "geckodriver":
            self.b = Browser()
    
    def step1(self):
        r = requests.get("{}".format(self.url)).text
        soup = bs4.BeautifulSoup(r, 'lxml')
        #trouver le bon bouton!!!

if __name__ == "__main__" :

    email = ask_email()
    worked = False
    start_date = datetime.today()
    while not worked:
        start_date, worked = ask_date()
        if not worked:
            print("invalid date please start over")


    INFO = {
        "driver": "geckodriver",
        "email": email,
        "start_date": start_date
    }

    bot = Bot(**INFO)
    bot.main()
