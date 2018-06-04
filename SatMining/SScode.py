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

class AuthorStruct(object):
    fname = "NULL"
    mname = "NULL"
    lname = "NULL"
    suffix = "NULL"
    email = "NULL"
    aff = "NULL"
    corporate = "FALSE"

class ExcelEntry(object):
    complete_Entry =[]
    totalAuthorMeta = []
    authorCounter = 0
    excelRowCount = 1
    title = "NULL"
    fulltext = "NULL"
    keywords = "NULL"
    abstract = "NULL"
    disciplines = "NULL"
    comments = "NULL"
    dcmi = "NULL"
    embargo = "NULL"
    endDate = "NULL"
    funder = "NULL"
    grant = "NULL"
    hosted = "NULL"
    location = "NULL"
    multimediaURL = "NULL"
    multimedia = "youtube"
    previousVersions = "NULL"
    researchArea = "NULL" # needs to be grabbed per session for a from a list of keyed terms
    session = "NULL" # can be copied from title split
    startDate = "NULL" # needs to be in a very specific format, if python can't date-format it OpenRefine will
    updateReason = "NULL"
    url = "NULL"

def CreateDate(rawTime):
    year = "2018"
    month = "08"
    day = "01" # going to need some logic to determine the day here
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
    print correctFormat
    return correctFormat

def checkItem(item2Add):
    if item2Add == "NULL":
        return ""
    else:
        return item2Add

def generateRowEntry(Entry_Data):
    organizedRow = []
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.title))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.fulltext))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.keywords))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.abstract))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.disciplines))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.comments))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.dcmi))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.embargo))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.endDate))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.funder))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.grant))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.hosted))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.location))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.multimediaURL))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.multimedia))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.previousVersions))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.researchArea))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.session))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.startDate))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.updateReason))
    Entry_Data.complete_Entry.append(checkItem(Entry_Data.url))
    Entry_Data.complete_Entry = Entry_Data.complete_Entry + Entry_Data.totalAuthorMeta
    if Entry_Data.authorCounter < (len(Entry_Data.totalAuthorMeta)/ 7):
        Entry_Data.authorCounter = (len(Entry_Data.totalAuthorMeta)/ 7)
    return

def convertToRomanNum(sessionData, Entry_Data, sessionTitleText, driver):
    if sessionData[0] == "Session":  # roman numeral conversion
        romanNum = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII']
        convertNum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        for numCheck in xrange(12):
            if sessionData[1][:-1] == romanNum[numCheck]:               # check individual words for Roman Numeral
                sessionData[1] = str(convertNum[numCheck]) + ":"        # Replace Roman Numeral with number
                twoDigit = ""
                if numCheck + 1 < 10: twoDigit = "0" + str(numCheck + 1)
                else: twoDigit = str(numCheck + 1)
                pageTitle = driver.find_element_by_css_selector("div[id^='page-title']")
                if str(pageTitle.text) == "TECHNICAL SESSIONS":
                    print "TPS" + twoDigit + "-2018"
                    Entry_Data.researchArea = "TPS" + twoDigit + "-2018"
                else: # pageTitle == "Pre-Conference"
                    print "PWS" + twoDigit + "-2018"
                    Entry_Data.researchArea = "PWS" + twoDigit + "-2018"

        dataString = ""
        for addData in xrange(sessionData.__len__()):
            dataString += sessionData[addData] + " "
        Entry_Data.session = dataString
    else:
        Entry_Data.session = sessionTitleText  # poster and swifty names caught here
        areaSplit = sessionTitleText.split()
        if areaSplit[0] == "Poster":
            Entry_Data.researchArea = "Poster" + areaSplit[2] + "-2018"
        else: # areaSplit[0] == "Swifty"
            Entry_Data.researchArea = "Swifty" + areaSplit[2] + "-2018"
    return

def addToTotalAuthorMeta(eachAuthorData, Entry_Data):
    for g in xrange(len(eachAuthorData)):
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].fname))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].mname))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].lname))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].suffix))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].email))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].aff))
        Entry_Data.totalAuthorMeta.append(checkItem(eachAuthorData[g].corporate))

def splitAuthorName (authorSingle, authorGroup, Entry_Data): # splits author's name into first and last

    eachAuthorData = []

    for m in xrange(len(authorSingle)):                       # cycle through each author

        splitName = authorSingle[m].split()                   # splits authors name apart

        authorMeta = AuthorStruct()                           # needs to be regenerated each time
        authorMeta.aff = authorGroup[1]                       # grab affiliation
        if len(splitName) == 0:
            print "ERROR - No ENTRY"
        elif len(splitName) == 2:
            authorMeta.fname = splitName[0]
            authorMeta.lname = splitName[1]
        elif len(splitName) == 3:
            authorMeta.fname = splitName[0]
            authorMeta.mname = splitName[1]
            authorMeta.lname = splitName[2]
        else:  # len(splitName) == 4:
            authorMeta.fname = splitName[0]
            authorMeta.mname = splitName[1]
            authorMeta.lname = splitName[2] + splitName[3]
        eachAuthorData.append(authorMeta) # logs author objects for processing
    addToTotalAuthorMeta(eachAuthorData, Entry_Data)


    return

def write_to_File(sheet, Entry_Data):
    for x in xrange(len(Entry_Data.complete_Entry)):
        sheet.write(Entry_Data.excelRowCount, x, Entry_Data.complete_Entry[x])
    Entry_Data.excelRowCount += 1
    return

