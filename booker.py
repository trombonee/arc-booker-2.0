import os, sys
sys.path.append(os.getcwd())

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from links import links
from datetime import datetime, timedelta, time, date
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

class Booker(object):

    def __init__(self, booking_day: date, booking_time: time, username: str, password: str, zone: str='lower-squatrack'):

        self.booking_info = None
        if type(booking_day) is date and type(booking_time) is time:
            self.booking_info = datetime.combine(booking_day, booking_time)
        else:
            logging.info('Ensure booking_day is of type date and booking_time is of type time')
            raise ValueError('Ensure booking_day is of type date and booking_time is of type time')
        
        self.booking_link = None
        if zone in links.keys():
            self.booking_link = links[zone]
        else:
            logging.info('Ensure zone is in dictionary of links')
            raise ValueError('Ensure zone is in dictionary of links')

        self.username = username
        self.password = password

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def book(self) -> None:
        if self.booking_info:
            self.driver.get(self.booking_link)
            tmp = self.acknowledge_cookies()

            tmp = self.login() if tmp else False
            tmp = self.find_booking_time() if tmp else False
            tmp = self.accept_waiver() if tmp else False
            tmp = self.checkout() if tmp else False

            if tmp:
                print(str(datetime.now()), 'Successfully booked for user: {}'.format(self.username))
                logging.info('Successfully booked for user: {}'.format(self.username))
            

    def login(self) -> bool:
        try:
            login_script = self.driver.find_element_by_id('loginLink').get_attribute('href')
            self.driver.execute_script(login_script)

            login_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                        (   By.CSS_SELECTOR, 
                            'button.loginOption.btn.btn-lg.btn-block.btn-social.btn-soundcloud'
                        )))

            login_button.click()
            print(str(datetime.now()), 'Found login page')
            logging.info('Found login page')
            return self.fill_login_form()
        except Exception as e:
            print(str(datetime.now()), 'Error when trying to login to webpage')
            logging.error('Error when trying to login to webpage')
            logging.error(str(e))
            return False
         
    def fill_login_form(self) ->  bool:
        try:
            signon_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (   By.CSS_SELECTOR,
                        'button.form-element'
                    )
                ))
            self.driver.find_element_by_id('username').send_keys(self.username)
            self.driver.find_element_by_id('password').send_keys(self.password)
            signon_button.click()
            print(str(datetime.now()), 'Filled log in form')
            logging.info('Filled log in form')
            WebDriverWait(self.driver, 5).until(EC.url_contains('getactive'))
            return True

        except Exception as e:
            print(str(datetime.now()), 'Error filling in log in form, ensure login credentials are correct')
            logging.error('Error filling in log in form, ensure login credentials are correct')
            logging.error(str(e))
            return False
    
    def find_booking_time(self) -> bool:
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'schedule-heading')))
            register_buttons = self.driver.find_elements_by_css_selector('button.btn.btn-primary')
            available_times = []
            for button in register_buttons:
                try:
                    available_time = button.get_attribute('onClick').split("'")[7]
                    time_slot = datetime.strptime(available_time, '%m/%d/%Y %I:%M:%S %p')
                    available_times.append(time_slot)
                    if self.booking_info == time_slot:
                        button.click()
                        print(str(datetime.now()), 'Found booking time')
                        logging.info('Found booking time')
                        return True
                except:
                    pass
            print(str(datetime.now()), 'Booking time could not be found')
            logging.warning('Booking time could not be found')
            # To send text to user offering other booking times
            return False
        except Exception as e:
            print(str(datetime.now()), 'Could not load booking times')
            logging.error('Could not load booking times')
            logging.error(str(e))
            return False
        
    
    def accept_waiver(self) -> bool:
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.ID, 'loading')))
            accept_button = self.driver.find_element_by_id('btnAccept')
            accept_button.click()
            print(str(datetime.now()), 'Accepted waiver')
            logging.info('Accepted waiver')
            return True
        except Exception as e:
            print(str(datetime.now()), 'Could not accept waiver')
            logging.error('Could not accept waiver')
            logging.error(str(e))
            return False
    
    def checkout(self) -> bool:
        try:
            checkout_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'checkoutButton')))
            checkout_button.click()
        except Exception as e:
            print(str(datetime.now()), 'Could not press checkout button')
            logging.error('Could not press checkout button')
            logging.error(str(e))
            return False
        
        try:
            payment_button = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.card-item-main:nth-child(3)')))
            payment_button.click()
            print(str(datetime.now()), 'Checked out')
            logging.info('Checked out')
            return True
        except Exception as e:
            print(str(datetime.now()), 'Could not press payment option')
            logging.error('Could not press payment option')
            logging.error(str(e))
            return False

    def acknowledge_cookies(self) -> bool:
        try:
            cookies_accept = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'gdpr-cookie-accept')))
            cookies_accept.click()
            print(str(datetime.now()), 'Cookies accepted')
            logging.info('Cookies accepted')
            return True
        except Exception as e:
            print(str(datetime.now()), 'Could not accept cookies')
            logging.error('Could not accept cookies')
            logging.error(str(e))
            return False

if __name__ == '__main__':
    booking_day = datetime.date(datetime.now() + timedelta(days=3))
    booking_time = time(7, 45)
    booker = Booker(booking_day, booking_time)
    booker.book()
