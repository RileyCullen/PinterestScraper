# Cullen, Riley 
# PinterestScraper.py
# Created on 4/18/2020

# Sources
#   1. https://github.com/xjdeng/pinterest-image-scraper/blob/master/pinterest_scraper/scraper.py
#      DATE RETRIEVED: 4/25/20
#      ADAPTED:
#         a. GetLinkSet() adapts code from runme()


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
#   April 25, 2020
#       1). __RemoveDuplicates() defined and implemented
#       2). __CleanInitialSet() removed
#       3). GetLinkSet() updated to scraper entire page and remove duplicates
#   April 27, 2020
#       1). _links added to keep as an instance variable so the class can access 
#           the links scraped from <a>
#       2). ScrapeLinkSet defined and partially implemented (the image collection)
#       3). __GetHighResImage() defined and implemented

# To fix:
#   1. scraper sometimes grabs wrong elements
#   2. Add to results queue (remove duplicates too)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from collections import deque
import time

class PinterestScraper:
    # desc: initializes webdriver object and logs into pinterest
    # pre:  email, password must be valid
    # post: _browser object initialized
    def __init__(self, email, password):
        options = Options()
        options.headless = True
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self._browser = webdriver.Chrome('/Users/rileycullen/chromedriver', options=options)
        self._wait = WebDriverWait(self._browser, 20, ignored_exceptions=ignored_exceptions)
        self.__Login(email, password)
        self._links = set()

    # desc: Logs into pinterest account with parameterized email/password
    # pre:  email, password must be valid
    def __Login(self, email, password):
        loginURL = 'https://www.pinterest.com/login/'
        self._browser.get(loginURL)

        emailInput = self._browser.find_element_by_id("email")
        passwordInput = self._browser.find_element_by_id("password")

        emailInput.send_keys(email)
        passwordInput.send_keys(password)
        time.sleep(1)
        passwordInput.send_keys(Keys.RETURN)

    # desc: Goes to linkSetURL and gets the set of links we will parse
    # pre:  linkSetURL must be a valid URL to a pinterest pin page
    def GetLinkSet(self, linkSetURL):
        MAX_TRIES = 5
        tries = 0
        linkSet = []
        results = set()
        self._browser.get(linkSetURL)

        body = self._browser.find_element_by_tag_name("body")

        try:
            while tries < MAX_TRIES:
                print("tries: %d"%tries)
                try:
                    time.sleep(2)
                    previousSet = linkSet
                    linkSet = self._wait.until(EC.presence_of_all_elements_located(
					        (By.CSS_SELECTOR, "a[href*='/pin/']")))

                    results = self.__RemoveDuplicates(results, linkSet)

                    if (previousSet != linkSet):
                        body.send_keys(Keys.PAGE_DOWN)
                        body.send_keys(Keys.PAGE_DOWN)
                        tries = 0
                    else:
                        tries += 1
                except (StaleElementReferenceException):
                    pass
        except KeyboardInterrupt:
            pass

        self._links = results
    
    # class will write to CSV, download images
    def ScrapeLinkset(self):
        loopCount = 1
        for link in self._links:
            self._browser.get(link)
            print("(%d/%d): "%(loopCount, len(self._links)) + link)
            loopCount += 1
            image = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class='XiG zI7 iyn Hsu'] > img")))
            imageLink = self.__GetHighResImage(image.get_attribute('src'))
            print("Obtained: " + imageLink)
            # Get caption
            # Write image to directory
            # Write caption to captions.txt in directory
            # Update main CSV

    def __GetHighResImage(self, imageLink):
        finalLink = ""
        if (imageLink.find("/236x/") != -1):
            finalLink = imageLink.replace("/236x/", "/736x/")
        return finalLink

    def __RemoveDuplicates(self, results, linkSet):
        helper = set(results)
        for link in linkSet:
            if link.get_attribute('href') not in helper:
                results.add(link.get_attribute('href'))
                helper.add(link.get_attribute('href'))
        return helper

    def __del__(self):
        if self._browser:
            self._browser.quit()
