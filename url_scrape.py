#!/usr/bin/python3
import os
import sys
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk

"""
Screen Scrape Websites and Check For Keywords in Paragraph Text

Libraries used in this project
https://docs.python.org/3.7/library/
https://docs.python.org/3.7/library/tkinter.html
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

"""

engine = Tk()
engine.withdraw()

class WindowSetup(object):
    def __init__(self, parent):
        # instantiate main instance
        self.parent = parent 
        self.parent.configure(background='#013A70')
        # init text widget
        self.text = Text(self.parent)
        # init styles widget
        self.f1_style = ttk.Style() 
        # styles for frame/window
        self.f1_style.configure('My.TFrame', background="black")
        self.f1 = ttk.Frame(self.parent, style='My.TFrame')
        # style for quit button
        self.f1_style.configure('TButton', foreground='#013A70')
        self.quit_Button = ttk.Button(self.parent, text="Quit Program", command=parent.quit)
        # positioning and configuration for frame/window
        self.parent.eval('tk::PlaceWindow %s center' % parent.winfo_pathname(parent.winfo_id()))
        self.parent.geometry("450x317") #450x317
        #self.parent.resizable(False, False)
        # title for frame/window
        self.parent.title("Website Parser Comparision Tool - (WPCT)")

        # grab logo image
        self.image = Image.open('assets/ezgif-2-18770de0fea5.gif')
        self.photo = ImageTk.PhotoImage(self.image)
        # image
        self.img_label = Label(self.parent, image=self.photo, width=70)
        self.img_label.pack()
        # image
        self.img_label.grid(column=1, row=0, sticky=(N), pady=20, padx=(1,1))

    def uploadAction(self,event=None):
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        print('select:', self.filename)
        return self.filename

    def interactions(self):
        self.url_Label_0 = ttk.Label(self.f1, text="              ")
        self.url_Label_1 = ttk.Label(self.f1, text="Enter URL To Parse ")
        self.url_Entry = ttk.Entry(self.f1)
        self.parse_data_Label = ttk.Label(self.f1, text="Data To Parse")
        self.upload_File = ttk.Label(self.f1, text="Upload Data File")
        self.upload_Button = ttk.Button(self.f1, text="Upload", command=self.uploadAction)
        self.start = ttk.Button(self.f1, text="Begin Parser", command=self.get_entries)

        # checkbox variables
        self.header_Var = BooleanVar()
        self.paragraph_Var = BooleanVar()
        self.attributes_Var = BooleanVar()
        # set checkbox values
        self.header_Var.set(False)
        self.paragraph_Var.set(False)
        self.attributes_Var.set(False)
        # add functionality to checkbox
        self.h_tag = ttk.Checkbutton(self.f1, text="Headers", variable=self.header_Var, onvalue=True)
        self.p_tag = ttk.Checkbutton(self.f1, text="Paragraph", variable=self.paragraph_Var, onvalue=True)
        self.a_tag = ttk.Checkbutton(self.f1, text="Attributes", variable=self.attributes_Var, onvalue=True)

    # layout for GUI
    def grid(self):
        self.f1.grid(column=0, row=0, sticky=(E, W, S, N))
        # blank line
        self.url_Label_0.grid(column=0, row=0, sticky=(N, E, S, W), padx=(10,10), pady=1)
        # url input and parse
        self.url_Label_1.grid(column=0, row=1, sticky=(N, E, S, W), padx=(10,1), pady=1)
        self.url_Entry.grid(column=0, row=2, sticky=(N, E, S, W), padx=(10,1), pady=1)
        # upload button
        self.upload_File.grid(column=0, row=5, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.upload_Button.grid(column=0, row=6, sticky=(E, W), padx=(10,130), pady=(1,1))
        # check boxes
        self.parse_data_Label.grid(column=0, row=3, sticky=(N, E, S, W), padx=(10,1), pady=(40,1))
        self.h_tag.grid(column=0, row=4, padx=(10, 1), pady=(1,1), sticky=(W))
        self.p_tag.grid(column=0, row=4, padx=(86,1), pady=(1,1), sticky=(W))
        self.a_tag.grid(column=0, row=4, padx=(175,1), pady=(1,1), sticky=(W))
        # quit button 
        self.quit_Button.grid(column=1, row=0, sticky=(S), pady=10, padx=10)
        # start button... Need to Call Function to send back and grab data from [upload; one,two,three; url-entry]
        self.start.grid(column=0, row=7, sticky=(W, E), padx=(10,1), pady=(40,1))
        # need to check what these do
        self.parent.columnconfigure(0, weight=1)# weight determines how much of the available space a row or column should occupy relative to the other rows or columns
        self.parent.rowconfigure(0, weight=1)


    def get_entries(self):
        # grab entry values
        self.url_Entry_Val = self.url_Entry.get()
        self.header_Entry_Val = self.header_Var.get()
        self.paragraph_Entry_Val = self.paragraph_Var.get()
        self.attribute_Entry_Val = self.attributes_Var.get()
        # validate entries
        print("\n\n")
        print("Entry 1 = ", self.header_Entry_Val, ", ", "Entry 2 = ", self.paragraph_Entry_Val, ", ", "Entry 3 = ", self.attribute_Entry_Val)
        # check for .txt file
        try:
            if self.filename:
                print("File that you uploaded", self.filename)
        except:
            print("There is no uploaded file... ")
            self.filename = None
        # check for url
        try:
            if self.url_Entry_Val:
                print('here is your url: ', self.url_Entry_Val)
                # start processing
                self.parse_url()
        except:
            print('Please try entering a new URL... ')
        
    # parse website url
    def parse_url(self):
        url = self.url_Entry_Val
        url_page = requests.get(url)
        soup = BeautifulSoup(url_page.content, 'html.parser')
        pg = soup.find_all("p")
        writeable_file = open('scrape-me.txt', 'w')
        for remove_tags in pg:
            writeable_file.write(remove_tags.text + '\n')
        writeable_file.close()

        ###### need to allow for other parsing options such as iframe

        # soup2 = BeautifulSoup(url_page.content, 'html.parser')
        # tg = soup.find_all("p")
        # append_writeable_file = open('scrape-me.txt', 'a')
        # append_writeable_file.write('PG2 variable ' + ' \n')
        # append_writeable_file.close()
        
        

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


        
### need to scan .txt file with the parsed data

### do error handlings

## connect Data to parse selections

###### need to allow for other parsing options such as iframe

## clear url input box

## regex for uploaded file (no special symbols, cases)



class DataScanner(object):
    def __init__(self, parent):
        pass


# Start GUI Engine
def main():
    eng = WindowSetup(engine)
    eng.load_screen()
    eng.interactions()
    eng.grid()
    engine.mainloop()
 
 
if __name__ == '__main__':
    main()
