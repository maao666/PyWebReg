from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


def _show_study_list(self, xpath="//input[@value='Show Study List']"):
    self._wait_until_present(By.XPATH, xpath)
    button = self.driver.find_element_by_xpath(xpath)
    button.click()

def _show_wait_list(self, xpath="//input[@value='Show Wait List']"):
    self._wait_until_present(By.XPATH, xpath)
    button = self.driver.find_element_by_xpath(xpath)
    button.click()


def _get_table_HTML(self, class_name="studyList", keyword='table') -> str:
    self._wait_until_present(By.CLASS_NAME, class_name)
    for table in self.driver.find_elements_by_class_name(class_name):
        outer_HTML = table.get_attribute('outerHTML')
        if not outer_HTML.find(keyword) == -1:
            return outer_HTML


def _parse_table_HTML(self, html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    rows = [i.strip() for i in text.split('\n') if not i.strip() == '']
    course_list = []
    if text.find('no classes')==-1:
        courses = [i for i in rows if not re.match(
            r'^\d\d\d\d\d', i.strip()) == None]
        course_list = [[0 for y in range(3)] for x in range(len(courses))]
        for i in range(len(courses)):
            courses[i] = list(filter(None, courses[i].split(" ")))
            course_list[i] = courses[i][0:3]
    return {'title': rows[0], 'body': course_list}


def get_study_list(self) -> list:
    return self._parse_table_HTML(self._get_table_HTML())['body']


def _get_table_title(self) -> str:
    return self._parse_table_HTML(self._get_table_HTML())['title']
