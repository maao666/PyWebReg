from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
import os
import logging
import traceback
from time import sleep
from ._exceptions import *

__all__ = ['WebReg']


class WebReg(object):
    from ._utils import _pause, _wait_until_present
    from ._study_list import get_study_list, _show_study_list, _get_table_title
    from ._study_list import _get_table_HTML, _parse_table_HTML
    from ._operation import _goto_enrollment, _goto_waitlist, _check_operation_status
    from ._operation import _send_enrollment_request, _send_waitlist_request

    #driver = None
    timeout = 10

    def __init__(self, URL='https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh', headless=True, window_size=(1366, 768), debug=False):
        self.debug = debug
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--disable-extensions")
        if headless:
            chrome_options.add_argument("--headless")
        #chrome_options.binary_location = "/usr/bin/chromium"
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(
            window_size[0], window_size[1], self.driver.window_handles[0])
        self.driver.get(URL)
        if self.debug:
            logging.info('Current URL: {}'.format(self.driver.current_url))
            logging.info('Get title: {}'.format(self.driver.title))

    def __del__(self):
        if self.debug:
            logging.warning('Auto logout has been disabled in debug mode')
        else:
            if not self.get_logout_status():
                self.logout(suppress_warning=True)
            self.driver.close()
            logging.info("Driver has been closed.")

    def login(self, username: str, password: str, username_textbox_id='ucinetid', password_textbox_id='password', login_button_name='login_button'):
        '''
        Login to WebReg
        ---

        returns the WebReg object
        :Args:
         - username - Your UCInetID Username
         - password - Your UCInetID password
        '''
        # Input Username
        self._wait_until_present(By.ID, username_textbox_id)
        textbox = self.driver.find_element_by_id(username_textbox_id)
        textbox.send_keys(username)

        # Input Password
        self._wait_until_present(By.ID, password_textbox_id)
        textbox = self.driver.find_element_by_id(password_textbox_id)
        textbox.send_keys(password)

        self._pause()

        # Click login button
        self._wait_until_present(By.NAME, login_button_name)
        button = self.driver.find_element_by_name(login_button_name)
        button.click()

        # Check if the page redirects
        button = self.driver.find_elements_by_name(login_button_name)
        if len(button) > 0:
            logging.error("Loggin Page Failed to Redirect")
            raise LoginFailedException(
                "Failed to login due to wrong username/passeord/account issue")
        return self

    def logout(self, class_name='WebRegLogoutButton', suppress_warning=False):
        '''
        Manually logout from WebReg
        ---

        This is not required normally because it will automatically logout 
        once the object gets purged.
        '''
        self._wait_until_present(By.CLASS_NAME, class_name)
        buttons = self.driver.find_elements_by_class_name(class_name)
        if len(buttons) > 0:
            buttons[0].click()
        else:
            if not suppress_warning:
                logging.warning("No Logout Button Found!")

    def get_page_title(self, title_class_name='WebRegTitle') -> str:
        self._wait_until_present(By.CLASS_NAME, title_class_name)
        title = self.driver.find_element_by_class_name(title_class_name)
        return title.text

    def check_err_msg(self, default='', err_msg_class_name='WebRegErrorMsg') -> str:
        msg_divs = self.driver.find_elements_by_class_name(err_msg_class_name)
        if len(msg_divs) > 0:
            logging.info(msg_divs[0].text)
            return msg_divs[0].text
        return default

    def get_logout_status(self, logout_msg_class='DivLogoutMsg'):
        '''Return True if logged out'''
        msg_divs = self.driver.find_elements_by_class_name(logout_msg_class)
        return len(msg_divs) > 0

    def add_course(self, course_code: str, letter_grade=True, variable_units=None, auth_code=None) -> int:
        '''
        Add a course to study list
        ---
        
        returns -1 if unsuccessful
        :Args:
         - course_code - 5-digit course code string that you want to add such as '16700'
         - letter_grade - (Optional, default True) True for letter grade course. Set to False for Pass/No Pass
         - variable_unit - (Optional) 1-digit string for variable unit. 
         - auth_code - (Optional) authorization code for enrolling in certain courses. 
        '''
        self._goto_enrollment()
        self._send_enrollment_request(
            'add', course_code, letter_grade=letter_grade, variable_units=variable_units, auth_code=auth_code)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Course Operation Failed: {}'.format(status))
            return -1
        return 0

    def change_course(self, course_code: str, letter_grade=True, variable_units=None, auth_code=None) -> int:
        '''
        Change an enrolled course
        ---
        
        returns -1 if unsuccessful
        :Args:
         - course_code - 5-digit course code string that you want to change such as '16700'
         - letter_grade - (Optional, default True) True for letter grade course. Set to False for Pass/No Pass
         - variable_unit - (Optional) 1-digit string for variable unit. 
         - auth_code - (Optional) authorization code for enrolling in certain courses. 
        '''
        self._goto_enrollment()
        self._send_enrollment_request(
            'change', course_code, letter_grade=letter_grade, variable_units=variable_units, auth_code=auth_code)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Course Operation Failed: {}'.format(status))
            return -1
        return 0

    def drop_course(self, course_code: str) -> int:
        '''
        Drop a course from study list
        ---
        
        returns -1 if unsuccessful
        :Args:
         - course_code - 5-digit course code string that you want to drop such as '16700' 
        '''
        self._goto_enrollment()
        self._send_enrollment_request('drop', course_code)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Course Operation Failed: {}'.format(status))
            return -1
        return 0

    def list_open_sections(self, course_code: str) -> list:
        '''
        List open sections for a course
        ---
        
        returns a list containing available sections.
        :Args:
         - course_code - 5-digit course code string such as '16700'
        '''
        self._goto_enrollment()
        self._send_enrollment_request('list open sections', course_code)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Course Operation Failed: {}'.format(status))
        try:
            return self.get_study_list()
        except:
            logging.warning('Seems no open section available')
            return []

    def add_waitlist(self, course_code: str, letter_grade=True, variable_units=None) -> int:
        '''
        Add a course to waitlist
        ---
        
        returns -1 if unsuccessful
        :Args:
         - course_code - 5-digit course code string that you want to add such as '16700'
         - letter_grade - (Optional, default True) True for letter grade course. Set to False for Pass/No Pass
         - variable_unit - (Optional) 1-digit string for variable unit. 
        '''
        self._goto_waitlist()
        self._send_waitlist_request(
            'add', course_code, letter_grade=letter_grade, variable_units=variable_units)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Waitlist Operation Failed: {}'.format(status))
            return -1
        return 0

    def drop_waitlist(self, course_code: str) -> int:
        '''
        Drop a course from waitlist
        ---
        
        returns -1 if unsuccessful
        :Args:
         - course_code - 5-digit course code string that you want to drop such as '16700'
        '''
        self._goto_waitlist()
        self._send_waitlist_request('drop', course_code)
        status = self._check_operation_status(default='ok')
        if not status == 'ok':
            logging.warning('Course Operation Failed: {}'.format(status))
            return -1
        return 0
