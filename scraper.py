import sys, PinterestScraper

def Main():
    if len(sys.argv) == 3:
        pinObj = PinterestScraper.PinterestScraper(sys.argv[1], sys.argv[2])
        linkSetURL = input("What pinterest page do you wanna scrape? ")
        pinObj.GetLinkSet(linkSetURL)
    else:
        print('invalid arguments... python3 scraper.py [email] [password] required')

if __name__ == "__main__":
    Main()