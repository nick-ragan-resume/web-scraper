#!/usr/bin/python3
import os
import sys
from bs4 import BeautifulSoup
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import requests
import urllib3

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

        # text widget
        self.text = Text(self.parent)
        # styles widget
        self.f1_style = ttk.Style() 
        # styles config
        self.f1_style.configure('My.TFrame')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame')
        # styles/config buttons
        self.f1_style.configure('TButton', foreground='#013A70', font=('Helvetica', 15))
        self.quit_Button = ttk.Button(self.parent, text="Quit Program", command=parent.quit)
        self.start_Button = ttk.Button(self.parent, text="Start Parsing", command=self.get_entries)
        # window position
        self.parent.eval('tk::PlaceWindow %s center' % parent.winfo_pathname(parent.winfo_id()))
        self.parent.geometry("450x317") 
        # window title
        self.parent.title("Website Parser Comparision Tool - (WPCT)")

        # logo image
        self.image = Image.open('assets/ezgif-2-18770de0fea5.gif')
        self.photo = ImageTk.PhotoImage(self.image)
        self.img_label = Label(self.parent, image=self.photo, width=70)
        self.img_label.pack()

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
        
        # checkbox variables
        self.header_Var = BooleanVar()
        self.paragraph_Var = BooleanVar()
        self.iframe_Var = BooleanVar()
        self.div_Var = BooleanVar()
        self.attribute_Var = BooleanVar()
        self.other_Var = BooleanVar()
        # set checkbox values
        self.header_Var.set(False)
        self.paragraph_Var.set(False)
        self.iframe_Var.set(False)
        self.div_Var.set(False)
        self.attribute_Var.set(False)
        self.other_Var.set(False)
        # add functionality to checkbox
        self.h_tag = ttk.Checkbutton(self.f1, text="Headers", variable=self.header_Var, onvalue=True)
        self.p_tag = ttk.Checkbutton(self.f1, text="Paragraph", variable=self.paragraph_Var, onvalue=True)
        self.if_tag = ttk.Checkbutton(self.f1, text="Iframe", variable=self.iframe_Var, onvalue=True)
        # add functionality to checkbox
        self.d_tag = ttk.Checkbutton(self.f1, text="Div", variable=self.div_Var, onvalue=True)
        self.a_tag = ttk.Checkbutton(self.f1, text="Attribute", variable=self.attribute_Var, onvalue=True)
        self.o_tag = ttk.Checkbutton(self.f1, text="Other", variable=self.other_Var, onvalue=True)

        # main style grid
        self.f1.grid(column=0, row=0, sticky=(E, W, S, N))
        # blank line grid
        self.url_Label_0.grid(column=0, row=0, sticky=(N, E, S, W), padx=(10,10), pady=1)
        # url input and parse grid
        self.url_Label_1.grid(column=0, row=1, sticky=(N, E, S, W), padx=(10,1), pady=1)
        self.url_Entry.grid(column=0, row=2, sticky=(N, E, S, W), padx=(10,1), pady=1)
        # check boxes grid
        self.parse_data_Label.grid(column=0, row=3, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.h_tag.grid(column=0, row=4, padx=(10, 1), pady=(5,1), sticky=(W))
        self.p_tag.grid(column=0, row=4, padx=(86,1), pady=(5,1), sticky=(W))
        self.if_tag.grid(column=0, row=4, padx=(175,1), pady=(5,1), sticky=(W))
        self.d_tag.grid(column=0, row=5, padx=(10, 1), pady=(5,1), sticky=(W))
        self.a_tag.grid(column=0, row=5, padx=(86,1), pady=(5,1), sticky=(W))
        self.o_tag.grid(column=0, row=5, padx=(175,1), pady=(5,1), sticky=(W))
        # upload button grid
        self.upload_File.grid(column=0, row=6, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.upload_Button.grid(column=0, row=7, sticky=(E, W), padx=(10,130), pady=(1,1))
        # image grid
        self.img_label.grid(column=1, row=0, sticky=(N), pady=20, padx=(1,1))
        # quit button grid
        self.quit_Button.grid(column=1, row=0, sticky=(S), pady=10, padx=10)
        self.start_Button.grid(column=1, row=0, sticky=(S), pady=(1,80), padx=10)
        # need to check what these do
        self.parent.columnconfigure(0, weight=1)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.parent.rowconfigure(0, weight=1)

    def uploadAction(self,event=None):
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        print('select:', self.filename)
        return self.filename

    def get_entries(self):
        # grab entry values
        self.url_Entry_Val = self.url_Entry.get()
        self.header_Entry_Val = self.header_Var.get()
        self.paragraph_Entry_Val = self.paragraph_Var.get()
        self.iframe_Entry_Val = self.iframe_Var.get()
        self.div_Entry_Val = self.div_Var.get()
        self.attribute_Entry_Val = self.attribute_Var.get()
        self.other_Entry_Val = self.other_Var.get()
        try:
            self.validate_checkboxes()
            self.validate_txt_file()
            self.validate_url()
        except:
            print('Something went wrong at validation... ')

    # validate checkboxes
    def validate_checkboxes(self):
        if self.header_Entry_Val:
            print("Header Checkbox Value = ", self.header_Entry_Val)
        else:
            print('Header Checkbox Value = ', self.header_Entry_Val)
        if self.paragraph_Entry_Val:
            print("Paragraph Checkbox Value = ", self.paragraph_Entry_Val)
        else:
            print("Paragraph Checkbox Value = ", self.paragraph_Entry_Val)
        if self.iframe_Entry_Val:
            print("Iframe Checkbox Value = ", self.iframe_Entry_Val)
        else:
            print("Iframe Checkbox Value = ", self.iframe_Entry_Val)

    # validate .txt file upload
    def validate_txt_file(self):
        try:
            if self.filename:
                print("File that you uploaded", self.filename)
        except:
            print("There is no uploaded file... ")
            self.filename = None

    # validate url
    def validate_url(self):
        try:
            if self.url_Entry_Val:
                print('here is your url: ', self.url_Entry_Val)
                the_url = self.url_Entry_Val
                if self.header_Entry_Val:
                    #parse headers
                    h = Parser(the_url)
                    h.parse_url_headers()
                if self.paragraph_Entry_Val:
                    #parse paragraph
                    p = Parser(the_url)
                    p.parse_url_paragraph()
                    print('just the paragraph val ')
                if self.iframe_Entry_Val:
                    #parse iframe
                    i = Parser(the_url)
                    i.parse_url_iframe()
                    print('just the iframe val ')    
            else:
                print('No url entered or no parse data selected... ')
        except:
            print('An error has occured. Please try entering a new URL... ')
        

    # second screen - load screen
    def load_screen(self):
        # init top level frame/window
        self.a = Toplevel(self.parent) 
        self.a.configure(background='#013A70')
        # frame/window size
        self.a.geometry("450x317")
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

    # parse website headers
    def parse_url_headers(self):
        # this example pulls entire page
        url_page = requests.get(self.url)
        print('Printing URL Page... ', url_page)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        pg = soup.find_all('h1')
        print(pg)
        writeable_file = open('scrape-header/scrape-header.txt', 'w')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()
        print('Done printing header text to file... ')
        

    # parse website paragraphs
    def parse_url_paragraph(self):
        url_page = requests.get(self.url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        pg = soup.find_all('p')
        writeable_file = open('scrape-paragraph/scrape-paragraph.txt', 'w')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()
        print('Done printing paragraph text to file... ')

    # parse website iframe
    def parse_url_iframe(self):
        # this example pulls entire page
        url_page = requests.get(url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        p = soup.find_all(text=True)
        write_file = open('scrape-iframe/scrape-iframe.txt', 'w')
        write_file.write(data + '\n')
        write_file.close()


class Comparison(object):
    pass        
### need to scan .txt file with the parsed data

### do error handlings

###### need to allow for other parsing options such as iframe

## clear url input box

## regex for uploaded file (no special symbols, cases)


# Start GUI Engine
def main():
    eng = WindowSetup(engine)
    eng.load_screen()
    engine.mainloop()
 
 
if __name__ == '__main__':
    main()