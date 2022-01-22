import inspect
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.Handling_Data.Visualizing_Data import InstagramDataVisualizer
from src.Handling_Data import utils

class fake_event:
    # Every time the screen is resized (aka the user changes the size of the window), the GUI executes the function
    # named "resize_all_text". By default, tkinter passes in an event object as an argument. Sometimes,
    # I want to call the "resize_all_text" function just to resize everything and make sure everything is properly
    # sized. I created this "fake_event" class so that I could call the "resize_all_text" without an actual event object
    def __init__(self,_height):
        self.height = _height

class GUI():
    """This class stores everything that is a part of of the gui."""

    def __init__(self):


        self.height = 500  # This is the initial window size, everything will be resized if you change the size of the# window
        self.width= 800

        # initial font type:
        self.font_type = 'Segoe UI'
        self.font = (self.font_type, 13)

        #I had normally set up this color scheme, however everything was later changed to a window theme so the
        # following colors are basically useless now
        # self.BACKGROUND_COLOR = "#282c34"
        # self.BUTTON_COLOR = "#3C3A40"
        # self.FOREGROUND_COLOR = "white"



        self.widgets_with_text=[] #keeps track of all widgets that have text inside. We will loop through these
        # widgets and resize the text inside them to make sure that the text scales with the window size

        self.all_widgets=[] # a list of all widgets. This list is used when we want to clear the screen


        self.root = tk.Tk()  # Initializes root (root is basically a tkinter class that stores a bunch of functions
        # and variables

        self.root.title("Inventory Tracking")  # setting window title name


        #Here we set the theme to "vista". This is the closest replica of a windows theme that ttk has.
        #By the way, ttk is almost the same thing as tk. The only difference is that ttk is a "themed tk".
        self.style = ttk.Style()
        self.style.theme_use("vista")

        #initializing and placing canvas object (canvas opens the window):
        self.screen = tk.Canvas(self.root, width=self.width, height=self.height)
        self.screen.pack()

        # initializing background:

        self.main_frame = ttk.Frame(self.root)

        #The following line makes sure that every time the size of the window changes, the function "resize_all_text"
        # is called:
        self.main_frame.bind("<Configure>",self.resize_all_text)


        # Placing the background:
        self.main_frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor="n")




    def no_main_start(self):
        #Executes the "start" function without starting another loop.
        #We have to create a seperate function for this since we can't pass in paramaters when we are executing
        # functions through button clicks
        self.start(False)






    def resize_all_text(self, event):
        # This function goes through every widget that contains text inside it, and resizes the text fits inside the
        # new window. This function is called everytime the window is resized

        self.font = (self.font_type,event.height//25) #default font
        for widget in self.widgets_with_text:
            try:#If widget has an attribute called scale, then use that as the value
                scale=widget.scale
            except:#if the widget has no scale attribute, then set the scale value to 1
                scale=1


            try: #if the widget is a tk widget, we can use .config
                widget.config(font = (self.font[0],int(self.font[1]*scale)))
            except: #If the widget is a ttk widget, python will give an error if we try .config . ttk uses .configure
                print(widget, widget.scale)
                self.style.configure('my.TButton', font = (self.font[0],int(self.font[1]*scale)))
                self.style.configure("TMenubutton", font = (self.font[0],int(self.font[1]*scale)))
                try:widget["menu"].configure(ffont = (self.font[0],int(self.font[1]*scale)))
                except: pass

    def place_method_options(self):
        #Places file selection button
        self.graph_functions, options = utils.get_all_user_created_static_methods(InstagramDataVisualizer)
        self.graph_function_name_to_index = {}
        for i, func_name in enumerate(options):
            self.graph_function_name_to_index[func_name] = i
        self.graph_options = tk.StringVar(self.root)
        self.graph_options.set(options[0])
        self.method_options = ttk.OptionMenu(self.main_frame,
                                             self.graph_options,
                                             options[0],
                                             *options,
                                             # bg=self.BUTTON_COLOR,  # background color

                                             # fg = self.FOREGROUND_COLOR,
                                             # command=self.select_file
                                             )



        self.method_options.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.1, anchor="n")
        self.method_options.scale=0.5
        self.widgets_with_text.append(self.method_options)
        self.all_widgets.append(self.method_options)

    def place_path_label(self, path):
        #Places the text that shows which path the user has selected
        self.path_label = ttk.Label(
            self.main_frame,
            text="Selected: " + path,
            # bg=self.BACKGROUND_COLOR,
            font=self.font,
            # fg=self.FOREGROUND_COLOR,
        )

        #Setting up values:
        self.path_label.configure(anchor = "center")
        self.path_label.place(relx=0.5,rely=0.8,relw=1,relh=0.1,anchor="n") #relative coordinates
        self.path_label.scale=0.6 #text scale
        self.all_widgets.append(self.path_label)
        self.widgets_with_text.append(self.path_label)

    def generate_current_graph(self):
        func_index = self.graph_function_name_to_index[self.graph_options.get()]
        self.graph_functions[func_index](self.path_to_data)
    def place_generate_graph_button(self):
        self.generate_graph = ttk.Button(
            self.main_frame,
            text="Click To Generate Graph",

            command=self.generate_current_graph

        )

        #placing the button, and setting it's text scale:
        self.generate_graph.place(relx = 0.5,rely = 0.7,relwidth=0.2, relheight=0.1, anchor="n")
        self.generate_graph.scale=0.8

    def clear_widgets_with_text_list(self, things_to_avoid=None):
        if things_to_avoid is None:
            things_to_avoid=[]

        #deletes every widget inside the "widgets_with_text" list except the widgets that are in "things_to_avoid"
        for k in self.widgets_with_text:
            if k not in things_to_avoid:
                k.destroy()

        self.widgets_with_text=list(things_to_avoid)

    def clear_all(self, things_to_avoid = None):
        #deletes every widget on the screen except the widgets that are in "things_to_avoid"

        if things_to_avoid is None:
            things_to_avoid = []

        self.clear_widgets_with_text_list(things_to_avoid)
        for k in self.all_widgets:
            if k not in things_to_avoid:
                k.destroy()


        self.all_widgets=list(things_to_avoid)

    def proceed_to_search(self, force=False):

        #This function displays the page that the user makes searches in

        if len(self.folder_selected)<2: #Checking to see if a folder is selected
            self.path_label.config(text="Please Select a Folder")
            return None

        if not force: #The variable force is a boolean value that states whether we should display the warning
            # message or not
            proceed=tk.messagebox.askyesno(message="The folder you have selected will always be the default folder from "
                                                "now on. Are you sure you would like to proceed? This step is permanent. ")
            if not proceed:
                return None


        self.clear_all() #clears page


        #saves the default directory:
        import os
        print(os.getcwd())
        folder = open("default.txt","w+")
        folder.write(self.folder_selected)
        folder.close()
        self.path_to_data = self.folder_selected
        #creates an instance of "excel_searcher": (The code for the excel_searcher class is in the folder titled
        # "scraping_excel"


        #Creating a prompt/text:
        self.prompt = ttk.Label(self.main_frame,
                               # bg=self.BACKGROUND_COLOR,
                               text="Select which graph you would like to generate",
                               # fg = self.FOREGROUND_COLOR,
                               font=self.font,
                               # bd=0, )
                                )
        self.prompt.place(relx=0.5, rely=0.15, relheight=0.2, relwidth=1, anchor="n")
        self.prompt.configure(anchor="center")
        self.place_method_options()
        self.place_generate_graph_button()


    def select_file(self):

        #This function opens the file explorer

        self.file_button.config(text="Opening File Browser...")
        self.file_button.scale=0.8


        #the following line opens the file explorer and saves the path of the folder selected:
        self.folder_selected = filedialog.askdirectory()




        self.file_button.config(text="Change Folder")

        self.proceed_button = ttk.Button(
            self.main_frame,
            text="Click To Proceed",

            command=self.proceed_to_search

        )

        #placing the button, and setting it's text scale:
        self.proceed_button.place(relx = 0.5,rely = 0.7,relwidth=0.2, relheight=0.1, anchor="n")
        self.proceed_button.scale=0.8

        #placing the text that shows which path you selected:
        self.place_path_label(self.folder_selected)

        #adding widgets in the list:
        self.widgets_with_text.append(self.proceed_button)
        self.all_widgets.append(self.proceed_button)

        #Resizing text to fit:
        self.resize_all_text(fake_event(self.main_frame.winfo_height()))
    def place_file_button(self):
        #Places file selection button
        self.file_button = ttk.Button(self.main_frame,  # Since this will be the child of the initial frame
                            text="Select Folder",
                            # bg=self.BUTTON_COLOR,  # background color

                            # fg = self.FOREGROUND_COLOR,
                            command=self.select_file)  # We don't want any borders




        self.file_button.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.1, anchor="n")
        self.file_button.scale=1
        self.widgets_with_text.append(self.file_button)
        self.all_widgets.append(self.file_button)

    def start(self,start_mainloop = True):
        #We read the default.txt file:
        try:
            folder = open("default.txt", "r")
            default=folder.read()
            folder.close()
        except:
            folder = open("default.txt", "a+")
            default=folder.read()
            folder.close()

        self.path_to_data = default
        if default!="":
            #If there is no default folder selected, we set up the select file button:
            self.place_path_label(default)
            self.folder_selected=default
            self.proceed_to_search(True)

        else:
            #If there is a default folder selected, we skip directly to the search screen
            self.place_file_button()
        #This function starts the gui
        # self.place_file_button()
        # self.place_method_options()
        # self.place_path_label("aasdf")

        if start_mainloop:
            #Officially starting UI:
            self.root.mainloop()

if __name__ == '__main__':
    # a = GUI()
    # a.start()
    print(
        inspect.signature(utils.get_all_user_created_static_methods(InstagramDataVisualizer)[0][0])
    )






