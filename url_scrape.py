#!/usr/bin/python3
import sys
import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()

# Supply URL 
url = 'https://www.mutualofomaha.com/medicare-solutions/medicare-basics'
# Get URL 
page = requests.get(url)

# Parse HTML Page
soup = BeautifulSoup(page.content, 'html.parser')

# Single out P Tag
p = soup.find_all("p")




# Open file to write contents to
sys.stdout = open('scrape-me.txt', 'w')
# Extract text from <p> tags and Print contents to file
for p in p:
    print (p.get_text())
# Close file 
sys.stdout.close()


