from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


import time
class LEAFLY:
    def __init__(self,driver):
        self.driver = driver
    
    def get_next_page(self):
        try:
            next_page_element = self.driver.find_element(By.XPATH, '//a[text()="Next"]').get_attribute("href")
            self.driver.get(next_page_element)
            return 1
        except:
            return 0

    
    def get_feelings(self,contains_text, effect_section):
        feelings = effect_section.find_elements_by_xpath("//span[contains(text(),'"+contains_text+"')]")
        i = 0
        feelings_arr = {}
        #positive and negative feelings
        for feeling in feelings:
            feelingx_text = feelings[i].text
            feelingx_text = feelingx_text.replace("%", "")
            # print("feeling text: ", feelingx_text)
            #percentage
            feelingx_val = [int(s) for s in feelingx_text.split() if s.isdigit()][0]
            # print("feeling 1: ", feelingx_val)
            parsed_feelingx_text = feelingx_text.split()
            feelingx = parsed_feelingx_text[-1]
            # print("feelingx: ", feelingx)
            i+=1
            feelings_arr[feelingx] = feelingx_val
        return feelings_arr

    def extractBudData(self):
        strain_name = ""
        strain_secondary_name = ""
        strain_picture_url = ""
        strain_type = ""
        strain_potency = ""
        calm_enrgy = ""
        rating = ""
        num_of_ratings = ""
        description = ""
        people_reporting_effects = ""
        num_of_effect_reports = ""
        stars = ""
        feelings_dict = {}
        review_data = []
        written_reviews_count = ""

        bud_data = {"name": "","image":"", "secondary_name":"","strain_type":"","potency":"","calm_enrgy":"","stars":"","reviews_count":"","description":"","people_reporting_effects": "", "reported_effects_count": "","effects": {},"review_data":[],"written_reviews_count":0}
        # data_element = self.driver.find_element_by_id('strain-card-data')
        content = None
        try:
            content = self.driver.find_element_by_css_selector("div#strain-card-data")
            console.log("content: ", content)

        except:
            print("couldnt get content", strain_name)
        if(content != None):
            try:
                children_list = content.find_elements_by_tag_name('div')
                sub1_children = children_list[0].find_elements_by_tag_name('span')
                strain_type = sub1_children[0].text#
                strain_potency = sub1_children[1].text[4:-1]#

            except:
                print("couldn't find strain type or strain potency", strain_name)
            try:
                pictures_content = self.driver.find_element_by_css_selector('div.image-container')
                picture_children = pictures_content.find_elements_by_css_selector("*")
                strain_picture_url = picture_children[1].get_attribute("srcset").split(",")[0]
            except:
                print("couldn't get image", strain_name)
            try:
                strain_name = content.find_elements_by_tag_name('h1')[0].text#
            except:
                print("coulnd't find strain name", strain_name)
            
            try:
                #parse secondary name
                strain_secondary_name = content.find_elements_by_tag_name('h2')[0].text#
                if(len(strain_secondary_name)>1):
                    strain_secondary_name = strain_secondary_name[4:].split(",")
                else:
                    arr = []
                    arr.append(strain_secondary_name)
                    strain_secondary_name = arr
                    
            except:
                print("couldn't find strain secondary name", strain_name)

            try:
                review_content = content.find_element_by_class_name('pb-sm')
                review_content = review_content.find_elements_by_tag_name("span")
                rating = review_content[0].text
                num_of_ratings = review_content[2].text
                num_of_ratings = num_of_ratings[1:len(num_of_ratings)-1]
            except:
                print("couldn't find rating or number of ratings", strain_name)
            
            try:
                calm_enrgy_content = content.find_element_by_class_name("calm-energize__mark")
                calm_enrgy = calm_enrgy_content.get_attribute("style")
                #percentage
                calm_enrgy = calm_enrgy[11:len(calm_enrgy)-2]
            except:
                print("couldn't get calm_enrgy for strain name: ",strain_name)

            try:
                #description
                description = content.find_element_by_class_name('strain__description').find_element_by_tag_name('p').text
            except:
                print("couldn't get description", strain_name)
            
            try:
                #effect section################
                effect_section = self.driver.find_element_by_id('strain-effects-section')
                reported_effects = effect_section.find_elements_by_tag_name('div')[2].text
                reported_effects_arr = [int(s) for s in reported_effects.split() if s.isdigit()]
                people_reporting_effects = reported_effects_arr[0]
                num_of_effect_reports = reported_effects_arr[1]
                pos_neg_feelings_dict = self.get_feelings('people report feeling',effect_section)
                helps_with_dict = self.get_feelings('people say it helps with', effect_section)
                feelings_dict = {**pos_neg_feelings_dict, **helps_with_dict}
            except:
                print("coudln't get reported effects", strain_name)
            #Review content
            try:
                try:
                    read_all_reviews_element_href = self.driver.find_element(By.XPATH, '//a[text()="Read all reviews"]').get_attribute("href")
                    self.driver.get(read_all_reviews_element_href)
                    time.sleep(2)
                except:
                    print("reviews don't exist for this strain: ", strain_name)
                get_next_review_page = 1
                test = 0
                while(get_next_review_page and test < 1):
                    read_all_reviews_element_href = None
                    try:
                        review_contents = self.driver.find_elements_by_css_selector("article.review-card")
                        for review in review_contents:
                            review_object = {"stars": "", "date": "", "feelings":[], "review_body": ""}
                            stars = ""
                            date = ""
                            feelings = []
                            review_body = ""
                            try:
                                stars_content = review.find_element_by_css_selector("span.star-rating").get_attribute("style")
                                stars = re.findall('\d*%', stars_content)[0]
                                stars = stars[0:len(stars)-1]
                                review_object["stars"] = stars
                            except:
                                print("couldn't get star content from review", strain_name)
                            try:
                                header_content = review.find_element_by_css_selector("header.border-b")
                                date = header_content.find_element_by_css_selector("div.text-default").text
                                review_object["date"] = date
                            except:
                                print("couldn't get header content from review", strain_name)
                            try:
                                feelings_content = review.find_elements_by_css_selector("div.jsx-1641593479")
                                for feeling_content in feelings_content:
                                    if(feeling_content.text):
                                        feelings.append(feeling_content.text)
                                review_object["feelings"] = feelings
                            except:
                                print("couldn't get feelings content from review", strain_name)
                            try:
                                review_body = review.find_element_by_xpath("//div[@itemprop='reviewBody']").text
                                review_object["review_body"] = review_body
                            except:
                                print("couldn't get review body from review", strain_name)
                            try:
                                if(review_object["stars"]!= "" or review_object["date"] != "" or review_object["feelings"].length != 0 or review_object["review_body"] != ""):
                                    review_data.append(review_object)
                            except:
                                print("couldn't append review object to review data array ", strain_name)
                    except:
                        print("couldn't find review_contents", strain_name)
                    try:
                        test += 1
                        get_next_review_page = self.driver.find_element(By.XPATH, '//a[text()="Next"]').get_attribute("href")
                        self.driver.get(get_next_review_page)
                        time.sleep(2)
                    except:
                        get_next_review_page = 0
                        print("no next review page for strain: ", strain_name)
                        
            except:
                print("couldn't get reviews")

        bud_data["name"] = strain_name
        bud_data["secondary_name"] = strain_secondary_name
        bud_data["image"] = strain_picture_url
        bud_data["strain_type"] = strain_type
        bud_data["potency"] = strain_potency
        bud_data["calm_enrgy"] = calm_enrgy
        bud_data["stars"] = rating
        bud_data["reviews_count"] = num_of_ratings
        bud_data["description"] = description
        bud_data["people_reporting_effects"] = people_reporting_effects
        bud_data["reported_effects_count"] = num_of_effect_reports
        bud_data["effects"] = feelings_dict
        bud_data["review_data"] = review_data
        bud_data["written_reviews_count"] = len(bud_data["review_data"])
        return bud_data
        

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
    def waitForPageLoad(self):
        try:
            myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, '__next')))
            print ("Page is ready!")
        except TimeoutException:
            print ("Loading took too much time!")

    def getAllHyperlinks(self):
        hyperlinks = []
        #seems to error out when no element is found
        try:
            self.waitForPageLoad()
            cards = self.driver.find_elements(By.XPATH, '//a[contains(@href,"/strains/")]')
            for card in cards: 
                href = card.get_attribute("href")
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

