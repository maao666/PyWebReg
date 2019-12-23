from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ._exceptions import NoElementException
import logging


def _goto_enrollment(self, xpathes=("//input[@value='Enrollment Menu']", "//input[@value='Go to Enrollment Menu']")):
    if self.get_page_title().find('Enrollment Menu') != -1:
        return
    for xpath in xpathes:
        button = self.driver.find_elements_by_xpath(xpath)
        if len(button):
            button[0].click()
            return
    raise NoElementException('No Enrollment Button Found')


def _goto_waitlist(self, xpathes=("//input[@value='Wait list Menu']", "//input[@value='Go to Wait List Menu']")):
    if self.get_page_title().find('Wait List Menu') != -1:
        return
    for xpath in xpathes:
        button = self.driver.find_elements_by_xpath(xpath)
        if len(button):
            button[0].click()
            return
    raise NoElementException('No Wait List Button Found')


def _send_enrollment_request(self, operation: str, course_code: str, letter_grade=True, variable_units=None, auth_code=None):
    # Radio
    xpath = {'add': "//input[@id='add'][@type='radio']",
             'change': "//input[@id='change'][@type='radio']",
             'drop': "//input[@id='drop'][@type='radio']",
             'list open sections': "//input[@id='listOpen'][@type='radio']"}
    self.driver.find_element_by_xpath(xpath[operation]).click()

    # Course Code
    xpath = "//input[@name='courseCode'][@type='text']"
    for box in self.driver.find_elements_by_xpath(xpath):
        box.send_keys(course_code.strip())

    # Grade Option
    xpath = "//input[@name='gradeOption'][@type='text']"
    self.driver.find_element_by_xpath(
        xpath).send_keys('1' if letter_grade else '2')

    # Var Units
    if isinstance(variable_units, str):
        xpath = "//input[@name='varUnits'][@type='text']"
        self.driver.find_element_by_xpath(xpath).send_keys(variable_units)

    # Auth Code
    if isinstance(auth_code, str):
        xpath = "//input[@name='authCode'][@type='text']"
        self.driver.find_element_by_xpath(xpath).send_keys(auth_code)
    # Button
    xpath = "//input[@value='Send Request'][@type='submit']"
    self.driver.find_element_by_xpath(xpath).click()


def _send_waitlist_request(self, operation: str, course_code: str, letter_grade=True, variable_units=None):
    # Radio
    xpath = {'add': "//input[@id='add'][@type='radio']",
             'drop': "//input[@id='drop'][@type='radio']"}
    self.driver.find_element_by_xpath(xpath[operation]).click()

    # Course Code
    xpath = "//input[@name='courseCode'][@type='text']"
    for box in self.driver.find_elements_by_xpath(xpath):
        box.send_keys(course_code.strip())

    # Grade Option
    xpath = "//input[@name='gradeOption'][@type='text']"
    self.driver.find_element_by_xpath(
        xpath).send_keys('1' if letter_grade else '2')

    # Var Units
    if isinstance(variable_units, str):
        xpath = "//input[@name='varUnits'][@type='text']"
        self.driver.find_element_by_xpath(xpath).send_keys(variable_units)

    # Button
    xpath = "//input[@value='Send Request'][@type='submit']"
    self.driver.find_element_by_xpath(xpath).click()


def _check_operation_status(self, default='ok'):
    err_msg = self.check_err_msg()
    if err_msg != '' and err_msg.find('N O T E') == -1:
        logging.info('Course operation unsuccessful')
        return err_msg
    logging.info('Operation Status Appears OK')
    return default
