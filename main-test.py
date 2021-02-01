from selenium import webdriver
from module.utils import check_response
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import asyncio


def main():
    ## when using mac
    durl ="./chromedriver"
    driver = webdriver.Chrome(durl)

    wait = WebDriverWait(driver, 10)
    url = "https://www.synology.com/zh-tw/support/nas_selector"

    if not check_response(url):
        print("URL not found or Error")
    else:
        driver.get(url)

    selection = {
        "user_type_business": {
            "app_fileserver":[],
            "app_databackup":[],
            "app_iscsi":[],
            "app_collatboration":[], 
            "app_mailserver":[],
            "app_vmm":[],

        },
        "user_type_home": {
            "app_fileserver":["how_many_people_checkbox_people_less","how_many_people_checkbox_people_medium","how_many_people_checkbox_people_large"],
            "app_databackup":["how_many_people_checkbox_people_less","how_many_people_checkbox_people_medium","how_many_people_checkbox_people_large"],
            "app_multimedia":["need_image_recognition_checkbox_no_image_reco","need_image_recognition_checkbox_yes_image_reco"],
            "app_productivity":["how_many_people_checkbox_people_large","how_many_people_checkbox_people_medium","how_many_people_checkbox_people_less"],
            "app_vmm":["","how_many_virtual_machines_for_home_checkbox_vmm_medium"],
        },
    }
    # collect options
    driver.find_element(By.XPATH, "//label[@for='user_type_business']").click()

    business = driver.find_elements_by_xpath(
        "//label[starts-with(@for,'app_')]")
    for i in business:
        selection['user_type_business'][i.get_attribute('for')] = dict()

    driver.find_element_by_css_selector("input#user_type_home").click()
    home = driver.find_elements_by_xpath("//label[starts-with(@for,'app_')]")

    # driver.find_element(By.XPATH, "//input[@id='app_fileserver']").click()
    for i in home:
        selection['user_type_home'][i.get_attribute('for')] = dict()

    for idx, value in selection['user_type_home'].items():
        selection['user_type_home'][str(idx)] = []
        # print("idx: ",idx)
        driver.find_element(By.XPATH, "//input[@id="+"'"+str(idx)+"'"+"]").click()

        # Click "next" button
        element = driver.find_element_by_css_selector("button.margin_bottom30")
        driver.execute_script("arguments[0].click()", element)

        element2=driver.find_elements_by_class_name("nas_s_lab")
        for i in element2:
            print("for : ",i.get_attribute('for'))
            element_sub=driver.find_element_by_id(i.get_attribute('for'))
            print("name : ",element_sub.get_attribute("name"))
        ## collect all types of requirement
        # driver.find_elements_by_xpath("//label[starts-with(@for,'app_')]")
        # for sub_idx, sub_value in selection['user_type_home'][str(idx)].items():
        #     selection['user_type_home'][str(idx)].append(str(sub_idx))


        break

    time.sleep(3)
    driver.close()


if __name__ == "__main__":
    main()
