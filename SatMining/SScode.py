#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

#
# dayCounter = 0

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
        self.startDate = "" # needs to be in a very specific format, if python can't date-format it OpenRefine will

def CreateDate(rawTime, day_num):
    year = "2018"
    month = "08"
    day = day_num # going to need some logic to determine the day here
    hour = ""
    minutes = ""
    seconds = "00"
    timeData = rawTime.split()
    AMPM = timeData[1]
    timeBreakdown = timeData[0].split(":")
    minutes = timeBreakdown[1]
    if AMPM == "PM":
        hour = str(int(timeBreakdown[0]) + 12) # convert to military time
    else: # AM time
        if len(timeBreakdown[0] == 1):
            hour = "0" + timeBreakdown[0] # add 0 infront of single digits
        else:
            hour = timeBreakdown[0]
    correctFormat = year + "-" + month + "-" + day + "T" + hour + ":" + minutes + ":" + seconds + "Z"
    #print correctFormat
    return correctFormat


def convertToRomanNum(sessionData, Entry_Data, sessionTitleText):
    if sessionData[0] == "Session":  # roman numeral conversion
        romanNum = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII']
        convertNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        for numCheck in xrange(12):
            if sessionData[1][:-1] == romanNum[numCheck]:               #check individual words for Roman Numeral
                sessionData[1] = str(convertNum[numCheck]) + ":"        #Replace Roman Numeral with number
        dataString = ""
        for addData in xrange(sessionData.__len__()):
            dataString += sessionData[addData] + " "
        Entry_Data.session = dataString
    else:
        Entry_Data.session = sessionTitleText  # poster and swifty names caught here
    return

def splitAuthorName (authorSingle, authorGroup):              # splits author's name into first and last
    for m in xrange(len(authorSingle)):                       # cycle through each author

        splitName = authorSingle[m].split()                   # splits authors name apart

        authorMeta = AuthorStruct()                           # needs to be regenerated each time
        authorMeta.aff = authorGroup[1]                       # grab affiliation
        if len(splitName) == 0:
            print "ERROR - No ENTRY"
        elif len(splitName) == 2:
            authorMeta.fname = splitName[0]
            authorMeta.lname = splitName[1]
            #print splitName[0]
            #print splitName[1]
        elif len(splitName) == 3:
            authorMeta.fname = splitName[0]
            authorMeta.mname = splitName[1]
            authorMeta.lname = splitName[2]
            #print splitName[0]
            #print splitName[1]
            #print splitName[2]
        else:  # len(splitName) == 4:
            authorMeta.fname = splitName[0]
            authorMeta.mname = splitName[1]
            authorMeta.lname = splitName[2] + splitName[3]
            #print splitName[0]
            #print splitName[1]
            #print splitName[2]
    return

def separateAuthors (authorsAff):                               #separates authors from affiliations and divides into
                                                                #individual authors
    for k in xrange(len(authorsAff)):                           # cycle through each affiliated group
        print "# of Aff: " + str(len(authorsAff))
        print authorsAff[k]

        authorGroup = re.split(u'- |- |– ', authorsAff[k])

        print authorGroup[0]
        print authorGroup[1]

        authorSingle = authorGroup[0].split(", ")               # divides authors up

        splitAuthorName(authorSingle, authorGroup)
    return

def splitDays(element, day_dictionary):
    count = 0;
    for i in xrange(len(element)):
        splitter = element[i].text.split()
        if splitter[0] == u'Tuesday,':
            for x in range(0,i):
                day_dictionary[element[x].text] = "monday"
            count = i
        elif splitter[0] == u'Wednesday,':
            for x in range(count, i):
                day_dictionary[element[x].text] = "tuesday"
            count = i
        elif splitter[0] == u'Thursday,':
            for x in range(count, i):
                day_dictionary[element[x].text] = "wednesday"
            count = i
        elif splitter[0] == u'Posters':
            for x in range(count, i):
                day_dictionary[element[x].text] = "thursday"
            count = i
        elif splitter[0] == u'Swifty' and splitter[1] == u'Sessions':
            for x in range(count, i):
                day_dictionary[element[x].text] = "posters"
            count = i

            for x in range(count, len(element)):
                day_dictionary[element[x].text] = "swifty"
    return

