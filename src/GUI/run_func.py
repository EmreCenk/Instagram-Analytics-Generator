
import tkinter as tk
from typing import Callable
def run_func(func_to_run: Callable) -> None:
    window = tk.Tk()
    window.title("Welcome to TutorialsPoint")
    window.geometry('400x400')
    window.configure(background="grey")

    params = ["alpha", "beta", "theta"]
    offset = 0.1
    width = 0.5
    labels = []
    entries = []
    for i in range(len(params)):
        labels.append(tk.Label(window, text=params[i]).place(relx=0, rely=offset*i, relwidth=width, relheight=offset, anchor="nw"))
        entries.append(tk.Entry(window).place(relx=width, rely=offset*i, relwidth=1-width, relheight=offset, anchor="nw"))

    tk.Button(text = "Generate Graph").place(relx=0.5, rely=offset*(i+1), relwidth=0.4, relheight=offset, anchor="n")
    window.mainloop()

if __name__ == '__main__':
    run_func("")