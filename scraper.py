# Cullen, Riley 
# PinterestScraper.py
# Created on 5/5/2020

# Revision History
#   May 5, 2020:
#       1). Main() and RunScraper defined and implemented
#   May 8, 2020:
#       1). PrintCommandList() defined and implemented
#   May 12, 2020:
#       1). GetPassword() defined and implemented
#       2). User no longer enters password when starting program. Passwords are
#           entered after the program begins
#       3). GetEmail() defined and implemented
#   May 13, 2020:
#       1). Function documentation updated
#   May 16, 2020:
#       1). RunScraper updated so user only has to enter keyword instead of having
#           to enter keyword and directory (this is usually the same)

import sys, PinterestScraper, requests, bs4, csv, os, getpass

def Main():
    if len(sys.argv) == 2:
        password = GetPassword()
        RunScraper(password)
    else:
        print('invalid arguments... python3 scraper.py [email] required')

# desc: Main loop for scraper shell
# 
# Parameters:
# ------------
# password : string
#       Holds the user entered password
def RunScraper(password):
    isRunning = True
    pinObj = PinterestScraper.PinterestScraper(sys.argv[1], password)

    while(pinObj.GetLoginStatus() == False):
        email = GetEmail()
        password = GetPassword()
        pinObj.Login(email, password)

    print("Root directory: " + pinObj.GetRoot() + "\n")

    while (isRunning):
        usrInput = input("[Pinterest_Scraper] $ ")

        if (usrInput == 'quit'):
            isRunning = False
        elif (usrInput == 'scrape'):
            keyword = input("Keyword: ")
            linkSetURL = input("What pinterest page do you wanna scrape? ")
            pinObj.GetLinkSet(linkSetURL, keyword)
            pinObj.ScrapeLinkset()
        elif (usrInput == 'help'):
            PrintCommandList()

# desc: Prints out the currently supported commands 
def PrintCommandList():
    print("\nCommands:\nscrape - runs Pinterest Scraper\nquit - Terminates program")
    print("\n")

# desc: Receives and returns the user's password
def GetPassword():
    return getpass.getpass("Password: ")

# desc: Receives and returns the user's email
def GetEmail():
    return input("Username: ")

if __name__ == "__main__":
    Main()