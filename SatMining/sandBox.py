from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlrd # read
import xlwt # write

import string

class car():
    num = 2

def testIt(car):
    car.num = 5
    return

def main():
    truck = car()
    print truck.num
    testIt(truck)
    print truck.num
    return

if __name__ == '__main__':
    main()

#
# uniText = u''.join(testing).encode('utf-8')
# testing2 = testing.decode('ascii', 'replace').replace(u'\ufffd', 'Yes')
# print testing2
test = [11, 12, 13]
test2 = [1, 2, 3]
test = test + test2
print test

# test = multiRow.splitlines()
# print test[0]
#
# path = "C:\\Users\\Casey\\PycharmProjects" + "\\" + "browserTest\\TestingGround\\Pulitzers Sheet.xlsx"
# print path
# bookOpen = xlrd.open_workbook(path)
# firstSheet = bookOpen.sheet_by_index(0)
#
# bookWrite = xlwt.Workbook()
# writeSheet = bookWrite.add_sheet('Sheet 1')
#
# i = 0
# while i != len(firstSheet.col_values(0)):
#     cell = firstSheet.cell(i, 0).value
#     splitter = cell.split('by')
#     # print splitter
#     # splitSplitter = splitter[0].split()
#     # splitSplitter.pop(0)
#     # j = 0
#     # while j < splitter[0].__len__():
#     #     splitter[j] = splitter[j] + " "
#     #     j += 1
#     if splitter.__len__() > 1:
#         writeSheet.write(i, 0, splitter[0])
#         writeSheet.write(i, 1, splitter[1])
#     else:
#         writeSheet.write(i, 0, splitter[0])
#     # print splitter[0] + splitter[1]
#     i += 1
#
# bookWrite.save("Pulitzers Sheet 2.xls")
# testArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# evensList = []
# print testArray[0]
# i = 0
# for i in range(testArray.__len__()):
#     if testArray[i] % 2 == 0:
#         evensList.append(testArray[i])
#     i += 1
# print testArray
# print evensList

# class AuthorStruct(object):
#     fname = "NULL"
#     mname = "NULL"
#     lname = "NULL"
#     aff = "NULL"
#     corporate = "FALSE"
# testing = AuthorStruct()
# testing.corporate = "try this"
# print testing.corporate
# getHeaders = xlrd.open_workbook("SmallSat_2017_Metadata.xls")
# pullSheet = getHeaders.sheet_by_index(0)
# testhead = pullSheet.row(0)
# print testhead[0].value
# book = xlwt.Workbook()
# sheet = book.add_sheet('Sheet 1')
# row = sheet.row(0)
# row.write(0, tuple["a", "b"])
# book.save("Sample.xls")
#
#
# driver = webdriver.Chrome("chromedriver.exe")
# # # #driver = webdriver.Firefox("")
# # # #driver = webdriver.Opera("")
# # #
# driver.get("http://smallsat.org/")
# linksArray = ["https://www.smallsat.org/technical-program/tech-sessions",
#               "https://www.smallsat.org/technical-program/workshop",
#               "https://www.smallsat.org/technical-program/keynote"]
# driver.get(linksArray[0])  # Got to Technical Sessions (After one link works this will need to loop for the others)
# time.sleep(5)
# sessionsList = driver.find_elements_by_css_selector("div[class^='demo']")
# sessionsList[0].click()  # opens drop down list per session
# time.sleep(5)
# # css = By.CSS_SELECTOR("#main-info div.main-info>h1")
# # element = driver.find_element(By.CSS_SELECTOR, "#main-info")
# # element2 = element.find_element(By.PARTIAL_LINK_TEXT, "August")
# # element2 = element.find_element_by_partial_link_text("h2['Monday']")
# element2 = driver.find_elements_by_css_selector("#main-info h2")
# print len(element2)
# correctElements = []
# for i in xrange(len(element2)):
#     print element2[i].text
#
# for i in xrange(len(element2)):
#     splitter = element2[i].text.split()
#     if splitter[0] == "Session" or splitter[0] == "Poster" or splitter[0] == "Swifty" or splitter[0] == "Posters":
#         print splitter[0]
#     else:
#         correctElements.append(element2[i])
# print len(correctElements)
# print correctElements[0].text
# print correctElements[1].text
# # if driver.find_elements_by_name("btnk").__len__() != 0: # .isEmpty() or .size() != 0
# #     print "Element found!"
# # else:
# #     print "Element does not exist!"
# # testing = "Hi! Hello it worked! "
# # testing = testing[:-4]
# #
# # search = driver.find_element_by_name("q")
# # search.send_keys("Utah")
# # search.send_keys(Keys.ENTER)
# # time.sleep(5)
# # nextPage = driver.find_elements_by_css_selector("a[class^='pn']")
# # print nextPage.__len__()
# # if nextPage.__len__() != 0:
# #     print "Page Completed"
# #     nextPage[0].click()
# # else:
# #     print "Last Page"
# #
# # f = open("testingCreate.txt", "w") # test "w+" - may be append on the the end, otherwise use "a" or "a+"
# # f.write(testing + "\n")
# # f.write("Hello here")
# # # f.write("") # Erases data in file when "w" is enabled
# # f.close()
#
#
# # driver.get("https://www.goodreads.com")
# # driver.find_element_by_name("user[email]").send_keys("digistudent1@gmail.com")
# # driver.find_element_by_name("user[password]").send_keys("*Bigblue17")
# # driver.find_element_by_id("remember_me").click()
# #
# # driver.find_element_by_name("user[password]").send_keys(Keys.ENTER)
# #
# # # driver.implicitly_wait(10)
# # driver.get("https://www.goodreads.com/book/show/4671.The_Great_Gatsby?from_search=true")
# # time.sleep(10)
# # driver.close()
# #
# time.sleep(5)
# driver.quit()