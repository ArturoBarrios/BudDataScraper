from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from LEAFLY_SCRAPE import LEAFLY

import time
driver = webdriver.Chrome('/Users/arturobarrios/Documents/BudRecommender/chromedriver')
driver.get("https://www.leafly.com/strains")

delay = 3 # seconds

#initialize Leafly class with driver
leafly = LEAFLY(driver)
leafly.agebypass()
time.sleep(2)
bud_data = []
get_next_page = 1
while(get_next_page):
    hyperlinks = leafly.getAllHyperlinks()
    i = 0
    for hyperlink in hyperlinks:
        # if(i<2):
        leafly.open_new_leafly_tab(hyperlink)
        data = leafly.extractBudData()
        bud_data.append(data)
        leafly.close_tab(-1)
        i+=1
    get_next_page = leafly.get_next_page()

print("bud data: ",bud_data)






