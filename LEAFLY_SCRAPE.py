from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


import time
class LEAFLY:
    def __init__(self,driver):
        self.driver = driver
    
    def get_feelings(self,contains_text, effect_section):
        feelings = effect_section.find_elements_by_xpath("//span[contains(text(),'"+contains_text+"')]")
        i = 0
        #positive and negative feelings
        for feeling in feelings:
            feelingx_text = feelings[i].text
            feelingx_text = feelingx_text.replace("%", "")
            print("feeling text: ", feelingx_text)
            #percentage
            feelingx_val = [int(s) for s in feelingx_text.split() if s.isdigit()][0]
            print("feeling 1: ", feelingx_val)
            parsed_feelingx_text = feelingx_text.split()
            feelingx = parsed_feelingx_text[-1]
            print("feelingx: ", feelingx)
            i+=1

    def extractBudData(self):
        # data_element = self.driver.find_element_by_id('strain-card-data')
        content = self.driver.find_element_by_css_selector("div#strain-card-data")

        print("data_element: ", content)
        children_list = content.find_elements_by_tag_name('div')
        sub1_children = children_list[0].find_elements_by_tag_name('span')
        strain_type = sub1_children[0].text#
        strain_potency = sub1_children[1].text#
        print("content: ", strain_type,"   ", strain_potency)
        strain_name = content.find_elements_by_tag_name('h1')[0].text#
        strain_secondary_name = content.find_elements_by_tag_name('h2')[0].text#
        print("names: ", strain_name, "   ",strain_secondary_name)
        #parse secondary name
        review_content = content.find_element_by_class_name('pb-sm')
        review_content = review_content.find_elements_by_tag_name("span")
        rating = review_content[0].text#
        num_of_ratings = review_content[2].text#
        num_of_ratings = num_of_ratings[1:len(num_of_ratings)-1]
        print("green content: ", rating,"    ", num_of_ratings)

        calm_enrgy_content = content.find_element_by_class_name("calm-energize__mark")
        calm_enrgy = calm_enrgy_content.get_attribute("style")
        #percentage
        calm_enrgy = calm_enrgy[11:len(calm_enrgy)-2]
        print("cccc: ", calm_enrgy)
        #description
        description = content.find_element_by_class_name('strain__description').find_element_by_tag_name('p').text
        print("description: ", description)
        #effect section################
        effect_section = self.driver.find_element_by_id('strain-effects-section')
        print("effect section: ", effect_section)
        reported_effects = effect_section.find_elements_by_tag_name('div')
        print("reported effects: ", reported_effects[2].text)
        self.get_feelings('of people report feeling',effect_section)
        self.get_feelings('people say it helps with', effect_section)
        

    def agebypass(self):
        try:
            yes_button = self.driver.find_element(By.XPATH, '//button[text()="yes"]')
            yes_button.click()
            return 1
        except:
            print("agebypass button not found")
            return 0
    
    def nextPage(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '//a[text()="Next"]') 
            next_button.click()
            return 1
        except:
            print("nextPage button not found")
            return 0

    def getAllHyperlinks(self):
        hyperlinks = []
        try:
            cards = self.driver.find_elements_by_class_name('carousel-card--quadruplet')
            for card in cards: 
                href = card.find_element_by_class_name('relative').get_attribute("href")
                hyperlinks.append(href)
        except:
            print("cards not found")
        return hyperlinks

    def open_new_leafly_tab(self,hyperlink):
        self.driver.execute_script("window.open('');")
        time.sleep(3)
        Window_List = self.driver.window_handles
        self.driver.switch_to_window(Window_List[-1])
        self.driver.get(hyperlink)

    def close_tab(self,tab_index):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[tab_index])

