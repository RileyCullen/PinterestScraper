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

# TODO 
#   1. Updated scraper so the user can enter root directory from shell

import sys, PinterestScraper, requests, bs4, csv, os, getpass, CSVHelper

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
    root = ''

    while(pinObj.GetLoginStatus() == False):
        email = GetEmail()
        password = GetPassword()
        pinObj.Login(email, password)

    print('Root directory: ' + pinObj.GetRoot() + '\n')

    while (isRunning):
        usrInput = input('[Pinterest_Scraper] $ ')
        tokens = usrInput.split(' ')

        if (tokens[0] == 'quit'):
            isRunning = False
        elif (tokens[0] == 'scrape'):
            keyword = input('Keyword: ')
            linkSetURL = input('What pinterest page do you wanna scrape? ')
            pinObj.GetLinkSet(linkSetURL, keyword)
            pinObj.ScrapeLinkset()
        elif (tokens[0] == 'help'):
            PrintCommandList()
        elif (tokens[0] == 'create'):
            if (len(tokens) == 3):
                if (tokens[1] == 'master' and tokens[2] == 'csv'):
                    print('root:%s'%pinObj.GetRoot())
                    CSVHelper.CreateMasterCSV(pinObj.GetRoot(), 'master.csv')
        elif (tokens[0] == 'set'):
            if (len(tokens) == 3):
                if (tokens[1] == 'root' and tokens[2] == 'directory'):
                    root = input('root: ')
                    if (not pinObj.SetRoot(root)):
                        print('Invalid root. Root could not be set!\n')
                elif (tokens[1] == 'image' and tokens[2] == 'bounds'):
                    hMin = input('horizontal min: ')
                    vMin = input('vertical min: ')
                    if (not pinObj.SetBounds(hMin, vMin)):
                        print('Invalid bounds. Bounds could not be set!\n')


# desc: Prints out the currently supported commands 
def PrintCommandList():
    print('\nCommands:\nscrape - runs Pinterest Scraper\nquit - Terminates program')
    print('\n')

# desc: Receives and returns the user's password
def GetPassword():
    return getpass.getpass('Password: ')

# desc: Receives and returns the user's email
def GetEmail():
    return input('Username: ')

if __name__ == '__main__':
    Main()