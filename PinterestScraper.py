# Cullen, Riley 
# PinterestScraper.py
# Created on 4/18/2020

# Revision History:
#   April 18, 2020:
#       1). __init__(self, str, str) defined and implemented to support the login
#           to pinterest
#       2). __Login(self, str, str) defined and implemented to log in
#       3). __del__(self) defined and implemented to quit browser
#       4). GetLinkSet() defined and implemented to get links
#   April 19, 2020
#       1). __CleanInitialSet() defined and implemented
#   April 21, 2020
#       2). __CleanInitialSet() --> __CleanLinkSet()

# To fix:
#   1. scraper sometimes grabs wrong elements
#   2. figure out scroll method

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from collections import deque

class PinterestScraper:
    # desc: initializes webdriver object and logs into pinterest
    # pre:  email, password must be valid
    # post: _browser object initialized
    def __init__(self, email, password):
        options = Options()
        options.headless = True
        self._browser = webdriver.Chrome('/Users/rileycullen/chromedriver', options=options)
        self._wait = WebDriverWait(self._browser, 20)
        self.__Login(email, password)

    # desc: Logs into pinterest account with parameterized email/password
    # pre:  email, password must be valid
    def __Login(self, email, password):
        loginURL = 'https://www.pinterest.com/login/'
        self._browser.get(loginURL)

        emailInput = self._browser.find_element_by_id("email")
        passwordInput = self._browser.find_element_by_id("password")

        emailInput.send_keys(email)
        passwordInput.send_keys(password)
        passwordInput.send_keys(Keys.RETURN)

    # desc: Goes to linkSetURL and gets the set of links we will parse
    # pre:  linkSetURL must be a valid URL to a pinterest pin page
    def GetLinkSet(self, linkSetURL):
        linkQueue = deque()
        self._browser.get(linkSetURL)

        linkSet = self._wait.until(EC.presence_of_all_elements_located(
					(By.CSS_SELECTOR, "a[href*='/pin/'] img")))
        linkQueue = self.__CleanLinkSet(linkSet)

        for i in range(len(linkQueue)):
            print(linkQueue[i])

    # desc: Removes non-infographic images
    def __CleanLinkSet(self, linkSet):
        newLinkSet = []
        for i in range(len(linkSet)):
            imgSrc = linkSet[i].get_attribute('src')
            if imgSrc.find('/236x/') != -1:
                imgSrc = imgSrc.replace('/236x/','/736x/')
                newLinkSet.append(imgSrc)
        # changeg
        return newLinkSet

    def __del__(self):
        if self._browser:
            self._browser.quit()
