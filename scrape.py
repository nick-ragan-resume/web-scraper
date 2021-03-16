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
    word_2 = 'Hello'
    the_string = '<div class="theclass">Hello this is a random string inside some tags</div>'
    # this lookahead allows for any one of these symbols after each word
    reg_ex_1 = re.search(rf"{word_1}(?=[< .!?])", the_string)
    # this lookbehind allows checks for one of these symbols before each word
    reg_ex_2 = re.search(rf"(?<=[> ]){word_2}", the_string)
    print(reg_ex_1)
    print(reg_ex_2)

def loop_over_files():
    # array of matched words
    matched_words = []
    uploaded_file = open('import-file/uploaded_list.txt').read()
    parsed_file = open('scrape-html-max/scrape.txt')

    pass


    # loop over files
    def loop_files(self, opened_file, upload_list):
        # passing through the opened file and uplaod list
        # need to loop through the opened file with the upload list
        print('\n\n\n\nWe are in the loop files method... Passing two things, opened_file and upload_list \n\n\n\n')
        matched_words = []
        with open(opened_file, 'r') as read_obj:
            for line in read_obj:
                for u in upload_list:
                    if u in line:
                        matched_words.append(u)

        print('\n\n\nPrinting matched words.... ', matched_words, '\n\n\n')
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