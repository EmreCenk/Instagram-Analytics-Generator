
import tkinter as tk
from tkinter import ttk
from typing import Callable
import inspect

class TrueFalseComboBox(ttk.Combobox):
    def __init__(self, *args):
        super().__init__(*args, values = ["True", "False"], state = "readonly")
class IntervalComboBox(ttk.Combobox):
    def __init__(self, *args):
        super().__init__(*args, values = ["0", "1", "2", "3"], state = "readonly")


def run_func_via_gui(func_to_run: Callable, ready_inputs=None) -> None:

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
    type_to_widg = {int: tk.Entry,
                    bool: TrueFalseComboBox,
                    str: tk.Entry}

    for i in range(len(params)):
        labels.append(tk.Label(window, text=params[i]).place(relx=0, rely=offset*i, relwidth=width, relheight=offset, anchor="nw"))
        type_of_widget = type_to_widg[types[i]]

        if params[i] == "interval": current = IntervalComboBox(window)
        else: current = type_of_widget(window)

        current.place(relx=width, rely=offset*i, relwidth=1-width, relheight=offset, anchor="nw")
        if params[i] in ready_inputs:
            current.insert(0, ready_inputs[params[i]])
            current.configure(state = tk.DISABLED)

        entries.append(current)
    try: i
    except: return
    tk.Button(window, text = "Generate Graph", command = execute).place(relx=0.5, rely=offset*(i+1), relwidth=0.4, relheight=offset, anchor="n")
    warning = tk.Label(window, text = "")
    warning.place(relx=0.5, rely=offset * (i + 2), relwidth=0.4,
                                                             relheight=offset, anchor="n")
    window.mainloop()

if __name__ == '__main__':
    from src.Handling_Data.Visualizing_Data import InstagramDataVisualizer
    run_func_via_gui(InstagramDataVisualizer.visualize_active_chats, ready_inputs = {"path": "somepath"})







