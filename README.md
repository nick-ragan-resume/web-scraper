#### To use the URL-SCRAPE tool

1. open a new terminal session
2. cd into the web-scraper directory
3. run the setup.py file  -  command:  . /setup.py

What this setup script does
    # This will check for and create an isolated python virtual environment (venv) if one is not found.
    # The script will then activate the virtual environment
    # Then it will check to see if the dependencies listed in requirements.txt are installed on the virtual environment
    # If they are installed it will start the program. 
    # If they are not installed this script will install all dependencies
    # These dependencies will be isolated from your main system so you can delete this tool directory and
    # Once the dependencies are installed on the virtual environment the tool will open 


### The main directory is called web-scraper 
### The main script is url_scrape.py


### To use the tool follow the directions:

1. Enter a url that you would like to parse
2. Keep the 'Data To Parse' checkbox selected
3. Upload your data file - this needs to be a text file of all the words you would like to search for
4. Click start to run the program
5. a report.txt file will be exported to your desktop on Mac devices - this will contain a list of all words that were matched and how many
   times they matched




