from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
import os
import logging
from time import sleep


def _pause(self, ms_min=100, ms_max=800):
    sleep(randint(ms_min, ms_max) * 0.001)


def _wait_until_present(self, by: str, element_name: str):
    element_present = EC.presence_of_element_located(
        (by, element_name))
    WebDriverWait(self.driver, self.timeout).until(element_present)
