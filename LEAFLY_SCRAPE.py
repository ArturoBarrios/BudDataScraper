from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


import time
class LEAFLY:
    def __init__(self,driver):
        self.driver = driver

    def agebypass(self):
        try:
            yes_button = self.driver.find_element(By.XPATH, '//button[text()="yes"]')
            # String typeOfElement = someElement.getAttribute("type"); 
            yes_button.click()
            return 1
        
        except:
            print("disabled button")
            time.sleep(2)
            return 0
    
    def nextPage(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '//a[text()="Next"]')
            # String typeOfElement = someElement.getAttribute("type"); 
            next_button.click()
            return 1
        
        except:
            print("disabled button")
            time.sleep(2)
            return 0
