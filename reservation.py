from selenium import webdriver
import re
import datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException

PATH = '/usr/local/bin/chromedriver'
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

class Bot:
    #TODO: tune sleeps to improve performance


    def __init__(self):
        self.url = 'https://bge.agenda.ch/'
        self.driver = webdriver.Chrome(PATH)
        self.email = 'jbm.nantck@gmail.com'
        self.slot_template = '//*[@id="layout-content"]/div[2]/section/div[2]/div/div/div/div[2]/table/tbody/tr/td[{}]/div[{}]/button[{}]'
        self.iframe_xpath = '/html/body/div[6]/div[1]/iframe'

    def start(self):
        self.driver.get(self.url)

    def end(self):
        self.driver.quit()
    
    def find_sdl(self):
        self.driver.find_element_by_xpath('//*[@id="service-groups"]/div[2]').click()

    def click_on_slot(self, slot):
        self.driver.switch_to.frame(frame_reference=self.driver.find_element_by_id("agenda_iframe"))
        try:
            self.driver.find_element_by_xpath(slot).click()
            print("found it")
            return True
        except NoSuchElementException:
            print("slot not found")
            return False
    
    def enter_email(self):
        mail_form = '//*[@id="layout-content"]/div[2]/form/label/input'
        continue_button = '//*[@id="layout-content"]/div[2]/form/div[2]/button'
        self.driver.find_element_by_xpath(mail_form).send_keys(self.email)
        sleep(0.5)
        self.driver.find_element_by_xpath(continue_button).click()
 
    def accept_conditions(self):
        accept1 = '//*[@id="layout-content"]/div[2]/form/div[2]/div[1]/label'
        accept2 = '//*[@id="layout-content"]/div[2]/form/div[2]/div[2]/label'
        confirm_button = '//*[@id="layout-content"]/div[2]/form/div[3]/button'
        self.driver.find_element_by_xpath(accept1).click()
        self.driver.find_element_by_xpath(accept2).click()
        self.driver.find_element_by_xpath(confirm_button).click()

    def enter_mail_and_confirm(self):
        # 2 cases: 
        # 1) it already has you e-mail: only need to accept conditions
        # 2) fill out the whole form
        # we only handle case 1 for now
        self.enter_email()
        sleep(1)
        self.accept_conditions()
        sleep(0.5)
        return True
  
    def back_to_homepage(self):
        book_again = '//*[@id="layout-content"]/div[2]/div/a/button'
        try:
            self.driver.find_element_by_xpath(book_again).click()
            return True
        except NoSuchElementException:
            print("back_to_homepage: can't click on book again")

    #scripts:
    def book_one_slot(self, day, half_day, time):
        slot = self.slot_template.format(day, half_day, time)
        self.click_on_slot(slot)
        sleep(5)
        self.enter_mail_and_confirm()
        sleep(2)
        self.back_to_homepage()

    def reserver_all_slots(self):
        # TODO: handle already booked slots
        # TODO: navigate to next page in agenda
        # TODO: handle last case
        # TODO: handle start date

        for day in range(1,8):
            for half_day in range(1,3):
                if half_day == 1:
                    t = 2
                else:
                    t = 4
                for time in range (1,t+1):
                    try:
                        book_one_slot(day, half_day, time)
                    except NoSuchElementException:
                        print('reserver_all_slots: Time slot unavailable :(')

    def main(self):
        self.start()
        self.book_one_slot(1,2,3)
        self.end()



if __name__ == "__main__" :


    bot = Bot()
    bot.main()
