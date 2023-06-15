from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from ttkthemes import ThemedTk
import os
from sheet_parser import SheetParser
from backend_main import *

class ViewScreen:
    def __init__(self, master):
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None    
        self.master = master
        self.master.title('Jazz Hands')
        self.master.geometry('600x800+400+40')
        self.master.resizable(0, 0)
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)

        # adding a two buttons to the sub menus
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

        self.top_frame = ttk.Frame(self.master, width=600, height=800)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)

        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=600, height=800)
        self.output.grid(row=0, column=0)
        
    # function for opening pdf files
    def open_file(self, filepath):
        # for test purposes
        #filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        # checking if the file exists
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.parser = SheetParser(self.path)
            data, numPages = self.parser.get_metadata()
            self.current_page = 0
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
    
    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.parser.get_page(self.current_page)
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.stringified_current_page = self.current_page + 1
            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)         

    def terminate_session(self):
        self.master.quit()
