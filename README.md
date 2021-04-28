#### To use the URL-SCRAPE tool

# First time user?
Simply download and run the init-scraper.sh
    ./init-scraper.sh




# Already have the virtual environment and dependencies installed?
Open a new terminal session and follow these commands:
1. git clone https://github.com/nick-ragan-resume/web-scraper.git
2. cd web-scraper
3. python3 -m venv venv
4. pip3 install -r requirements.txt
5. python3 url_scrape.py

# Notes about files in this repo
  - The main directory is called web-scraper 
  - The main file is url_scrape.py




### How do I use this too? 

1. Enter a url that you would like to parse
2. Keep the 'Data To Parse' checkbox selected
3. Upload your data file - this needs to be a text file of all the words you would like to search for
4. Click start to run the program
5. a report.txt file will be exported to your desktop on Mac devices - this will contain a list of all words that were matched and how many
   times they matched