def separateAuthors (authorsAff, Entry_Data):                               # separates authors from affiliations and divides into
                                                                # individual authors
    for k in xrange(len(authorsAff)):                           # cycle through each affiliated group
        print "# of Aff: " + str(len(authorsAff))
        print authorsAff[k]

        authorGroup = re.split(u'- |- |– ', authorsAff[k])
        print authorGroup[0]
        print authorGroup[1]

        authorSingle = authorGroup[0].split(", ")               # divides authors up

        splitAuthorName(authorSingle, authorGroup, Entry_Data)

    return

def createInitialHeaders(sheet):
    sheet.write(0, 0, "title")
    sheet.write(0, 1, "fulltext_url")
    sheet.write(0, 2, "keywords")
    sheet.write(0, 3, "abstract")
    sheet.write(0, 4, "disciplines")
    sheet.write(0, 5, "comments")
    sheet.write(0, 6, "dcmi_type")
    sheet.write(0, 7, "embargo_date")
    sheet.write(0, 8, "end_date")
    sheet.write(0, 9, "funder")
    sheet.write(0, 10, "grant")
    sheet.write(0, 11, "hosted")
    sheet.write(0, 12, "location")
    sheet.write(0, 13, "multimedia_url")
    sheet.write(0, 14, "multimedia_format")
    sheet.write(0, 15, "previous_versions")
    sheet.write(0, 16, "research_area")
    sheet.write(0, 17, "session")
    sheet.write(0, 18, "start_date")
    sheet.write(0, 19, "update_reason")
    sheet.write(0, 20, "url")
    return

def createAuthorHeaders(sheet, authorMaxCount):
    o = 21
    for m in xrange(authorMaxCount):
        sheet.write(0, o, "author" + str(m + 1) + "_fname")
        sheet.write(0, o + 1, "author" + str(m + 1) + "_mname")
        sheet.write(0, o + 2, "author" + str(m + 1) + "_lname")
        sheet.write(0, o + 3, "author" + str(m + 1) + "_suffix")
        sheet.write(0, o + 4, "author" + str(m + 1) + "_email")
        sheet.write(0, o + 5, "author" + str(m + 1) + "_institution")
        sheet.write(0, o + 6, "author" + str(m + 1) + "_is_corporate")

        o += 7
    return


def main():
    book = xlwt.Workbook()
    sheet = book.add_sheet('Sheet 1')

    # ---- Add function for initial sheet setup
    createInitialHeaders(sheet)

    driver = webdriver.Chrome("chromedriver.exe")
    Entry_Data = ExcelEntry()
    driver.get("https://smallsat.org")
    linksArray = ["https://www.smallsat.org/technical-program/tech-sessions", "https://www.smallsat.org/technical-program/workshop", "https://www.smallsat.org/technical-program/keynote"]
    driver.get(linksArray[0]) # Got to Technical Sessions (After one link works this will need to loop for the others)
    sessionsList = driver.find_elements_by_css_selector("div[class^='demo']")
    print "# of Sessions: " + str(sessionsList.__len__())

    i = 0

    # while i < len(sessionsList): # cycle through sessions
    while i < 1:          # single test
        alternateKey = 0                                        # reset each session
        sessionTitleText = sessionsList[i].text
        sessionData = sessionTitleText.split()                  # break up session title
        # TODO---- Logic of determining "day" here *I'm working on it

        convertToRomanNum(sessionData, Entry_Data, sessionTitleText, driver)
        print Entry_Data.session
        sessionsList[i].click()                                 # opens drop down list per session

        time.sleep(5)

        eventsList = sessionsList[i].find_elements_by_css_selector("p")
        print "# of Events: " + str(eventsList.__len__())

        j = 2                                                   # ignore first two elements, should be 2
        while j in xrange(len(eventsList) - 1):                 # cycle through events
            del Entry_Data.complete_Entry[:]
            del Entry_Data.totalAuthorMeta[:]
            eventData = eventsList[j].text                      # data on separate lines
            splitData = eventData.splitlines()                  # lines divided into list elements

            if splitData[0] == "Alternates:":
                alternateKey = 1

            if alternateKey == 0:                               # not an alternate/has time stamp
                print splitData[0]                              # Time
                # TODO--- Time needs to be formatted properly!!! ---
                formattedDate = CreateDate(splitData[0])
                Entry_Data.startDate = formattedDate
                print splitData[1]                              # Event Title
                Entry_Data.title = splitData[1]

                authorsAff = splitData[2].split("; ")           # puts authors with their affiliation
                separateAuthors(authorsAff, Entry_Data)
                print "Execl entry: " + str(Entry_Data.excelRowCount)
                generateRowEntry(Entry_Data)
                write_to_File(sheet, Entry_Data)

                        # TODO---- Entry should be written out to spreadsheet --- #

            else: # alternateKey = 1
                # i must be referenced as i + 1, "Alternates:" is considered an element and should not be processed
                if splitData[0] == "Alternates:":
                    print "---Alternates Here---"
                else: # do the stuff
                    print splitData[0]                          # Event Title
                    Entry_Data.title = splitData[0]
                    print splitData[1]           # Authors/Presenters
                    Entry_Data.startDate = "2018-08-00T12:00:00Z"

                    authorsAff = splitData[1].split("; ")       # puts authors with their affiliation

                    separateAuthors(authorsAff, Entry_Data)
                    print "Execl entry: " + str(Entry_Data.excelRowCount)
                    generateRowEntry(Entry_Data)
                    write_to_File(sheet, Entry_Data)
                    # TODO---- Entry should be written out to spreadsheet --- #

            j += 1
        i += 1
        alternateKey = 0

    createAuthorHeaders(sheet, Entry_Data.authorCounter)
    book.save("SS2018-Metadata.xls")
    # testbook = xlrd.open_workbook("SS2018-Metadata.xls")
    # testsheet = testbook.sheet_by_index(0)
    # print testsheet.cell(0, 20).value
    # print testsheet.cell(0, 21).value

    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    main()