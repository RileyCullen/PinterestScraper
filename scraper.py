# Cullen, Riley 
# PinterestScraper.py
# Created on /5/2020

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


if __name__ == "__main__":
    Main()