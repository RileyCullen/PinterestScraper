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
#       2). ScrapeLinkSet defined and partially implemented (the image collection,
#           caption collection)
#       3). __GetHighResImage() defined and implemented
#   April 28, 2020
#       1). __DownloadImages(), __WriteToCaptionsFile(), __CheckForCaptionsTxt()
#           , and __CreateNewCaptionsText() defined and implemented
#   April 29, 2020
#       1). __CheckForCSV(), __CreateNewCSVFile(), and __WriteToCSV() defined
#           and implemented
#   May 5, 2020
#       1). ScrapeLinkSet updated to take in a keyword and download path from 
#           user
#       2). __CheckForDir() and __CreateNewDir() defined and implemented
#       3). GetRoot() defined and implemented
#   May 8, 2020
#       1). ScrapeLinkSet updated to take title 
#   May 9, 2020
#       1). ScrapeLinkSet updated to take in source as well
#       2). __WriteToCaptionsFile() --> __WriteToMetadataFile(). Also updated to
#           write source and title
#       3). __WriteToCSV updated to write title if the title exists and the 
#           caption if there is no title
#   May 12, 2020
#       1). __Login() --> Login() so that if the log in fails, user can try again
#       2). Login() returns True if the login was successful and False if the login
#           failed.
#       3). GetLoginStatus() defined and implemented
#   May 13, 2020
#       1). Login() updated so that if it fails, it sets hasLoggedIn to false
#       2). Function parameter documentation updated
#   May 15, 2020:
#       1). ScrapeLinkset() now gets title from external website if caption and 
#           title don't exist on pin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time, os, requests, csv, json, TitleParser

