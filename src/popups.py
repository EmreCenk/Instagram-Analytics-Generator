# Importing required modules

import tkinter as tk
import tkinter.scrolledtext as st

def popupmsg(message: str, title_in_popup: str = "", title: str = "") -> None:
    """
    Creates a resizable popup with a given message
    :param message: message to display in popup
    :param title_in_popup: title to display inside of the window
    :param title: name of title for window
    :return: None
    """
    # Creating tkinter window
    win = tk.Tk()
    win.title(title)

    # Title Label
    a = tk.Label(win,
             text=title_in_popup,
             font=("Times New Roman", 15),
             )
    a.place(relx=0.5, rely=0, relwidth=1, relheight=0.1, anchor="n")
    # Creating scrolled text area
    # widget with Read only by
    # disabling the state
    text_area = st.ScrolledText(win,
                                width=30,
                                height=8,
                                font=("Times New Roman",
                                      15))

    text_area.place(relx=0.5, rely=0.1, relwidth=0.6, relheight=0.8, anchor="n")

    # Inserting Text which is read only
    text_area.insert(tk.INSERT,
                     message)

    # Making the text read only
    text_area.configure(state='disabled')
    win.mainloop()

if __name__ == '__main__':
    popupmsg("alpha\n"*100, "beta", "particles")