﻿import sys
import os
import selenium
import pyautogui
import options
from selenium import webdriver
from options import Options,attrs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import re

path_root = "https://shopee.vn"
list_link = []
file_name_collected_link = "collected_link.txt"
# link da collect data 
collected_link = []

class ShoopeCr:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(executable_path = "./chromedriver.exe",options = options)
        self.driver.maximize_window()

    def scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while (True) :
            self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height :
                break
            else :
                last_height = new_height      
        time.sleep(3)


    def request_html(self,url):
        self.driver.get(url)
        self.driver.set_page_load_timeout(100)
        self.scroll()

    def get_products_from_catagory(self,url_catagory):
        self.request_html(url_catagory)
        link_products = []
        aTag = self.driver.find_elements_by_class_name("shopee-search-item-result__items")[0].find_elements_by_tag_name("a")
        print(len(aTag))
        for a in aTag:
            link_products.append(a.get_attribute("href"))
        return link_products


    def get_comments(self,url_product):
        self.request_html(url_product)
        self.driver.implicitly_wait(10)
        time.sleep(2)
        total_comments = 0
        if self.driver.find_elements_by_class_name("_1_WXLA") != []:
            comments = []
            if self.driver.find_elements_by_class_name("_3Oj5_n") != []:
                if len(self.driver.find_elements_by_class_name("_3Oj5_n")) == 2:
                    total_comments = int(self.driver.find_elements_by_class_name("_3Oj5_n")[1].text)
                if total_comments != 0 :
                    self.driver.find_elements_by_class_name("_1_WXLA")[1].click()
                else :
                    return 1
            else :
                return 1
            if self.driver.find_elements_by_class_name("product-rating-overview__filter--with-comment") != []:
                BL = self.driver.find_elements_by_class_name("product-rating-overview__filter--with-comment")[0].text
            else :
                return 1
            numOfBL = int(re.findall('\d+',BL)[0])
            print(numOfBL)
            if numOfBL != 0:
                time.sleep(2)
                count_comments = 0
                while True:
                    self.driver.implicitly_wait(7)
                    comments_tag = self.driver.find_elements_by_class_name("shopee-product-rating__content")
                    for x in comments_tag :
                        if x.text != "":
                            comments.append(x.text)
                        count_comments += 1
                        if count_comments == numOfBL:
                                break
                    if count_comments == numOfBL:
                        break
                    if self.driver.find_elements_by_class_name("shopee-icon-button--right") != []:
                        self.driver.find_elements_by_class_name("shopee-icon-button--right")[0].click()
                    else :
                        break
                    time.sleep(2)
                print(comments)
                self.save_data("data.crash",comments)
            return 1

    def auto_get_comments(self,sub_catagory_link):
        link_products = self.get_products_from_catagory(sub_catagory_link)
        for link in link_products:
            if link != None and link not in collected_link:
                collected_link.append(link)
                self.get_comments(link)
                time.sleep(5)
    def wait_time(self,t):
        #self.driver.implicitly_wait(t)
        time.sleep(t)
        self.driver.close()


    def save_data(self,fileJS_name,data):
        with open(fileJS_name,"a",encoding = 'utf-8') as fw:
            for x in data :
                fw.write(b'"'.decode('utf-8') + x + b'",'.decode('utf-8') + "\n")
        fw.close()


    def get_link(self,page):
        self.request_html(page)
        try:
            time.sleep(2)
            home_catagory_list = self.driver.find_elements_by_class_name("home-category-list__category-grid")
            for tag in home_catagory_list:
                list_link.append(tag.get_attribute("href"))
            #print(list_link)
        except:
            print("An Error has been raised")


    def get_catagory_lists(self,url,list_SubCatagory):
        try:
            if url == None:
                print("Khong ton tai url ")
            else :
                self.request_html(url)
                self.driver.implicitly_wait(10)
                aTag_subCatagory = self.driver.find_elements_by_class_name("shopee-category-list__sub-category")
                time.sleep(3)
                for Tag in aTag_subCatagory :
                    list_SubCatagory.append(Tag.get_attribute('href'))
                time.sleep(3)
        except:
            print("An error has been raised")
            sys.exit()


    def close_driver(self):
        time.sleep(10)
        self.driver.quit()
#End Class Shopee

def read_file(fileJS_name):
    data = {}
    data_list = {}
    with open(fileJS_name,"r") as fr:
        data_list = json.load(fr)
    data = {"catagorys": data_list}
    return data

def save_link_collected(filename, ll):
    with open( filename, 'w') as fw:
        for x in ll:
            fw.writelines(x)
    fw.close()
def read_link_collected(filename):
    collected_link = []
    with open(filename,'r') as fr:
        collected_link = fr.readlines()
    fr.close()
    return collected_link
def main():
    collected_link = read_link_collected(file_name_collected_link)
    Shopee = ShoopeCr()
    data = {}
    data = read_file("list_sub_catagorys.json")
    list_catagorys = data['catagorys']
    for l in list_catagorys:
        if l == None :
            continue
        for ls in l :
            Shopee.auto_get_comments(ls)
            if collected_link != [] :
                save_link_collected(file_name_collected_link,collected_link)
    Shopee.close_driver()
if __name__ == "__main__":
    main()