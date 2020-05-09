# Cullen, Riley 
# PinterestScraper.py
# Created on 5/5/2020

# Revision History
#   May 5, 2020:
#       1). Main() and RunScraper defined and implemented
#   May 8, 2020:
#       1). PrintCommandList() defined and implemented

import sys, PinterestScraper, requests, bs4, csv, os

def Main():
    if len(sys.argv) == 3:
        RunScraper()
    else:
        print('invalid arguments... python3 scraper.py [email] [password] required')

def RunScraper():
    isRunning = True
    pinObj = PinterestScraper.PinterestScraper(sys.argv[1], sys.argv[2])

    print("Root directory: " + pinObj.GetRoot() + "\n")

    while (isRunning):
        usrInput = input("[Pinterest_Scraper] $ ")

        if (usrInput == 'quit'):
            isRunning = False
        elif (usrInput == 'scrape'):
            path = input("\nDirectory: ")
            keyword = input("Keyword: ")
            linkSetURL = input("What pinterest page do you wanna scrape? ")
            pinObj.GetLinkSet(linkSetURL, keyword, path)
            pinObj.ScrapeLinkset()
        elif (usrInput == 'help'):
            PrintCommandList()

def PrintCommandList():
    print("\nCommands:\nscrape - runs Pinterest Scraper\nquit - Terminates program")
    print("\n")

if __name__ == "__main__":
    Main()