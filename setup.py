import sys
import os
from tkinter import Tk, Text, Label, BooleanVar, E, W, S, N, Toplevel, RAISED, LEFT, filedialog
import tkinter.font as font
import tkinter.ttk as ttk
from threading import Thread
from queue import Queue




engine = Tk()

class WindowSetup():
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(background='#013A70')
        self.myFont = font.Font(family='Helvetica', size=15)
        # window position
        self.parent.eval('tk::PlaceWindow %s center' % self.parent.winfo_pathname(self.parent.winfo_id()))
        self.parent.geometry("420x315") 
        self.parent.resizable(width=False, height=False)
        # window title
        self.parent.title("Website Parser Comparision Tool - (WPCT)")
        # queue and thread varaibles
        self.queue = Queue()
        self.threads = 4
        # text widget
        self.text = Text(self.parent)
        #pass myself to HomeFrame
        print('end')
        self.load_home_screen()

    def load_home_screen(self):
        l = Factory('LoadScreen')
        l(self.parent)
        HomeFrame(self.parent)




class HomeFrame():
    def __init__(self, parent):
        self.parent = parent
        print('We are in HomeFrame and passing Window Setup')
        self.layout()
    
    def layout(self):
        self.upload_button = ttk.Button(self.parent, width=5, text="Hello", command=self.hi)
        self.upload_button.grid(column=0, row=0, sticky=(E, W, N, S), padx=(10,110), pady=(1,1))
        self.upload_button2 = ttk.Button(self.parent, width=5, text="HelpFrame Class", command=self.open_Help)
        self.upload_button2.grid(column=1, row=0, sticky=(E, W, N, S), padx=(10,110), pady=(1,1))
        self.loading = ttk.Button(self.parent, width=5, text="HelpFrame Class", command=self.open_Loader)
        self.loading.grid(column=2, row=0, sticky=(E, W, N, S), padx=(10,110), pady=(1,1))

    def hi(self):
        print('hi')

    def open_Help(self):
        HelpFrame(self.parent)

    def open_Loader(self):
        LoadScreen(self.parent)






class HelpFrame():
    def __init__(self, parent):
        self.help = Toplevel(parent)
        print('In the helpFrame')





class destroy_frame():
    def __init__(self, kill_frame):
        pass


class uplaods():
    def __init__(self):
        self.filename = None
    
    def file_checker(self):
        path = "import-file"
        num_dirs = []
        dir = os.listdir('import-file')
        if len(dir) == 0:
            print('We have no fle in the directory')
        else:
            for files in os.walk(path):
                for filename in files:
                    if filename:
                        print("Printing filename... ", filename)
                        num_dirs.append(filename)

    def uploadAction(self, event=None):
        self.file_checker()
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        current_dir = os.path.abspath(os.getcwd())
        target = current_dir + '/import-file'

        if self.filename:
            # delete file contents
            self.delete_last_upload(current_dir, target)
            # move uploaded file to target
            dest = shutil.copy(self.filename, target)
            print('destination path... ', dest)
            self.rename_file()
        else:
            print('No file selected... ')
        return self.filename        

    def rename_file(self):
        dir = os.listdir('import-file')
        os.rename(rf'import-file/{dir[0]}', 'import-file/upload_list.txt')
        print(dir[0])
        
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





class LoadScreen():
    def __init__(self, parent):
        self.parent = parent
        self.loader = Toplevel(self.parent)
        self.loader.configure(background="#013A70")
        self.loader.geometry("420x315")
        # get frame/window width/height
        windowWidth = self.loader.winfo_reqwidth()
        windowHeight = self.loader.winfo_reqheight()
        # confirm frame/window width/height
        print("Width",windowWidth,"Height",windowHeight)
        # calculate center of frame/window width/height
        positionRight = int(self.loader.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.loader.winfo_screenheight()/2 - windowHeight/2)
        # positions frame/window
        self.loader.geometry("+{}+{}".format(positionRight, positionDown))
        # init percentage of load value
        self.percentage = 0
        # load screen text
        self.title = Label(self.loader, text=f"Loading...{self.percentage}", background="#013A70", foreground="white", pady=200, padx=200)
        self.title.pack()
        self.loading()

    # loading calculator
    def loading(self):
        """
        Length of time load shall last
        """
        self.percentage += 10
        self.title.config(text=f"Loading... {self.percentage}")
        if self.percentage == 100:
            self.loader.destroy()
            return
        else:
            engine.after(100,self.loading)  



# Factory Function
def Factory(show_window=None):
    """Factory Method"""
    display = {
        "HelpScreen": HelpFrame,
        "HomeScreen": HomeFrame,
        "LoadScreen": LoadScreen,
        "WindowSetup": WindowSetup
    }
    print('returning factory selection')
    return display[show_window]

# Select classes to run
def app_engine(class_selector):
    # this will select windows from the factory class
    pass


# Loop the program
if __name__ == '__main__':
    main_window = Factory("WindowSetup")(engine)
    engine.mainloop()
