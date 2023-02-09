import sys
import tkinter
from tkinter import ttk
from tkinter import *


class PlayGui:
    LIST_LEFT = 1
    LIST_RIGHT = 2
    controller = []
    root = tkinter.Tk()
    list_left = []
    list_right = []
    label = []
    bt_ok = []
    bt_start = []
    combo_test_choice = []
    combo_test_value = []

    def getRoot(self) -> Tk:
        return self.root

    def __init__(self, playController):
        self.controller = playController
        self.root.title('Learning new words')

        # ------------------------------------
        #  ---< C O N F I G U R A T I O N >---
        # ------------------------------------

        frm_configuration = tkinter.LabelFrame(self.root, text="Configuration")
        frm_configuration.grid(column=0, row=0, columnspan=2, pady=5, padx=10)

        self.combo_test_choice = tkinter.ttk.Combobox(frm_configuration, width=30)
        self.combo_test_choice.grid(column=0, row=0, columnspan=2, pady=5, padx=5)
        self.combo_test_choice['values'] = ('Test1', 'Test2', 'Test3')
        self.combo_test_choice.bind('<<ComboboxSelected>>', self.controller.test_type_selection)
        self.combo_test_value = tkinter.ttk.Combobox(frm_configuration, width=30)
        self.combo_test_value.grid(column=2, row=0, columnspan=2, pady=5, padx=5)
        self.combo_test_value['values'] = ('5', '10', '15', '20')

        self.bt_start = tkinter.Button(frm_configuration, text="Start", command=self.controller.start_command, width=10,
                                   height=2, state=tkinter.DISABLED)
        self.bt_start.grid(column=4, row=0, pady=10, padx=10)


        # Left frame
        frm_word_left = tkinter.LabelFrame(self.root, text="")
        frm_word_left.grid(column=0, row=1, pady=5, padx=10)
        self.list_left = tkinter.Listbox(frm_word_left, width=40, height=25)
        self.list_left.grid(column=0, row=0, pady=10, padx=10)

        # Right frame
        frm_word_right = tkinter.LabelFrame(self.root, text="")
        frm_word_right.grid(column=1, row=1, pady=5, padx=10)
        self.list_right = tkinter.Listbox(frm_word_right, width=40, height=25)
        self.list_right.grid(column=0, row=0, pady=10, padx=10)

        self.list_left.bind("<<ListboxSelect>>", self.controller.left_list_selection)
        self.list_right.bind("<<ListboxSelect>>", self.controller.right_list_selection)

        self.bt_ok = tkinter.Button(self.root, text="OK", command=self.controller.ok_command, width=50,
                                   height=2, state=tkinter.DISABLED)
        self.bt_ok.grid(column=0, row=2, columnspan=2, pady=10, padx=10)


    def enable_controls(self):
        self.bt_start['state'] = tkinter.NORMAL
        self.bt_ok['state'] = tkinter.NORMAL

    def add_words(self, where: int, words : []) -> None:
        if where == self.LIST_LEFT:
            list = self.list_left
        else:
            list = self.list_right
        for word in words:
            list.insert(END, word)


    def clear_words(self, where: int) -> None:
        list = []
        if where == self.LIST_LEFT:
            list = self.list_left
        else:
            list = self.list_right
        list.delete(0, END)




# *******************
# --- CONTROLLER ---
# *******************



class PlayController:
    db_connection = []
    gui = []

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def set_gui(self, gui) -> None:
        self.gui = gui

    def clear_all(self) -> None:
        self.gui.list_left.delete(0, END)
        self.gui.list_right.delete(0, END)


    def left_list_selection(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            new_index = selection[0]
            print("Left index:", new_index)
        else:
            print("No Selection")


    def right_list_selection(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            new_index = selection[0]
            print("Right index:", new_index)
        else:
            print("No Selection")

    def test_type_selection(self, event) -> None:
        selection = event.widget.get()
        if selection:
            new_value = selection
            print("Test index:", new_value)
            if new_value != "":
                self.gui.enable_controls()
        else:
            print("No Selection")


    def start_command(self):
        words = ["apple", "day", "nothing"]
        self.gui.add_words(PlayGui.LIST_LEFT, words)
        pass

    def ok_command(self):
        self.gui.clear_words(PlayGui.LIST_LEFT)
        pass


def run_play(db_conx) -> None:
    controller = PlayController(db_conx)
    gui = PlayGui(controller)
    controller.set_gui(gui)
    gui.getRoot().mainloop()
