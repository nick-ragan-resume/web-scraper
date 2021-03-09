import os
import sys
from bs4 import BeautifulSoup
import urllib3
import ssl


### 
handling exceptions
###

def check_Answer():
    answer = input()
    if answer.lower() == 'y':
        get_URL()
    elif answer.lower() == 'n':
        print('Exiting the program... ')
        sys.exit()
    else:
        print('You need to enter "y" for "yes or "n" for "no"')
        check_Answer()

def get_URL():
    try:
        print('Enter the URL you want to parse... ')
        # assign url input to variable
        the_url = input()
        parse_Title(the_url)
    except:
        print('You need to enter a URL... ')
        print('Would you like to continue? Y or N')
        check_Answer()
    else:
        print('No Exceptions Raised.. ')


def parse_Title(url):
    try:
        # open urllib3 pool manager
        req = urllib3.PoolManager()
        # get url
        res = req.request('GET', url)
        print('Here is the request... ', res)
    # handle http errors from get request
    except HTTPError as e:
        return None 
    try:
        # parse url data
        soup = BeautifulSoup(res.data, 'html.parser')
        title = soup.body.h1
        print('Here is the title.... ', title)
    # handle Attribute errors... 
    # if no tag exists it will hit an AttributeError
    except AttributeError as e:
        return None




def main():
  get_URL()

if __name__ == "__main__":
  main()









# # sample connecting classses

# import tkinter as tk
# from tkinter import ttk


# LARGEFONT =("Verdana", 35)

# class tkinterApp(tk.Tk):
	
# 	# __init__ function for class tkinterApp 
# 	def __init__(self, *args, **kwargs): 
		
# 		# __init__ function for class Tk
# 		tk.Tk.__init__(self, *args, **kwargs)
		
# 		# creating a container
# 		container = tk.Frame(self) 
# 		container.pack(side = "top", fill = "both", expand = True) 

# 		container.grid_rowconfigure(0, weight = 1)
# 		container.grid_columnconfigure(0, weight = 1)

# 		# initializing frames to an empty array
# 		self.frames = {} 

# 		# iterating through a tuple consisting
# 		# of the different page layouts
# 		for F in (StartPage, Page1, Page2):

# 			frame = F(container, self)

# 			# initializing frame of that object from
# 			# startpage, page1, page2 respectively with 
# 			# for loop
# 			self.frames[F] = frame 

# 			frame.grid(row = 0, column = 0, sticky ="nsew")

# 		self.show_frame(StartPage)

# 	# to display the current frame passed as
# 	# parameter
# 	def show_frame(self, cont):
# 		frame = self.frames[cont]
# 		frame.tkraise()

# # first window frame startpage

# class StartPage(tk.Frame):
# 	def __init__(self, parent, controller): 
# 		tk.Frame.__init__(self, parent)
		
# 		# label of frame Layout 2
# 		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
		
# 		# putting the grid in its place by using
# 		# grid
# 		label.grid(row = 0, column = 4, padx = 10, pady = 10) 

# 		button1 = ttk.Button(self, text ="Page 1",
# 		command = lambda : controller.show_frame(Page1))
	
# 		# putting the button in its place by
# 		# using grid
# 		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

# 		## button to show frame 2 with text layout2
# 		button2 = ttk.Button(self, text ="Page 2",
# 		command = lambda : controller.show_frame(Page2))
	
# 		# putting the button in its place by
# 		# using grid
# 		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		


# # second window frame page1 
# class Page1(tk.Frame):
	
# 	def __init__(self, parent, controller):
		
# 		tk.Frame.__init__(self, parent)
# 		label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
# 		label.grid(row = 0, column = 4, padx = 10, pady = 10)

# 		# button to show frame 2 with text
# 		# layout2
# 		button1 = ttk.Button(self, text ="StartPage",
# 							command = lambda : controller.show_frame(StartPage))
	
# 		# putting the button in its place 
# 		# by using grid
# 		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

# 		# button to show frame 2 with text
# 		# layout2
# 		button2 = ttk.Button(self, text ="Page 2",
# 							command = lambda : controller.show_frame(Page2))
	
# 		# putting the button in its place by 
# 		# using grid
# 		button2.grid(row = 2, column = 1, padx = 10, pady = 10)




# # third window frame page2
# class Page2(tk.Frame): 
# 	def __init__(self, parent, controller):
# 		tk.Frame.__init__(self, parent)
# 		label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
# 		label.grid(row = 0, column = 4, padx = 10, pady = 10)

# 		# button to show frame 2 with text
# 		# layout2
# 		button1 = ttk.Button(self, text ="Page 1",
# 							command = lambda : controller.show_frame(Page1))
	
# 		# putting the button in its place by 
# 		# using grid
# 		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

# 		# button to show frame 3 with text
# 		# layout3
# 		button2 = ttk.Button(self, text ="Startpage",
# 							command = lambda : controller.show_frame(StartPage))
	
# 		# putting the button in its place by
# 		# using grid
# 		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


# # Driver Code
# app = tkinterApp()
# app.mainloop()


    def validate_data(self):
        if self.url_Entry.get() and self.filename:
            self.error_message.grid_remove()
            self.get_entries()
        else:
            #need to add error message
            print('Alert!!! You need to enter a url, make a selection and upload a file.')
            self.error_message.grid()

    # validate checkboxes
    def validate_checkboxes(self):
        h = self.header_Entry_Val
        p = self.paragraph_Entry_Val
        i = self.iframe_Entry_Val

        if 1 in {h, p, i}:
            if h:
                print("Header Checkbox Value = ", h)
            else:
                print('Header Checkbox Value = ', h)
            if p:
                print("Paragraph Checkbox Value = ", p)
            else:
                print("Paragraph Checkbox Value = ", p)
            if i:
                print("Iframe Checkbox Value = ", i)
            else:
                print("Iframe Checkbox Value = ", i)
        else:
            self.error_message.grid()

    # validate .txt file upload
    def validate_txt_file(self):
        try:
            if self.filename:
                print("File that you uploaded", self.filename)
        except:
            print("There is no uploaded file... ")
            self.filename = None
            self.error_message.grid()

    # validate url
    def validate_url(self):
                if self.header_Entry_Val:
                    print('WE HAVE A HEADER')
                    #parse headers
                    h = Parser(the_url)
                    h.parse_url_headers()
                if self.paragraph_Entry_Val:
                    print('WE HAVE A PARAGRAPH')
                    #parse paragraph
                    p = Parser(the_url)
                    p.parse_url_paragraph()
                    print('just the paragraph val ')
                if self.iframe_Entry_Val:
                    print('WE HAVE A IFRAME')
                    #parse iframe
                    i = Parser(the_url)
                    i.parse_url_iframe()
                    print('just the iframe val ')    
        except:
            print('An error has occured validating the url. Please try entering a new URL... ')
            self.error_message.grid()