def getDayNum(day):
    day_num = "00"
    if day == "monday":
        day_num = "06"
    elif day == "tuesday":
        day_num = "07"
    elif day == "wednesday":
        day_num = "08"
    elif day == "thursday":
        day_num = "09"
    elif day == "posters":
        day_num = "06"
    elif day == "swifty":
        day_num = "06"
    return day_num

def pullInfo(sessionsList, Entry_Data, day_dictionary):
    i = 1
    while i < 2:          # single test. Will be replace with for i in xrange(sessionsList):
        alternateKey = 0                                        # reset each session
        sessionTitleText = sessionsList[i].text
        sessionData = sessionTitleText.split()                  # break up session title

        dict_keys = day_dictionary.keys()
        day = day_dictionary[sessionTitleText]

        day_num = getDayNum(day)

        convertToRomanNum(sessionData, Entry_Data, sessionTitleText)
        #print Entry_Data.session
        sessionsList[i].click()                                 # opens drop down list per session

        time.sleep(5)

        eventsList = sessionsList[i].find_elements_by_css_selector("p")


        #print "# of Events: " + str(eventsList.__len__())

        j = 2                                                   # ignore first two elements, should be 2
        while j in xrange(len(eventsList) - 1):                 # cycle through events

            eventData = eventsList[j].text                      # data on separate lines
            splitData = eventData.splitlines()                  # lines divided into list elements

            if splitData[0] == "Alternates:":
                alternateKey = 1

            if alternateKey == 0:                                # not an alternate/has time stamp
                #print splitData[0]                              # Time
                # TODO--- Time needs to be formatted properly!!! ---
                formattedDate = CreateDate(splitData[0], day_num)
                Entry_Data.startDate = formattedDate
                #print splitData[1]                              # Event Title
                Entry_Data.title = splitData[1]

                authorsAff = splitData[2].split("; ")            # puts authors with their affiliation
                separateAuthors(authorsAff)

                        # TODO---- Entry should be written out to spreadsheet --- #

            else: # alternateKey = 1
                # i must be referenced as i + 1, "Alternates:" is considered an element and should not be processed
                if splitData[0] == "Alternates:":
                    print "---Alternates Here---"
                else: # do the stuff
                    #print splitData[0]                          # Event Title
                    Entry_Data.title = splitData[0]
                    #print splitData[1]                          # Authors/Presenters

                    authorsAff = splitData[1].split("; ")       # puts authors with their affiliation

                    separateAuthors(authorsAff)
                    # TODO---- Entry should be written out to spreadsheet --- #

            j += 1
        i += 1
        alternateKey = 0

def main():
    # book = xlwt.Workbook()
    # sheet = book.add_sheet('Sheet 1')
    # book.save("Sample.xls")

    driver = webdriver.Chrome("chromedriver.exe")
    Entry_Data = ExcelEntry()

    driver.get("https://smallsat.org")
    linksArray = ["https://www.smallsat.org/technical-program/tech-sessions", "https://www.smallsat.org/technical-program/workshop", "https://www.smallsat.org/technical-program/keynote"]
    driver.get(linksArray[0]) # Got to Technical Sessions (After one link works this will need to loop for the others)
    allSessions = driver.find_elements_by_css_selector("div[class^='demo']")

    element = driver.find_elements_by_css_selector("#main-info h2")

    day_dictionary = {}

    splitDays(element, day_dictionary)

    pullInfo(allSessions, Entry_Data, day_dictionary)

    #print "# of Sessions: " + str(sessionsList.__len__())



    # while i < len(sessionsList): # cycle through sessions



    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    main()