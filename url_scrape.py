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
        #self.img_label.pack()

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
        self.start_Button.grid(column=1, row=0, sticky=(S), pady=(1,130), padx=(1,1))
        self.clear_Button.grid(column=1, row=0, sticky=(S), pady=(1,90), padx=(1,1))
        # need to check what these do
        self.parent.columnconfigure(0, weight=1)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.parent.rowconfigure(0, weight=1)

    # clear url value
    def destroy_f1_frame(self):
        if self.url_Entry:
            self.setup()

    def uploadAction(self,event=None):
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
        # grab entry values
        ## probably need to store data into two separte lists. One for URL and Entry File.... the other for checkboxes.
        try:
            self.url_Entry_Val = self.url_Entry.get()
            self.header_Entry_Val = self.header_Var.get()
            self.paragraph_Entry_Val = self.paragraph_Var.get()
            self.divMax_Entry_Val = self.divMax_Var.get()
            self.div_Entry_Val = self.div_Var.get()
            self.input_entries()
        except:
            self.error_message.grid()

    # organize entries
    def input_entries(self):
        self.urls.clear()
        self.checkboxes.clear()
        # [0]
        if self.url_Entry_Val:
            self.urls.append(self.url_Entry_Val)
        else:
            self.urls.append(False)
        # [0]
        if self.header_Entry_Val:
            self.checkboxes.append(self.header_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [1]
        if self.paragraph_Entry_Val:
            self.checkboxes.append(self.paragraph_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [2]
        if self.divMax_Entry_Val:
            self.checkboxes.append(self.divMax_Entry_Val)
        else:
            self.checkboxes.append(False)
        # [3]
        if self.div_Entry_Val:
            self.checkboxes.append(self.div_Entry_Val)
        else:
            self.checkboxes.append(False)
        # print to terminal results
        print('I am printing the urls... ', self.urls)
        print('I am printing the checkboxes... ', self.checkboxes)
        # call validation functions
        self.validate_url_entry(self.urls), self.validate_checkboxes(self.checkboxes), self.validate_upload(self.filename)
        self.validate_all()

    # validate url entries
    def validate_url_entry(self, urls):
        for f in self.urls:
            if f:
                # do something
                print('unpack urls and do stuff', urls)
                self.url_data = True
            else:
                self.url_data = False
            return self.url_data

    # validate checkboxes
    def validate_checkboxes(self, checkboxes):
        for c in checkboxes:
            if c == True:
                print('we have a c... ', c)
                self.checkboxes_val = True
                break
            else:
                print('we are changing c for some reason')
                self.checkboxes_val = False
        return self.checkboxes_val

    # validate uploads 
    def validate_upload(self, upload_item):
        if self.filename:
            self.upload_val = True
            print("File that you uploaded", upload_item)
        else:
            self.upload_val = False
        return self.upload_val

    # check to see if there is at least one entry per selection
    def validate_all(self):
        if self.url_data and self.checkboxes_val and self.upload_val:
            self.job_list()
        else:
            print('We are missing some stuff!!!! ')
            print('printing the val of the url... ', self.url_data)
            print('printing the val of the checkbox... ',self.checkboxes_val)
            print('printing the val of the upload... ',self.upload_val)
            self.supply_err_message()

    def processor(self):
        if self.queue.empty() == True:
            print("the Queue is empty!")
            sys.exit(1)
        try:
            job = self.queue.get()
            print("I'm operating on job item: %s" %(job))
            self.queue.task_done()
            self.supply_done_message()
        except:
            print("Failed to operate on job")

    def job_list(self):
        self.jobs = [self.supply_go_message(), self.run_parser()]
        for job in self.jobs:
            print('inserting jobs into queue: ')
            self.queue.put(job)
            self.start_job_processor()

    def start_job_processor(self):
        for num in range(self.threads):
            th = Thread(target=self.processor)
            th.setDaemon(True)
            th.start()

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

    def run_parser(self):
        self.start_url_parsers()
        
    def start_url_parsers(self):
        if self.header_Entry_Val:
            print('WE HAVE A HEADER')
            #parse headers
            h = Parser(self.urls[0])
            h.parse_url_headers()
        if self.paragraph_Entry_Val:
            print('WE HAVE A PARAGRAPH')
            #parse paragraph
            p = Parser(self.urls[0])
            p.parse_url_paragraph()
            print('just the paragraph val ')
        if self.divMax_Entry_Val:
            print('WE HAVE A divMax')
            #parse divMax
            i = Parser(self.urls[0])
            i.parse_url_divMax()
            print('just the divMax val ') 
        if self.div_Entry_Val:
            print('WE HAVE A DIV')
            #parse divMax
            i = Parser(self.urls[0])
            i.parse_url_div()
            print('just the div val ') 

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
        
    def loading(self):
        self.percentage += 10
        self.title.config(text=f"Loading... ", background="#013A70")
        if self.percentage == 100:
            self.a.destroy()
            engine.deiconify()
            return
        else:
            engine.after(100,self.loading)        

# Passing something to class
class Parser(object):
    def __init__(self, url):
        self.url = url
        print('In Parser class. Getting data for url... ', self.url)

    # need to clean these up
    def clean_file(self, file_name):
        print('Scrubbing file... ')
        file1 = open(file_name, 'w')
        print('File sizes... \n File Stats - ', os.stat(file1))
        file1.close()
        print('Finish scrubbing file... ')

    # parse website headers
    def parse_url_headers(self):
        url_page = requests.get(self.url)
        print('Printing URL Page... ', url_page)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        pg = soup.find_all('h1')
        writeable_file = open('scrape-header/scrape-header.txt', 'w+')
        # clear data
        self.clean_file(writeable_file)
        # add data
        print('\n Writing header file data... ')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()
        print('\n Done writing header file data... ')
        ComparisonTool()
        
    # parse website paragraphs
    def parse_url_paragraph(self):
        url_page = requests.get(self.url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        writeable_file = open('scrape-paragraph/scrape-paragraph.txt', 'w+')
        pg = soup.find_all('p')
        # clear data
        self.clean_file(writeable_file)
        # add data
        print('\n Writing paragraph file data... ')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()
        print('\n Done writing paragraph file data... ')
        ComparisonTool()

    # parse website divMax --- need to clean data file for this one
    def parse_url_divMax(self):
        url_page = requests.get(self.url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        pg = soup.find_all("div")
        paragraph = []
        for x in pg:
            paragraph.append(str(x))
        # clear data
        self.clean_file(writeable_file)
        writeable_file = open('scrape-iframe/scrape-iframe.txt', 'w+')
        for p in paragraph:
            writeable_file.write(p)
        writeable_file.close()
        ComparisonTool()

    # parse website div
    def parse_url_div(self):
        url_page = requests.get(self.url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        writeable_file = open('scrape-div/scrape-div.txt', 'w+')
        pg = soup.find_all('div')
        # clear data
        self.clean_file(writeable_file)
        # add data
        print('\n Writing div file data... ')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()
        print('\n Done writing div file data... ')
        ComparisonTool()



# Compare Upload File to Parsed URL
class ComparisonTool(object):
    
    def __init__(self):
        self.printstatement = 'Hi there!!'
        # open files - uploaded .txt file & any parsed file - w+
        self.header_file = open('scrape-header/scrape-header.txt', 'r+')
        self.paragraph_file = open('scrape-paragraph/scrape-paragraph.txt', 'r+')
        self.divMax_file = open('scrape-divMax/scrape-divMax.txt', 'r+')
        # self.text_file = open('import-file/text_file.txt', 'r+')
        
        print(self.printstatement)

    # clean files

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