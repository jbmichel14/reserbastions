from selenium import webdriver
import re
import datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException

PATH = '/usr/local/bin/chromedriver'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
slot_template = '//*[@id="layout-content"]/div[2]/section/div[2]/div/div/div/div[2]/table/tbody/tr/td[{}]/div[{}]/button[{}]'
iframe_xpath = '/html/body/div[6]/div[1]/iframe'
a_slot = '//*[@id="layout-content"]/div[2]/section/div[2]/div/div/div/div[2]/table/tbody/tr/td[6]/div[2]/button[3]'




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

    def __init__(self):
        self.url = 'https://bge.agenda.ch/'
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(self.url)
        self.email = 'jbm.nantck@gmail.com'


    def end(self):
        self.driver.quit()
    
    def find_reserver_sdl(self):
        self.driver.find_element_by_xpath('//*[@id="service-groups"]/div[2]').click()


    def click_on_a_slot(self, slot):
        #l = self.driver.find_elements_by_class_name('timeButton-0-2-82 ')
        #t = '#layout-content > div:nth-child(2) > section > div.availabilityBox-0-2-71.box-0-2-25.cardBox-0-2-21.paddedBox-0-2-22 > div > div > div > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > div:nth-child(2) > button:nth-child(3)'
        #self.driver.find_elements_by_css_selector(t)[0].click()
        #self.driver.find_element_by_id("root")
        self.driver.switch_to.frame(frame_reference=self.driver.find_element_by_id("agenda_iframe"))
        self.driver.find_element_by_xpath(slot).click()
        print("found it")
    
    def enter_mail_and_confirm(self, last=False):
        mail_form = '//*[@id="layout-content"]/div[2]/form/label/input'
        continue_button = '//*[@id="layout-content"]/div[2]/form/div[2]/button'
        accept1 = '//*[@id="layout-content"]/div[2]/form/div[2]/div[1]/label'
        accept2 = '//*[@id="layout-content"]/div[2]/form/div[2]/div[2]/label'
        confirm_button = '//*[@id="layout-content"]/div[2]/form/div[3]/button'
        new_rdv = '//*[@id="layout-content"]/div[2]/div/a/button'

        case = 1
        # 2 cases: 
        # 1 it already has you e-mail: only need to accept conditions
        # 2 fill out the whole form
        # we only handle case one for now

        self.driver.find_element_by_xpath(mail_form).send_keys(self.email)

        sleep(0.5)
    
        if case == 2:
            self.case2()

        self.driver.find_element_by_xpath(continue_button).click()
        sleep(2)
        self.driver.find_element_by_xpath(accept1).click()
        sleep(0.5)
        self.driver.find_element_by_xpath(accept2).click()
        sleep(0.5)
        self.driver.find_element_by_xpath(confirm_button).click()
        #sleep(0.5)
        #if not last:
            #self.driver.find_element_by_xpath(new_rdv).click()
        

    def case2(self):
        return True

    
    def reserver_one_slot(self, day, half_day, time):
        slot = slot_template.format(day, half_day, time)
        self.driver.find_element_by_xpath(slot).click()
        sleep(5)
        self.enter_mail_and_confirm(False)


    def reserver_all_slots(self):
        for day in range(1,8):
            for half_day in range(1,3):
                if half_day == 1:
                    t = 2
                else:
                    t = 4
                for time in range (1,t+1):
                    try:
                        self.reserver_one_slot(day, half_day, time)
                    except NoSuchElementException:
                        print('Time slot unavailable :( Va falloir faire une fausse')
        #then : need to navigate to next page


    def main(self):
        sleep(1)
        self.find_reserver_sdl()
        sleep(5)
        #self.reserver_all_slots()
        self.click_on_a_slot(a_slot)
        sleep(3)
        self.enter_mail_and_confirm()
        self.end()


def script():
    for half_day in range(1,3):
        if half_day == 1:
            t = 2
        else:
            t = 4
            for time in range (1,t+1):
                try:
                    slot = slot_template.format(7, half_day, time)
                    bot = Bot(slot)
                    bot.main()
                        
                except NoSuchElementException:
                    print('Time slot unavailable :( Va falloir faire une fausse')


if __name__ == "__main__" :

    """ email = ask_email()
    worked = False
    start_date = datetime.today()
    while not worked:
        start_date, worked = ask_date()
        if not worked:
            print("invalid date please start over")
    """

    bot = Bot()
    bot.main()
