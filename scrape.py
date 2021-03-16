import re
import os
import sys



def file_handler():
    data_file = open('scrape-html-max/scrape.txt', 'r')
    scrubbed_file = open('scrubbed.txt', 'w')
    remove_footer_from_data(data_file, scrubbed_file)

def remove_footer_from_data(data_file, scrubbed_file):
    ### this will remove footer
    for r in data_file:
        if '<footer' in r:
            break
    scrubbed_file.close()
    uploaded_file_sort()

def uploaded_file_sort():
    #loop through uploaded list 
    uploaded_list = open('import-file/upload_list.txt').read()
    new_list = []
    for u in uploaded_list:
        new_list.append(u)
    scrubbed_file = open('scrubbed.txt', 'w')
    for n in new_list:
        scrubbed_file.write(n)
    scrubbed_file.close()
    return new_list

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
    for l in the_list:
        if re.search(rf"(?<=[>]){word_2}|{word_2}(?=[< .,!?])", l):
            print('YEEEEEESSSSS')

def loop_over_files():
    # array of matched words
    matched_words = []
    uploaded_file = open('import-file/upload_list.txt').read()
    parsed_file = 'scrape-html-max/scrape.txt'
    with open(parsed_file, 'r') as read_obj:
        # loops through every line in parsed data file
        for each_line in read_obj:
            # loops through every word in uploaded list
            for word_2 in uploaded_file:
                if word_2 in each_line:
                    pass
                    


def loop_over_files_2():
    # array of matched words
    matched_words = []
    # need to create a list of the uploaded_file
    uploaded_file = open('import-file/upload_list.txt').read()
    parsed_file = 'scrape-html-max/scrape.txt'
    with open(parsed_file, 'r') as read_obj:
        # loops through every word in uploaded list
        for r in read_obj:
            for word_2 in uploaded_file:
                if word_2 in r:
                    matched_words.append(word_2)
    print(matched_words)
         


#file_handler()
#uploaded_file_sort()
reg_exp_func()


# (?ms)^[ \t]*whattomatch+.*
# "
# gm
# (?ms) match the remainder of the pattern with the following effective flags: gms
# m modifier: multi line. Causes ^ and $ to match the begin/end of each line (not only begin/end of string)
# s modifier: single line. Dot matches newline characters
# ^ asserts position at start of a line
# Match a single character present in the list below [ \t]
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
#   matches the character   literally (case sensitive)
# \t matches a tab character (ASCII 9)
# class matches the characters class literally (case sensitive)
# = matches the character = literally (case sensitive)
# + matches the previous token between one and unlimited times, as many times as possible, giving back as needed (greedy)
# . matches any character 
# * matches the previous token between zero and unlimited times, as many times as possible, giving back as needed (greedy)
# Global pattern flags
# g modifier: global. All matches (don't return after first match)
# m modifier: multi line. Causes ^ and $ to match the begin/end of each line (not only begin/end of string)