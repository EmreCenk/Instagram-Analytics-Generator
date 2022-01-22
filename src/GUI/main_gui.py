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

    def place_file_button(self):
        #Places file selection button
        noneed, options = utils.get_all_user_created_static_methods(InstagramDataVisualizer)
        w = tk.StringVar(self.root)
        w.set(options[0])
        self.file_button = ttk.OptionMenu(self.main_frame,
                                          w,
                                          options[0],
                                          *options,
                                            # bg=self.BUTTON_COLOR,  # background color

                                            # fg = self.FOREGROUND_COLOR,
                                            # command=self.select_file
                                                      )



        self.file_button.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.1, anchor="n")
        self.file_button.scale=0.5
        self.widgets_with_text.append(self.file_button)
        self.all_widgets.append(self.file_button)

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


    def start(self,start_mainloop = True):
        #This function starts the gui

        self.place_file_button()
        self.place_path_label("aasdf")

        if start_mainloop:
            #Officially starting UI:
            self.root.mainloop()

if __name__ == '__main__':
    a = GUI()
    a.start()







