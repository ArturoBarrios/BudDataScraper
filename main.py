from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from LEAFLY_SCRAPE import LEAFLY

import time
driver = webdriver.Chrome('/Users/arturobarrios/Documents/BudRecommender/chromedriver')
# driver = webdriver.Chrome()
driver.get("https://www.leafly.com/strains")

delay = 3 # seconds

#initialize Leafly class with driver
leafly = LEAFLY(driver)
leafly.agebypass()
time.sleep(2)
leafly.nextPage()
time.sleep(2)

#create function that gathers all links on strains site(potentially grab strain info that's 
#displayed on front page)
#iterate through each hyperlink

#create function that gathers information for each

#click next page and do these steps over




