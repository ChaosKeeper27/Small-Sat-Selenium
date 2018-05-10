from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl
import xlrd # read
import xlwt # write
import string

class AuthorStruct():
    def __init__(self):
        self.fname = ""
        self.mname = ""
        self.lname = ""
        self.aff = ""

def main():
    # book = xlwt.Workbook()
    # sheet = book.add_sheet('Sheet 1')
    # book.save("Sample.xls")

    driver = webdriver.Chrome("C:\\Users\\Casey\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver.get("https://smallsat.org")
    linksArray = ["https://www.smallsat.org/technical-program/tech-sessions", "https://www.smallsat.org/technical-program/workshop", "https://www.smallsat.org/technical-program/keynote"]
    driver.get(linksArray[0])
    sessionsList = driver.find_elements_by_css_selector("div[class^='demo']")
    print "# of Sessions: " + str(sessionsList.__len__())

    i = 0
    while i < len(sessionsList):
        print sessionsList[0].text
        sessionsList[0].click()
        time.sleep(5)
        eventsList = sessionsList[0].find_elements_by_css_selector("p")
        print "# of Events: " + str(eventsList.__len__())
        print eventsList[3].text
        eventData = eventsList[3].text
        splitData = eventData.splitlines()
        print splitData[0] # Time
        print '----'
        print splitData[1] # Event Title
        print '----'
        print splitData[2] # Authors/Presenters
        authorsAff = splitData[2].split(";")
        print authorsAff[0] # authors with affiliation
        authorGroup = authorsAff[0].split("-")
        print authorGroup[0] # only authors
        authorSingle = authorGroup[0].split(",")
        print authorSingle[0] # only one author
        splitName = authorSingle[0].split()
        print splitName[0] # first name of one author
        authorMeta = AuthorStruct()
        authorMeta.fname = splitName[0]
        print authorMeta.fname
        i += 1
    # partsList = eventsList[1].find_elements_by_css_selector("strong")
    # print "# of Parts: " + str(partsList.__len__())
    # print partsList[0].text
    # authors = eventsList[1].find_elements_by_css_selector("br")
    # print authors[0].text

    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    main()