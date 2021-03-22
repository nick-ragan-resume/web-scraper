#!/usr/bin/python3
import os
from os.path import expanduser
import sys
import json
from bs4 import BeautifulSoup
import requests
from tkinter import Tk, Text, Label, BooleanVar, E, W, S, N, Toplevel
import tkinter.font as font
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
#import urllib3
import shutil
import time
from threading import Thread
from queue import Queue
from random import random
import re
from collections import Counter


"""
Screen Scrape Websites and Check For Keywords in Paragraph Text
Libraries used in this project
https://docs.python.org/3.7/library/
https://docs.python.org/3.7/library/tkinter.html
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""


# Start tkinter.Tk()
engine = Tk()

class WindowSetup(object):
    def __init__(self, parent):

        """ 
        Set up the main tkinter instance
        Configure the main window, font, background color, size, title, threading and Queue instance
        """
        # main instance
        self.parent = parent 
        self.parent.configure(background='#013A70')
        self.myFont = font.Font(family='Helvetica', size=15)

        # window position
        self.parent.eval('tk::PlaceWindow %s center' % self.parent.winfo_pathname(self.parent.winfo_id()))
        self.parent.geometry("420x315") 

        # window title
        self.parent.title("Website Parser Comparision Tool - (WPCT)")
        self.queue = Queue()
        self.threads = 4
        self.setup()

    def setup(self):
        """
        Sets program variables that can be cleared upon "Clear" button function "destroy_f1_frame"
        Setup styles for window, buttons, labels, and grids
        """
        # variables
        self.urls = []
        self.url_data = False
        self.checkboxes = []
        self.checkboxes_val = False
        self.filename = None
        self.upload_val = False

        # text widget
        self.text = Text(self.parent)

        # styles widget
        self.f1_style = ttk.Style() 

        # styles config
        self.f1_style.configure('My.TFrame')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame')

        # styles/config buttons
        self.f1_style.configure('TButton', foreground='#013A70', font=('Helvetica', 15))
        self.quit_Button = ttk.Button(self.parent, width=5, text="Quit ", command=self.parent.quit)
        self.start_Button = ttk.Button(self.f1, width=5, text="Start", command=self.get_entries)
        self.clear_Button = ttk.Button(self.parent, width=5, text="Clear", command=self.destroy_f1_frame)

        # logo image
        self.image = Image.open('assets/ezgif-2-18770de0fea5.gif')
        self.photo = ImageTk.PhotoImage(self.image)
        self.img_label = Label(self.parent, image=self.photo, width=70)

        # label stuff
        self.url_Label_0 = ttk.Label(self.f1, text="              ")
        self.url_Label_1 = ttk.Label(self.f1, text="Enter URL To Parse ")
        self.url_Label_1['font'] = self.myFont
        self.url_Entry = ttk.Entry(self.f1)
        self.parse_data_Label = ttk.Label(self.f1, text="Data To Parse")
        self.parse_data_Label['font'] = self.myFont
        self.upload_File = ttk.Label(self.f1, text="Upload Data File")
        self.upload_File['font'] = self.myFont
        self.upload_Button = ttk.Button(self.f1, text="Upload", command=self.uploadAction)
        self.error_message = ttk.Label(self.f1, foreground="red", text="Please complete all fields... ")
        self.go_message = ttk.Label(self.f1, foreground="blue", text="Working on parsing... ")
        self.done_message = ttk.Label(self.f1, foreground="#006400", text="Finished parsing this page... ")        
        self.finished_message = ttk.Label(background="white", foreground="blue", text="Finished... ")  
        self.clear_values_message = ttk.Label(self.f1, foreground="blue", text="Cleared the URL and any attached file... ") 

        # checkbox variables
        self.body_Var = BooleanVar()

        # set checkbox values
        self.body_Var.set(True)

        # add functionality to checkbox
        self.body_tag = ttk.Checkbutton(self.f1, text="Full HTML", variable=self.body_Var, onvalue=True)

        # main style grid
        self.f1.grid(column=0, row=0, sticky=(E, W, S, N))

        # blank line grid
        self.url_Label_0.grid(column=0, row=0, sticky=(N, E, S, W), padx=(10,10), pady=1)

        # url input and parse grid
        self.url_Label_1.grid(column=0, row=1, sticky=(N, E, S, W), padx=(10,1), pady=1)
        self.url_Entry.grid(column=0, row=2, sticky=(N, E, S, W), padx=(10,1), pady=1)

        # check boxes grid
        self.parse_data_Label.grid(column=0, row=4, sticky=(N, E, S, W), padx=(10,1), pady=(10,1))
        self.body_tag.grid(column=0, row=4, padx=(10,1), pady=(55,1), sticky=(W))

        # upload button grid
        self.upload_File.grid(column=0, row=7, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.upload_Button.grid(column=0, row=8, sticky=(E, W, N, S), padx=(10,110), pady=(1,1))

        # error message and go message
        self.done_message.grid(column=0, row=9, sticky=(E, W), pady=(2,1),padx=(10,1))
        self.done_message.grid_remove()
        self.error_message.grid(column=0, row=9, sticky=(E, W), pady=(2,1),padx=(10,1))
        self.error_message.grid_remove()
        self.go_message.grid(column=0, row=9, sticky=(N, S, E, W), pady=(2,1),padx=(10,1))
        self.go_message.grid_remove()
        self.clear_values_message.grid(column=0, row=9, sticky=(N, S, E, W), pady=(2,1),padx=(10,1))
        self.clear_values_message.grid_remove()
        
        # image grid
        self.img_label.grid(column=2, row=0, sticky=(N, W), pady=(0,0), padx=(0,0))
        self.start_Button.grid(column=1, row=10, sticky=(E, W), pady=(40,10), padx=(20,10))

        # quit button grid
        self.quit_Button.grid(column=2, row=0, sticky=(S), pady=(1,10), padx=(1,1))
        self.clear_Button.grid(column=2, row=0, sticky=(S), pady=(1,40), padx=(1,1))

        # need to check what these do
        self.parent.columnconfigure(0, weight=1)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=2)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.f1.rowconfigure(0, weight=2)

    # second screen - load screen
    def load_screen(self):
        """
        This is the initial load window --- maybe separate this and put a load bar in the future
        """
        # init top level frame/window
        self.a = Toplevel(self.parent) 
        self.a.configure(background='#013A70')
        # frame/window size
        self.a.geometry("420x315")
        # get frame/window width/height
        windowWidth = self.a.winfo_reqwidth()
        windowHeight = self.a.winfo_reqheight()
        # confirm frame/window width/height
        print("Width",windowWidth,"Height",windowHeight)
        # calculate center of frame/window width/height
        positionRight = int(self.a.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.a.winfo_screenheight()/2 - windowHeight/2)
        # positions frame/window
        self.a.geometry("+{}+{}".format(positionRight, positionDown))
        # init percentage of load value
        self.percentage = 0
        # load screen text
        self.title = Label(self.a, text=f"Loading...{self.percentage}", background="#013A70", foreground="white", pady=200)
        self.title.pack()
        # call loading function
        self.loading()

    # loading calculator
    def loading(self):
        """
        Length of time load shall last
        """
        self.percentage += 10
        self.title.config(text=f"Loading... ", background="#013A70")
        if self.percentage == 100:
            self.a.destroy()
            engine.deiconify()
            return
        else:
            engine.after(100,self.loading)  

    # clear url value
    def destroy_f1_frame(self):
        """
        resets setup to clear all values
        """
        print('CLEARED ALL VALUES!!!')
        if self.url_Entry:
            self.setup()


    def check_for_upload(self):
        """
        Check to see if an upload currently exists in the import-file directory
        """
        path = "import-file"
        num_dirs = [] 
        dir = os.listdir('import-file')
        if len(dir) == 0:
            print('we have nothing in directory')
        else:
            # do you want to use the prior upload
            for files in os.walk(path):
                for filename in files:
                    if filename:
                        print("Printing filename.... ",filename)
                        num_dirs.append(filename)

    # ask if they want to use prior upload and skip upload action
    def rename_upload(self):
        """
        Re-names any uploaded text file to "upload_list.txt"
        """
        dir = os.listdir('import-file')
        os.rename(rf'import-file/{dir[0]}', 'import-file/upload_list.txt')
        print(dir[0])
                    
    # handle any .txt upload file
    def uploadAction(self,event=None):
        """
        Opens the upload dialog box and allows for the selection of .txt files.
        shuttle the file to the import-file directory
        """
        self.check_for_upload()
        # open a txt file
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        print('\nselect:', self.filename)
        # get current directory and name target directory
        current_dir = os.path.abspath(os.getcwd())
        target = current_dir + '/import-file'
        
        if self.filename:
            # delete file contents
            self.delete_last_upload(current_dir, target)
            # move uploaded file to target
            dest = shutil.copy(self.filename, target)
            print('destination path... ', dest)
            self.rename_upload()
        else:
            print('No file selected... ')
        return self.filename

    
    def delete_last_upload(self, current, target):
        """
        deletes the last known uploaded data file
        """
        current_dir = current
        target = target
        print('current... ', current_dir)
        print('target... ', target)
        # remove all files from target directory
        for f in os.listdir(target):
            if not f.endswith(".txt"):
                continue
            os.remove(os.path.join(target, f))

    def get_entries(self):
        """
        This is the initial 'kick off' function when you click start to run the program
        We start by grabbing all
        All values are required to continue
        """
        # grab entry values
        try:
            self.url_Entry_Val = self.url_Entry.get()
            self.body_Entry_Val = self.body_Var.get()
            self.clear_lists()
            self.input_entries()
        except:
            self.error_message.grid()

    def clear_lists(self):
        """
        Clear prior lists of data bool vals
        """
        # clear url list values
        self.urls.clear()
        # clear checkboxes list values
        self.checkboxes.clear()

    # organize entries
    def input_entries(self):
        """
        Create new lists of data bool vals
        """
        print('input_entries method... \n')
        # [0] - array position
        if self.url_Entry_Val:
            self.urls.append(self.url_Entry_Val)
        else:
            self.urls.append(False)
        # [0] - array position
        if self.body_Entry_Val:
            self.checkboxes.append(self.body_Entry_Val)
        else:
            self.checkboxes.append(False)
        # print results to terminal
        print('I am printing the urls... ', self.urls)
        print('I am printing the checkboxes... ', self.checkboxes)
        # call validation methods - validate: url, checkboxes, upload
        self.validate_url_entry(self.urls), self.validate_checkboxes(self.checkboxes), self.validate_upload(self.filename)
        self.validate_all()

    # validate url entries
    def validate_url_entry(self, urls):
        """
        validate that a url was entered
        """
        print('validate url entry method... \n')
        for u in self.urls:
            if u:
                print('URL to parse... ', urls)
                self.url_data = True
            else:
                self.url_data = False
            return self.url_data

    # validate checkboxes
    def validate_checkboxes(self, checkboxes):
        """
        validate that a checkbox was selected
        """
        print('validate checkboxes method... \n')
        for c in checkboxes:
            if c == True:
                print('Checkbox value found...  ', c)
                self.checkboxes_val = True
                break
            else:
                print('No checkbox value... ', c)
                self.checkboxes_val = False
        return self.checkboxes_val

    # validate uploads 
    def validate_upload(self, upload_item):
        """
        validate that a file was uploaded
        """
        print('validate upload method... \n')
        if self.filename:
            self.upload_val = True
            print("File that you uploaded", upload_item)
        else:
            self.upload_val = False
        return self.upload_val

    # check to see if there is at least one entry per selection
    def validate_all(self):
        """
        This will confirm we have at least one value per entry item
        """
        print('validating all method... \n')
        if self.url_data and self.checkboxes_val and self.upload_val:
            # queue messaging jobs
            self.job_list()
        else:
            print('We are missing some stuff!!!! ')
            print('printing the val of the url... ', self.url_data)
            print('printing the val of the checkbox... ',self.checkboxes_val)
            print('printing the val of the upload... ',self.upload_val)
            self.supply_err_message()

    ###################################################################
    ###### JOB THREAD AND QUEUE         #############################
    ###############################################################

    # process queues 
    def processor(self):
        if self.queue.empty() == True:
            print("the Queue is empty!")
            sys.exit(1)
        try:
            # get all jobs that are in queues 
            job = self.queue.get()
            print("I'm operating on job item: %s" %(job))
            self.queue.task_done()
            self.supply_done_message()
        except:
            print("Failed to operate on job")

    # queue threaded jobs
    def job_list(self):
        # create array of [message method and run method] - make two different queues - one for messages and one for parsing
        self.jobs = [self.supply_go_message(), self.run_parser()]
        for job in self.jobs:
            print('inserting jobs into queue: ', job)
            self.queue.put(job)
            # run threader
            self.start_job_processor()

    # start jobs in order - this will create a thread per job
    def start_job_processor(self):
        for num in range(self.threads):
            print('We are printing num', num)
            # call the processor for threading
            th = Thread(target=self.processor)
            th.setDaemon(True)
            th.start()

    #################################################
    ###### END JOB QUEUE and THREADING      #############
    ###########################################################

    ###########################################################
    # Messaging that is queued              #############
    ##################################################

    def supply_go_message(self):
        self.error_message.grid_remove()
        self.go_message.grid()
        self.f1.update()

    def supply_done_message(self):
        self.error_message.grid_remove()
        self.go_message.grid_remove()
        self.done_message.grid()
        self.f1.update()
        self.remove_message()

    def supply_err_message(self):
        self.go_message.grid_remove()
        self.done_message.grid_remove()
        self.error_message.grid()
        self.f1.update()

    def remove_message(self):
        time.sleep(3)
        self.go_message.grid_remove()
        self.done_message.grid_remove()
        self.error_message.grid_remove()
        self.f1.update()        

    #############################################################
    # End Messages                   ################################
    #####################################################################

    ################### start parsing urls
    def run_parser(self):
        self.start_url_parsers()
        
    def start_url_parsers(self):
        print('ARRAY OF CHECKBOXES... ', self.checkboxes, '\n')
        parse = Parser(self.urls[0], self.checkboxes)
        return parse.parse_web()
      
# Passing something to class
class Parser(object):
    def __init__(self, urls, checkboxes):
        self.urls = urls
        self.checkboxes = checkboxes
        self.parse_list = ['body']

    def parse_web(self):
        """
        Grab url entered and request the url
        Create a Beautiful soup object of the url
        """
        print('\n\n We are in, parse all.... ')
        # get the url
        try:
            url_page = requests.get(self.urls)
            print('\n\nPrinting the url we received... ', url_page)
            # Get page content
            soup = BeautifulSoup(url_page.content, 'html.parser')
            print('\n\n Removing header tags from body of page') 
            soup.header.decompose()
            soup.footer.decompose()
            self.assign_label(soup)
        except:
            print('Error --- this is not a URL')
            error = 'ERROR: - This is not a correct URL'
            c = ComparisonTool()
            c.create_final_report(None, error)

    def assign_label(self, soup):
        """
        Create a list with the checkbox
        """
        self.soup = soup
        list_to_parse = []
        if self.checkboxes[0]:
            list_to_parse.append('body')
        else:
            list_to_parse.append(None)
        print('\n\n Printing list_to_parse..... ', list_to_parse)
        self.parse_data(list_to_parse)

    def parse_data(self, list_to_parse):
        """
        find the body tag and everthing contained within it from the Beautiful soup object
        """
        list_of_vals = list_to_parse
        data = self.soup.find_all(list_of_vals[0])# finding all within body tag --- list_of_vals[0] is 'body'
        

        # erase file data
        self.erase_files()

        # parse data
        if list_of_vals[0] == 'body':
            print('\n\n\n\n ............. WE HAVE HTML MAX DATA...................... \n\n')
            self.html_max_data(data)
        else:
            print("We do not have the html data")

    def erase_files(self):
        """
        erase scrape data file
        """
        print('\n\n\n We are erasing files!!! ')
        try:
            writeable_file = open('scrape-html-max/scrape.txt', 'w')
            writeable_file.close()
            print('\n\n opened file to erase and closed file.... ')
            writeable_file_2 = open('final-report/report.txt', 'w')
            writeable_file_2.close()
        except:
            print('\n\n Could not open file to erase')

    def html_max_data(self, data):
        """
        write data found from webpage to the scrape data file
        """
        writeable_file = open('scrape-html-max/scrape.txt', 'a+')
        body = []
        for d in data:
            body.append(str(d))
        for remove_tag in body:
            writeable_file.write(remove_tag)
        writeable_file.close()
        # scrub file 
        self.compare_files_html_max()

    def compare_files_html_max(self):
        html_file_max = 'body'
        compare = ComparisonTool()
        print('We are printingn self.urls before comparision tools......', self.urls, '\n\n\n')
        compare.key_word_search(html_file_max, self.urls)


# Compare Upload File to Parsed URL
class ComparisonTool(object):
    """
    This will clean parsed data and uploaded data
    """
    def __init__(self):
        self.open_html_max= False
        self.printstatement = 'Starting data clean in comparisontool... \n'
        print(self.printstatement)

    def key_word_search(self, html_file_max, urls):
        # check file size 
        self.check_filesize(html_file_max)

        # create empty list for keyword file
        keywords = []

        # create empty list for  scraped file
        scraped_words = []

        # final results
        matched_words = []

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

        # loop through scraped file array
        for scrape_data in scraped_words:
            for key_data in keywords:
                #finditer will find every occurance of the word. The lookahead will require one of the set characters to be behind the word
                results = re.finditer(rf"(?<=[ >]){key_data}(?=[ !?.,])", scrape_data, re.IGNORECASE)
                for r in results:
                    #This will grab all matches and capitalize them
                    matched_words.append(r[0].capitalize())


        if not matched_words:
            print('There were no matched words')
            self.create_final_report(None, urls)
        else:
            self.matched_word_counter(matched_words, urls)

    def matched_word_counter(self, matched_words, urls):
        duplicate_dict={}
        for i in matched_words:
            duplicate_dict[i]=matched_words.count(i)
        print('Printing duplicate dictionary......', duplicate_dict, '\n\n\n')
        self.create_final_report(duplicate_dict, urls)

    def create_final_report(self, duplicate_dict, urls):
        print('Creating final report!!! ')
        if duplicate_dict:
            # loop through matched words and write to report
            with open('final-report/report.txt', 'w') as file:
                file.write('Page URL: ' + '\n' + '---------' + '\n' + urls)
                file.write('                        \n\n\n\n')
                file.write('Matched Word        \n')
                file.write('--------------------------------------------------  \n\n')
                file.write(json.dumps(duplicate_dict, indent=2))
                file.write('                        \n\n\n\n')
                file.write('DISCLAIMER\n')
                file.write('-------------')
                file.write('\n***\nThese words are matches within the body copy of the web-page excluding \nanything in <header></header> and <footer></footer> tags.\n***')
                file.write('\n\n')
                file.close()
        elif not duplicate_dict:
            print('\n\n\n we found no matches!\n')
            # loop through matched words and write to report
            with open('final-report/report.txt', 'w') as file:
                file.write("We found nothing for URL: " + '\n\n' + urls)
                file.write('                        \n\n\n\n')
                file.close()        
        home = expanduser("~")
        src = 'final-report/report.txt'
        shutil.copy(src, home+'/Desktop')
    

    def check_filesize(self, file_val): 
        """
        Check stats of the scrape data file
        """
        file_stats = None
        try:  
            if file_val == 'body':
                file_size = os.stat('scrape-html-max/scrape.txt')
                file_stats = file_size.st_size
                print('Here are the file stats.... ',file_stats)
        except:
            print('something went wrong.')
        return file_stats

  
# Start GUI Engine
def main():
    eng = WindowSetup(engine)
    eng.load_screen()
    engine.mainloop()
 
 
if __name__ == '__main__':
    main()