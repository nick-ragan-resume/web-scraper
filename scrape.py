import re
import os
import sys

### this will be useful to remove footers so we don't have to waste time scrubbing that data
def remove_footer_from_data(data_file, scrubbed_file):
    ### this will remove footer
    for r in data_file:
        if '<footer' in r:
            break
    scrubbed_file.close()
    uploaded_file_sort()


def reg_exp_func():
    # while we loop through scrape.txt
    # and search for words from list
    # before we will allow for ----- (space >)
    # after we will allow for ----- (.?!< )
    word_1 = 'tags'
    word_2 = 'score'
    the_list = []
    parsed_file = open('scrape-html-max/scrape.txt').read().split('\n')
    the_string = '<div class="theclass">Hello this is a random string inside some tags</div>'
    # this lookahead allows for any one of these symbols after each word
    reg_ex_1 = re.search(rf"{word_1}(?=[< .!?])", the_string)
    # this lookbehind allows checks for one of these symbols before each word
    reg_ex_2 = re.search(rf"(?<=[> ]){word_2}", the_string)
    # combine look ahead and look behind
    reg_ex_3 = re.search(rf"(?<=[>]){word_2}|{word_2}(?=[< .,!?])", the_string)
    for p in parsed_file:
        the_list.append(p)

    ##### this will loop through file as a list and search regex 
    count = 0
    for l in the_list:
        if re.search(rf"(?<=[>]){word_2}|{word_2}(?=[< .,!?])", l):
            count += 1
            print(count)
    pass




def key_word_search():
    # create empty list for keyword file
    keywords = []

    # create empty list for  scraped file
    scraped_words = []

    # open keyword file ... split on new line
    keyword_file = open('import-file/upload_list.txt').read().split('\n')

    # open scraped file ... split on new line
    scraped_word_file = open('scrape-html-max/scrape.txt').read().split('\n')

    # loop through keyword file and append to empty list
    for k in keyword_file:
        keywords.append(k)

    # loop through scraped file and append to empty list
    for s in scraped_word_file:
        scraped_words.append(s)

    #####################
    # loop through scraped file array
    for scrape_data in scraped_words:
        for key_data in keywords:
            if re.search(rf"(?<=[>]){key_data}|{key_data}(?=[< .,!?])", scrape_data):
                print('yes')

    # loop through keyword file array

    # looop over scrapped file array with keyword array using our regex


key_word_search()







    #### STEPS
    # open parsed file in read mode and split on \n line
    # loop through file and append to a an empty list
    # loop through the appended list and do regex there


    ##### append results to a new results file

    #### export file

    #### have a new screen for help

    ### create input entry for searching for something specific

    ### make portable 
