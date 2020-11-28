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
            yes_button.click()
            return 1
        except:
            print("agebypass button not found")
            time.sleep(2)
            return 0
    
    def nextPage(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '//a[text()="Next"]') 
            next_button.click()
            return 1
        except:
            print("nextPage button not found")
            time.sleep(2)
            return 0

    def getAllCards(self):
        cards = None
        try:
            cards = self.driver.find_elements_by_class_name('carousel-card--quadruplet')
            print("cards: ", len(cards))
        except:
            print("cards not found")
        return cards
