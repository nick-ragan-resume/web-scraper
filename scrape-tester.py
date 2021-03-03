import os
import sys
from bs4 import BeautifulSoup
import urllib3
import ssl


#### 
# handling exceptions
####

def check_Answer():
    answer = input()
    if answer.lower() == 'y':
        get_URL()
    elif answer.lower() == 'n':
        print('Exiting the program... ')
        sys.exit()
    else:
        print('You need to enter "y" for "yes or "n" for "no"')
        check_Answer()

def get_URL():
    try:
        print('Enter the URL you want to parse... ')
        # assign url input to variable
        the_url = input()
        parse_Title(the_url)
    except:
        print('You need to enter a URL... ')
        print('Would you like to continue? Y or N')
        check_Answer()
    else:
        print('No Exceptions Raised.. ')


def parse_Title(url):
    try:
        # open urllib3 pool manager
        req = urllib3.PoolManager()
        # get url
        res = req.request('GET', url)
        print('Here is the request... ', res)
    # handle http errors from get request
    except HTTPError as e:
        return None 
    try:
        # parse url data
        soup = BeautifulSoup(res.data, 'html.parser')
        title = soup.body.h1
        print('Here is the title.... ', title)
    # handle Attribute errors... 
    # if no tag exists it will hit an AttributeError
    except AttributeError as e:
        return None


def main():
  get_URL()


if __name__ == "__main__":
  main()