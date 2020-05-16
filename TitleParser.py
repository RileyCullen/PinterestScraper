# Cullen, Riley
# TitleParser.py
# Created on May 15, 2020

# Revision History:
#   May 15, 2020:
#       1). GetTitle defined and implemented

# TODO: If empty title, pass N/A

import bs4, requests

# desc: This function goes to a user specified url and gets that website's title 
#
# Parameters:
# ------------
# url - string
#       Holds the URL that we want to get the title from 
def GetTitle(url):
    title = "N/A"
    userAgent = {'User-agent': 'Mozilla/5.0'}
    requestsObject = requests.get(url, headers = userAgent)
    try:
        requestsObject.raise_for_status()
        soupObj = bs4.BeautifulSoup(requestsObject.text, "html.parser")

        title = soupObj.find("title").string
    except requests.exceptions.HTTPError:   
        pass
    except requests.exceptions.RequestException as exc:
        print(exc) 

    return title

print(GetTitle('http://www.ottoolkit.com/blog/?p=2484'))