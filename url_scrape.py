#!/usr/bin/python3
import os
import sys
from bs4 import BeautifulSoup
from tkinter import Tk, Text, Label, BooleanVar, E, W, S, N, Toplevel
import tkinter.font as font
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import requests
import urllib3
import shutil
import time
from threading import Thread
from queue import Queue
from random import random
import re

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
        self.quit_Button = ttk.Button(self.parent, text="Quit ", command=self.parent.quit)
        self.start_Button = ttk.Button(self.parent, text="Start", command=self.get_entries)
        self.clear_Button = ttk.Button(self.parent, text="Clear", command=self.destroy_f1_frame)
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
        # checkbox variables
        self.header_Var = BooleanVar()
        self.paragraph_Var = BooleanVar()
        self.divMax_Var = BooleanVar()
        self.div_Var = BooleanVar()
        # set checkbox values
        self.header_Var.set(False)
        self.paragraph_Var.set(False)
        self.divMax_Var.set(False)
        self.div_Var.set(False)
        # add functionality to checkbox
        self.h_tag = ttk.Checkbutton(self.f1, text="Headers", variable=self.header_Var, onvalue=True)
        self.p_tag = ttk.Checkbutton(self.f1, text="Paragraph", variable=self.paragraph_Var, onvalue=True)
        self.if_tag = ttk.Checkbutton(self.f1, text="Iframe-Div", variable=self.divMax_Var, onvalue=True)
        # add functionality to checkbox
        self.d_tag = ttk.Checkbutton(self.f1, text="Div", variable=self.div_Var, onvalue=True)
        # main style grid
        self.f1.grid(column=0, row=0, sticky=(E, W, S, N))
        # blank line grid
        self.url_Label_0.grid(column=0, row=0, sticky=(N, E, S, W), padx=(10,10), pady=1)
        # url input and parse grid
        self.url_Label_1.grid(column=0, row=1, sticky=(N, E, S, W), padx=(10,1), pady=1)
        self.url_Entry.grid(column=0, row=2, sticky=(N, E, S, W), padx=(10,1), pady=1)
        # check boxes grid
        self.parse_data_Label.grid(column=0, row=4, sticky=(N, E, S, W), padx=(10,1), pady=(10,1))
        self.h_tag.grid(column=0, row=4, padx=(10, 1), pady=(55,1), sticky=(W))
        self.p_tag.grid(column=0, row=4, padx=(86,1), pady=(55,1), sticky=(W))
        self.if_tag.grid(column=0, row=4, padx=(175,1), pady=(55,1), sticky=(W))
        self.d_tag.grid(column=0, row=6, padx=(10, 1), pady=(5,1), sticky=(W))
        # upload button grid
        self.upload_File.grid(column=0, row=7, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.upload_Button.grid(column=0, row=8, sticky=(E, W), padx=(10,130), pady=(1,1))
        # error message and go message
        self.done_message.grid(column=0, row=9, sticky=(N, S, E, W), pady=(20,1),padx=(10,1))
        self.done_message.grid_remove()
        self.error_message.grid(column=0, row=9, sticky=(N, S, E, W), pady=(20,1),padx=(10,1))
        self.error_message.grid_remove()
        self.go_message.grid(column=0, row=9, sticky=(N, S, E, W), pady=(20,1),padx=(10,1))
        self.go_message.grid_remove()
        # image grid
        self.img_label.grid(column=1, row=0, sticky=(N), pady=20, padx=(1,1))
        # quit button grid
        self.quit_Button.grid(column=1, row=0, sticky=(S), pady=(1,10), padx=(1,1))
        self.start_Button.grid(column=1, row=0, sticky=(S), pady=(1,120), padx=(1,1))
        self.clear_Button.grid(column=1, row=0, sticky=(S), pady=(1,90), padx=(1,1))
        # need to check what these do
        self.parent.columnconfigure(0, weight=1)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.parent.rowconfigure(0, weight=1)


    # second screen - load screen
    def load_screen(self):
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

    # handle any .txt upload file
    def uploadAction(self,event=None):
        """
        handles the uploaded data file
        """
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
            dest = shutil.move(self.filename, target)
            print('destination path... ', dest)
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
        This is the initial 'kick off' function when you click start
        We start by grabbing all values to varify what they are
        """
        # grab entry values
        try:
            self.url_Entry_Val = self.url_Entry.get()
            self.header_Entry_Val = self.header_Var.get()
            self.paragraph_Entry_Val = self.paragraph_Var.get()
            self.divMax_Entry_Val = self.divMax_Var.get()
            self.div_Entry_Val = self.div_Var.get()
            self.clear_lists()
            self.input_entries()
        except:
            self.error_message.grid()

    def clear_lists(self):
        """
        Clear prior lists of data bool vals
        """
        # clear url list
        self.urls.clear()
        # clear checkboxes list
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
        if self.header_Entry_Val:
            self.checkboxes.append(self.header_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [1] - array position
        if self.paragraph_Entry_Val:
            self.checkboxes.append(self.paragraph_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [2] - array position
        if self.divMax_Entry_Val:
            self.checkboxes.append(self.divMax_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [3] - array position
        if self.div_Entry_Val:
            self.checkboxes.append(self.div_Entry_Val)
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
        self.parse_list = ['h1', 'p', 'div', 'div']

    def parse_web(self):
        print('We are in, parse all.... ')
        # get the url
        url_page = requests.get(self.urls)
        print('Printing the url we received... ', url_page)
        # Get page content
        soup = BeautifulSoup(url_page.content, 'html.parser')
        self.assign_label(soup)

    def assign_label(self, soup):
        self.soup = soup
        list_to_parse = []
        if self.checkboxes[0]:
            list_to_parse.append('h1')
        else:
            list_to_parse.append(None)
        if self.checkboxes[1]:
            list_to_parse.append('p')
        else:
            list_to_parse.append(None)
        if self.checkboxes[2]:
            list_to_parse.append('div')
        else:
            list_to_parse.append(None)
        if self.checkboxes[3]:
            list_to_parse.append('div')
        else:
            list_to_parse.append(None)

        self.parse_data(list_to_parse)

    def parse_data(self, list_to_parse):
        list_of_vals = list_to_parse
        print('\n\n\n\n\nPrint list_of_vals', list_of_vals)
        headers = self.soup.find_all(list_of_vals[0])
        paragraphs = self.soup.find_all(list_of_vals[1])
        div_max = self.soup.find_all(list_of_vals[2])
        div = self.soup.find_all(list_of_vals[3])

        # erase file data
        self.erase_file()

        # parse data
        if list_of_vals[0] == 'h1':
            print('\n\n\n\n WE HAVE HEADERS')
            self.continue_parsing(headers)
        if list_of_vals[1] == 'p':
            print('\n\n\n\n WE HAVE PARAGRAPHS')
            self.continue_parsing(paragraphs)
        if list_of_vals[2] == 'div':
            print('\n\n\n\n WE HAVE DIV MAX ')
            self.div_max_data(div_max)
        if list_of_vals[3] == 'div':
            print('\n\n\n\n WE HAVE DIVS')
            self.continue_parsing(div)

        self.compare_files()

    def erase_file(self):
        writeable_file = open('scrape/scrape.txt', 'w')
        writeable_file.close()

    def continue_parsing(self, data):
        writeable_file = open('scrape/scrape.txt', 'a+')
        for remove_tag in data:
            writeable_file.write(remove_tag.text + '\n')
        writeable_file.close()

    def div_max_data(self, data):
        writeable_file = open('scrape/scrape.txt', 'a+')

        divider = []
        for d in data:
            divider.append(str(d))

        for remove_tag in divider:
            writeable_file.write(remove_tag)
        writeable_file.close()
        pass

    def compare_files(self):
        ComparisonTool()



# Compare Upload File to Parsed URL
class ComparisonTool(object):
    
    def __init__(self):
        self.printstatement = 'Hi there!!'
        print(self.printstatement)
        

        # clean file
        string = open('scrape/scrape.txt').read()
        new_str = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\S', ' ', string)
        open('cleaned-file/cleaned.txt', 'w').write(new_str)

        # Read lines as a list
        fh = open("cleaned-file/cleaned.txt", "r")
        lines = fh.readlines()
        fh.close()

        # Weed out blank lines with filter
        lines = filter(lambda x: not x.isspace(), lines)

        # Write
        fh = open("cleaned-file/cleaned.txt", "w")
        fh.write("".join(lines))
        # should also work instead of joining the list:
        # fh.writelines(lines)
        fh.close()
        pass
    ## clean scrape.txt

    ## grab uploaded data file and clean

    # combine all parsed files into one

    # erase prior data in files

    # loop uploaded data file over combined file

    # create new data file of matches
      


# Start GUI Engine
def main():
    eng = WindowSetup(engine)
    eng.load_screen()
    engine.mainloop()
 
 
if __name__ == '__main__':
    main()