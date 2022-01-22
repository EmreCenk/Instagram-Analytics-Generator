
import tkinter as tk
from tkinter import ttk
from typing import Callable
import inspect
from src.Handling_Data import utils

class TrueFalseComboBox(ttk.Combobox):
    def __init__(self, *args):
        super().__init__(*args, values = ["True", "False"], state = "readonly")

def run_func(func_to_run: Callable, ready_inputs=None) -> None:

    if ready_inputs is None: ready_inputs = {}


    def execute():
        args = []
        for result in entries:
            cur = result.get()
            if len(cur) == 0:
                warning["text"] = "Please fill out every parameter"
                return
            args.append(cur)
        warning["text"] = "Generating graph!"

        real_args = []
        print(args, types, entries, params)
        for i in range(len(args)):
            real_args.append(types[i](args[i]))
        func_to_run(*real_args)
    window = tk.Tk()
    window.title("Welcome to TutorialsPoint")
    window.geometry('400x400')
    window.configure(background="grey")

    params = []
    types = []
    things = inspect.signature(func_to_run)
    for arg in things.parameters:
        types.append(things.parameters[arg].annotation)
        params.append(arg)

    offset = 0.1
    width = 0.5
    labels = []
    entries = []
    for i in range(len(params)):
        labels.append(tk.Label(window, text=params[i]).place(relx=0, rely=offset*i, relwidth=width, relheight=offset, anchor="nw"))
        type_of_widget = {int: tk.Entry,
                          bool: TrueFalseComboBox,
                          str: tk.Entry}[types[i]]
        current = type_of_widget(window)
        current.place(relx=width, rely=offset*i, relwidth=1-width, relheight=offset, anchor="nw")
        if params[i] in ready_inputs: current.insert(0, ready_inputs[params[i]])

        entries.append(current)
    try: i
    except: return
    tk.Button(text = "Generate Graph", command = execute).place(relx=0.5, rely=offset*(i+1), relwidth=0.4, relheight=offset, anchor="n")
    warning = tk.Label(window, text = "")
    warning.place(relx=0.5, rely=offset * (i + 2), relwidth=0.4,
                                                             relheight=offset, anchor="n")
    window.mainloop()

if __name__ == '__main__':
    from src.Handling_Data.Visualizing_Data import InstagramDataVisualizer
    run_func(InstagramDataVisualizer.visualize_most_active_year, ready_inputs = {"path": "somepath"})







