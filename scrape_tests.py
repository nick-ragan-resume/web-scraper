import sys
import os
import re
import json


keywords = []

scraped_words = []

matched_words = []

duplicate_dict = {}
# open keyword file ... split on new line
keyword_file = open('import-file/upload_list.txt').read().split('\n')

# open scraped file ... split on new line
scraped_word_file = open('test-data.txt').read().split('\n')


for k in keyword_file:
    keywords.append(k)

for s in scraped_word_file:
    scraped_words.append(s)


print(scraped_words)



# loop through scraped file array
for scrape_data in scraped_words:
    for key_data in keywords:
        results = re.finditer(rf"{key_data}(?=[ !?.,])", scrape_data, re.IGNORECASE)
        for r in results:
            matched_words.append(r[0].capitalize())
        # if re.findall(rf"{key_data}(?=[?.,!<])", scrape_data, re.IGNORECASE):
        #     matched_words.append(key_data)

for i in matched_words:
    duplicate_dict[i]=matched_words.count(i)

j = json.dumps(duplicate_dict, indent=2)

print(j)

