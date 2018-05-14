from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import xlrd # read
import xlwt # write
import string
import re


class AuthorStruct():
    def __init__(self):
        self.fname = ""
        self.mname = ""
        self.lname = ""
        self.aff = ""
        self.corporate = "FALSE"

class ExcelEntry():
    def __int__(self):
        self.title = ""
        self.multimedia = "youtube"
        self.researchArea = "" # needs to be grabbed per session for a from a list of keyed terms
        self.session = "" # can be copied from title split
        self.startDate = "" # needs to be in a very specific format, if python can't date format it OpenRefine will



def main():
    # book = xlwt.Workbook()
    # sheet = book.add_sheet('Sheet 1')
    # book.save("Sample.xls")

    # driver = webdriver.Chrome("C:\\Users\\Casey\\Downloads\\chromedriver_win32\\chromedriver.exe") # works on Casey's Laptop (0riginal)
    driver = webdriver.Chrome("chromedriver.exe") # File path for Casey
    # driver = webdriver.Chrome() # File path for Jesse

    driver.get("https://smallsat.org")
    linksArray = ["https://www.smallsat.org/technical-program/tech-sessions", "https://www.smallsat.org/technical-program/workshop", "https://www.smallsat.org/technical-program/keynote"]
    driver.get(linksArray[0]) # Got to Technical Sessions (After one link works this will need to loop for the others)
    sessionsList = driver.find_elements_by_css_selector("div[class^='demo']")
    print "# of Sessions: " + str(sessionsList.__len__())

    i = 0
    alternateKey = 0
    # while i < len(sessionsList): # cycle through sessions
    while i < 1:  # single test
        print sessionsList[i].text
        sessionsList[i].click() # opens drop down list per session
        # ---- We will need to use session text to code each entry for DC ----
        time.sleep(5)

        eventsList = sessionsList[i].find_elements_by_css_selector("p")
        print "# of Events: " + str(eventsList.__len__())

        j = 4 # ignore first two elements, should be 2
        while j in xrange(len(eventsList) + 2): # cycle through events
        # while j < 3:  # single test

            # print eventsList[j].text
            eventData = eventsList[j].text # data on separate lines
            splitData = eventData.splitlines() # lines divided into list elements
            # time.sleep(10)

            if splitData[0] == "Alternates:":
                alternateKey = 1

            if alternateKey == 0: # not an alternate/has time stamp
                print splitData[0]  # Time
                # --- Time needs to be formatted properly!!! ---
                print splitData[1]  # Event Title

                # print splitData[2]  # Authors/Presenters

                authorsAff = splitData[2].split("; ") # puts authors with their affiliation

                for k in xrange(len(authorsAff)): # cycle through each affiliated group
                    print "# of Aff: " + str(len(authorsAff))
                    print authorsAff[k]
                    # authorGroup = authorsAff[k].split("- ") # puts authors by themselves
                    uniConvert = u''.join(authorsAff[k]).encode('utf-8')
                    authorGroup = re.split('- |,– |', authorsAff[k])

                    print authorGroup[0]
                    print authorGroup[1]

                    authorSingle = authorGroup[0].split(", ") # divides authors up
                    # print authorSingle[0]
                    for m in xrange(len(authorSingle)): # cycle through each author

                        splitName = authorSingle[m].split() # splits authors name apart

                        authorMeta = AuthorStruct() # needs to be regenerated each time
                        authorMeta.aff = authorGroup[1]  # grab affiliation
                        if len(splitName) == 0:
                            print "ERROR - No ENTRY"
                        elif len(splitName) == 2:
                            authorMeta.fname = splitName[0]
                            authorMeta.lname = splitName[1]
                            print splitName[0]
                            print splitName[1]
                        elif len(splitName) == 3:
                            authorMeta.fname = splitName[0]
                            authorMeta.mname = splitName[1]
                            authorMeta.lname = splitName[2]
                            print splitName[0]
                            print splitName[1]
                            print splitName[2]
                        else: # len(splitName) == 4:
                            authorMeta.fname = splitName[0]
                            authorMeta.mname = splitName[1]
                            authorMeta.lname = splitName[2] + splitName[3]
                            print splitName[0]
                            print splitName[1]
                            print splitName[2]
                        # ---- Entry should be written out to spreadsheet --- #


            else: # alternateKey = 1
                # i must be referenced as i + 1, "Alternates:" is considered an element and should not be processed
                print splitData[0]  # Event Title
                print splitData[1]  # Authors/Presenters

            j += 1
        i += 1
        alternateKey = 0


    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    main()