class PinterestScraper:
    # desc: initializes webdriver object and logs into pinterest
    # pre:  email, password must be valid
    # post: _browser object initialized
    #
    # Parameters:
    # ---------------
    # email : string
    #       Holds the email/username we will use to login to pinterest account
    #
    # password : string
    #       Holds the password we will use to login to pinterest account      
    def __init__(self, email, password):
        options = Options()
        options.headless = True
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self._browser = webdriver.Chrome('/Users/rileycullen/chromedriver', options=options)
        self._wait = WebDriverWait(self._browser, 2, ignored_exceptions=ignored_exceptions)
        self.__hasLoggedIn = False
        self.Login(email, password)
        self._links = set()
        self._root = "/Users/rileycullen/Seattle University/ShareNW Research Project - Documents/PinterestRepository"
        self._downloadPath = ""
        self._captionsFilename = "metadata.json"
        self._csvFilename = "infographics.csv"
        self._keyword = ""

    # desc: Logs into pinterest account with parameterized email/password
    # post: __hasLoggedIn initialized to True if login was successful and false if
    #       login was failed.
    #
    # Parameters:
    # ---------------
    # email : string
    #       Holds the email/username we will use to login to pinterest account
    #
    # password : string
    #       Holds the password we will use to login to pinterest account   
    def Login(self, email, password):
        loginURL = 'https://www.pinterest.com/login/'
        self._browser.get(loginURL)

        emailInput = self._browser.find_element_by_id("email")
        passwordInput = self._browser.find_element_by_id("password")

        emailInput.send_keys(email)
        passwordInput.send_keys(password)
        time.sleep(1)
        passwordInput.send_keys(Keys.RETURN)
    
        try:
            feedItem = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='homefeed-feed']")))
        except (TimeoutException):
            feedItem = 0

        if (feedItem != 0):
            self.__hasLoggedIn = True
        else:
            self.__hasLoggedIn = False

    # desc: Checks to see if there is a JSON file already in the directory that
    #       the user wants to write to
    def __CheckForCaptionsTxt(self):
        path = self._downloadPath + "/" + self._captionsFilename
        if(not os.path.isfile(path)):
            print(path + " not found... Creating a new copy")
            self.__CreateNewCaptionsTxt(path)
            print("Done")
        else:
            print(path + " found!")

    # desc: Creates a new JSON file to hold the image captions
    # 
    # Parameters:
    # ---------------
    # path : string holds the path of metadata.txt.
    def __CreateNewCaptionsTxt(self, path):
        with open(path, 'w') as f:
            data = {}
            data['image'] = []
            json.dump(data, f)
            f.close()

    # desc: Checks to see if there is a CSV file in the directory that the user
    #       wants to write to
    def __CheckForCSV(self):
        path = self._downloadPath + "/" + self._csvFilename
        if (not os.path.isfile(path)):
            print(path + " not found... Creating a new copy")
            self.__CreateNewCSVFile(path)
            print("Done")
        else:
            print(path + " found!")

    # desc: Creates a new CSV file
    # 
    # Parameters:
    # ---------------
    # csvPath : string
    #       Holds the path of infographics.csv in the filesystem.
    def __CreateNewCSVFile(self, csvPath):
        csvfile = open(csvPath, 'x', newline='')
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting = 
                                csv.QUOTE_MINIMAL)
        filewriter.writerow(['Image filename, Search keyword, Partial caption, URL'])
        csvfile.close()

    # desc: Checks if the user's directory exists
    def __CheckForDir(self):
        if (not os.path.isdir(self._downloadPath)):
            print(self._downloadPath + " not found... Creating a new directory")
            self.__CreateNewDir()
        else:
            print(self._downloadPath + " found!")

    # desc: Creates a new directory to save data to
    def __CreateNewDir(self):
        try:
            os.mkdir(self._downloadPath)
            print("Done")
        except OSError as err:
            print(err)

    # desc: Goes to linkSetURL and gets the set of links we will parse
    # pre:  linkSetURL must be a valid URL to a pinterest pin page, hasLoggedIn
    #       must be true
    # 
    # Parameters:
    # ---------------
    # linkSetURL : string
    #       Holds the pinterest board that we want to scrape for pins.
    #
    # keyword : string
    #       Holds the search term associated with the linkSetURL.
    #
    # path : string
    #       Holds the path on the filesystem we want to save the images and 
    #       metadata to.
    def GetLinkSet(self, linkSetURL, keyword, path):
        MAX_TRIES = 5
        tries = 0
        linkSet = []
        results = set()
        
        self._keyword = keyword
        self._downloadPath = self._root + '/' + path

        self.__CheckForDir()
        self.__CheckForCSV()
        self.__CheckForCaptionsTxt()

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
    
    # desc: Goes to each link within the linkset and downloads an image, caption,
    #       title, and source.
    # pre:  hasLoggedIn must be true
    def ScrapeLinkset(self):
        loopCount = 1
        successCount = 1
        captionContent = ""
        titleContent = ""
        srcContent = ""
        doesTitleExist = False
        
        for link in self._links:
            self._browser.get(link)
            imageName = self._keyword.replace(" ", "_") + "_%d.jpg"%(successCount)
            print("(%d/%d): "%(loopCount, len(self._links)) + link)
            loopCount += 1

            # Getting image download links
            image = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[class='XiG zI7 iyn Hsu'] > img")))
            imageLink = self.__GetHighResImage(image.get_attribute('src'))
            print("Image Link: " + imageLink)

            # Get title
            try:
                title = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class='lH1 dyH iFc ky3 pBj DrD IZT']")))
                titleContent = title.text
                doesTitleExist = True
            except (TimeoutException):
                doesTitleExist = False
                titleContent = "N/A"
            print("\nTitle content:\n\n" + titleContent)

            # Get source
            try:
                source = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='Jea jzS zI7 iyn Hsu'] a[class='linkModuleActionButton']")))
                srcContent = source.get_attribute('href')
            except:
                srcContent = "N/A"
            print("\nSource content:\n\n" + srcContent)

            # Get caption
            print("\nCaption content:\n")
            try:
                caption = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='tBJ dyH iFc MF7 pBj DrD IZT swG']")))
                captionContent = caption.text
            except (TimeoutException):
                captionContent = "N/A"

            print(captionContent)

            if (captionContent == "N/A" and titleContent == "N/A" and srcContent != "N/A"):
                titleContent = TitleParser.GetTitle(srcContent)                

            # Write image to directory
            imageSuccess = self.__DownloadImage(imageLink, imageName)
            # Write caption to captions.txt in directory
            if (imageSuccess):
                successCount += 1
                captionSuccess = self.__WriteToMetadataFile(imageName, titleContent, srcContent, captionContent)
                if (captionSuccess):
                    if (not doesTitleExist):
                        self.__WriteToCSVFile(imageName, captionContent[0 : 20], link)
                    else:
                        self.__WriteToCSVFile(imageName, titleContent[0 : 20], link)

            print()
            print()

    # desc: "Gets" the high res image by replacing /236x/ with /736x/ in the URL
    # 
    # Parameters:
    # ---------------
    # imageLink : string
    #       Holds the link to the image we want to download
    def __GetHighResImage(self, imageLink):
        finalLink = ""
        if (imageLink.find("/236x/") != -1):
            finalLink = imageLink.replace("/236x/", "/736x/")
        return finalLink

    # desc: Downloads picture to local disk
    # 
    # Parameters:
    # ---------------
    # imageLink : string
    #       Holds the link to the image we want to download
    #
    # imageName : string
    #       Holds the name we want to save the image as
    def __DownloadImage(self, imageLink, imageName):
        try:
            pictureRequest = requests.get(imageLink)
        except:
            print("Error: Image request failed")
            return False

        with open(self._downloadPath + '/' + imageName, 'wb') as f:
            f.write(pictureRequest.content)
            f.close()
            return True
        return False

    # desc: Writes captions to caption.txt on local disk
    # 
    # Parameters:
    # ---------------
    # imageName : string
    #       The name of the image we saved to the disk
    #
    # title : string
    #       Title associated with the saved image
    #
    # source : string
    #       Source associated with the saved image
    #
    # caption : string
    #       Caption associated with the saved image
    def __WriteToMetadataFile(self, imageName, title, source, caption):
        path = self._downloadPath + '/' + self._captionsFilename
        data = {}
        helper = 0
        with open(path,) as captionsFile:
            # content = "(" + imageName + "):\n\n" + caption + "\n\n"
            # captionsFile.write(content)
            helper = json.load(captionsFile)
            tmp = helper['image']

            data = {
                'image_filename': imageName,
                'title': title, 
                'source': source,
                'caption': caption
            }

            tmp.append(data)
            captionsFile.close()
        
        with open(path, 'w') as captionsFile:
            json.dump(helper, captionsFile, indent=4)
            captionsFile.close()
            return True

        return False

    # desc: Writes image name, keyword, a partial caption, and url to CSV
    # 
    # Parameters:
    # ---------------
    # imageName : string
    #       The name of the image we saved to the disk
    #
    # partialCaption : string
    #       A partial caption associated with the saved image
    #
    # url : string
    #       URL to the pin we want to download
    def __WriteToCSVFile(self, imageName, partialCaption, url):
        csvPath = self._downloadPath + "/" + self._csvFilename
        with open(csvPath, "a+", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([imageName, self._keyword, partialCaption, url])

    # desc: Removes duplicate links from linkset 
    # 
    # Parameters:
    # ---------------
    # results : set
    #       A set of pins scraped from the user given pinterest board with the 
    #       duplicate pins removed
    #
    # linkSet : list
    #       A list of pins from the most recent scrape of the board
    def __RemoveDuplicates(self, results, linkSet):
        helper = set(results)
        for link in linkSet:
            if link.get_attribute('href') not in helper:
                results.add(link.get_attribute('href'))
                helper.add(link.get_attribute('href'))
        return helper

    # desc: Returns the root directory the program will write to
    def GetRoot(self):
        return self._root

    def GetLoginStatus(self):
        return self.__hasLoggedIn

    # desc: Closes the selenium browser
    def __del__(self):
        if self._browser:
            self._browser.quit()