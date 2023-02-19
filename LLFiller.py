import sys
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

class FillerGui:
    controller = []
    root = tkinter.Tk()
    db_connection = []
    varGr = IntVar()
    combo_word = []
    list_words = []
    combo_translation = []
    list_all_translations = []
    list_translations = []
    my_menu = []
    connection_menu = []
    word_rows = []
    bt_link_translation = []
    bt_unlink_translation = []
    bt_update = []
    bt_remove = []

    def getRoot(self) -> Tk:
        return self.root

    def enable_db_access(self) -> None:
        answer1 = simpledialog.askstring("DB password", "Please type DB password?",
                                         parent=self.root)
        if self.controller.db_connection.isPasswordOK(answer1):
            self.connection_menu.entryconfig("DB drop", state="normal")
            self.connection_menu.entryconfig("DB create", state="normal")
            self.connection_menu.entryconfig("DB stats reset", state="normal")
        else:
            messagebox.showerror('error', "Invalid password");

    def db_drop_tables(self) -> None:
        res = messagebox.askquestion('Drop table', 'Do you want to drop DB tables?')
        if res == 'yes':
            try:
                self.controller.db_connection.drop_tables()
            except Exception as e:
                messagebox.showerror('error on drop', e.with_traceback());
        elif res == 'no':
            pass

    def db_create_tables(self) -> None:
        res = messagebox.askquestion('Create tables', 'Do you want to create new DB tables?')
        if res == 'yes':
            try:
                self.controller.db_connection.create_tables()
            except Exception as e:
                messagebox.showerror('error on creation', e.with_traceback());
        elif res == 'no':
            pass

    def db_reset_stats(self) -> None:
        res = messagebox.askquestion('Reset training stats', 'Do you want to reset training statistics')
        if res == 'yes':
            try:
                self.controller.db_connection.reset_all_stats()
            except Exception as e:
                messagebox.showerror('error on statistics reset', e.with_traceback());
        elif res == 'no':
            pass

    def get_word_type(self) -> int:
        return self.varGr.get()

    def set_word_type(self, value: int) -> None:
        return self.varGr.set(value)

    def set_word_choices(self, words) -> None:
        self.combo_word.option_clear()
        self.combo_word["values"] = words

    def set_translation(self, word: str) -> None:
        return self.combo_translation.set(word)

    def set_translation_choices(self, words) -> None:
        self.combo_translation.option_clear()
        self.combo_translation["values"] = words
        #self.combo_translation.current(END)
        #for word in words:
        #    return self.combo_translation.insert(END, word)

    def get_current_word_value(self) -> str:
        return self.combo_word.get()

    def get_current_translation_value(self) -> str:
        return self.combo_translation.get()

    def add_current_translation(self, tr):
        self.list_translations.insert(END, tr)

    def __init__(self, fillerController):
        self.controller = fillerController
        self.root.title('Learning new words')

        # MENU
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.connection_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label="DB Management", menu=self.connection_menu)
        self.connection_menu.add_command(label="DB access", command=self.enable_db_access)
        self.connection_menu.add_command(label="DB drop", state="disabled", command=self.db_drop_tables)
        self.connection_menu.add_command(label="DB create", state="disabled", command=self.db_create_tables)
        self.connection_menu.add_command(label="DB stats reset", state="disabled", command=self.db_reset_stats)
        self.connection_menu.add_command(label="Exit", command=self.root.quit)

        # Word Type
        self.varGr.set(1)
        frm_word_type = tkinter.LabelFrame(self.root, text="Word type")
        WORD_TYPES = ["Verb", "Noun", "Adjective", "Adverb", "Pronoun", 'Expression']
        rb_value = 1;
        for rb_text in WORD_TYPES:
            tkinter.Radiobutton(frm_word_type, text=rb_text, variable=self.varGr, \
                                value=rb_value).grid(column=rb_value - 1, row=0)
            rb_value += 1
        frm_word_type.grid(column=0, row=0, pady=5, padx=10)

        # New Word 2 learn
        frm_word = tkinter.LabelFrame(self.root, text="New word to learn")
        frm_word.grid(column=0, row=1, pady=5, padx=10)

        # New word
        frm_word_entry = LabelFrame(frm_word, height=70)
        frm_word_entry.grid(column=0, row=0, padx=8, pady=10)
        self.combo_word = tkinter.ttk.Combobox(frm_word_entry, width=35)
        self.combo_word.grid(column=0, row=0, pady=10, padx=10)
        self.combo_word.bind("<Key>", self.controller.word_key_stroke)
        bt_add = tkinter.Button(frm_word_entry, text="Add", command=self.controller.add_word, width=30, height=3)
        bt_add.grid(column=0, row=1, pady=10, padx=10)
        self.bt_update = tkinter.Button(frm_word_entry, text="Update", command=self.controller.update_word, width=30,
                                   height=3, state=tkinter.DISABLED)
        self.bt_update.grid(column=0, row=2, pady=10, padx=10)

        self.bt_remove = tkinter.Button(frm_word_entry, text="Remove", command=self.controller.remove_selected_word, width=30,
                                        height=3, state=tkinter.DISABLED)
        self.bt_remove.grid(column=0, row=3, pady=10, padx=10)

        frm_word_list = LabelFrame(frm_word, height=70, text="Available translations")
        #Scroll
        words_scroll_bar = Scrollbar(frm_word_list, orient=VERTICAL)
        self.list_words = tkinter.Listbox(frm_word_list, width=40, height=30, yscrollcommand=words_scroll_bar)
        words_scroll_bar.config(command=self.list_words.yview)
        words_scroll_bar.pack(side=RIGHT, fill=Y)
        self.list_words.pack(padx=8, pady=10)
        frm_word_list.grid(column=1, row=0, padx=8, pady=10)

        self.list_words.bind("<<ListboxSelect>>", self.controller.word_selection)

        # Translation
        frm_translation = tkinter.LabelFrame(self.root, text="Translation")
        frm_translation.grid(column=1, row=1, pady=5, padx=10)
        frm_translation_entry = LabelFrame(frm_translation, height=70, text="Word's translations")
        frm_translation_entry.grid(column=0, row=0, padx=8, pady=10)

        self.combo_translation = tkinter.ttk.Combobox(frm_translation_entry, width=30, )
        # Translation combobox events binding
        self.combo_translation.bind("<Key>", self.controller.translation_key_stroke)

        self.combo_translation.grid(column=0, row=0, pady=10, padx=10)
        bt_add_translation = tkinter.Button(frm_translation_entry, text="Add", command=self.controller.add_new_translation,
                                            width=30, height=2)
        bt_add_translation.grid(column=0, row=1, pady=10, padx=10)
        bt_add_translation = tkinter.Button(frm_translation_entry, text="Remove",
                                            command=self.controller.remove_selected_translation,
                                            width=30, height=2)
        bt_add_translation.grid(column=0, row=2, pady=10, padx=10)

        self.bt_link_translation = tkinter.Button(frm_translation_entry, text="<<<<<<",
                                            command=self.controller.link_translation,
                                            width=30, height=1, state=tkinter.DISABLED)
        self.bt_link_translation.grid(column=0, row=3, pady=10, padx=10)

        self.list_translations = tkinter.Listbox(frm_translation_entry, width=40, height=20)
        self.list_translations.grid(column=0, row=4, pady=5, padx=10)

        self.bt_unlink_translation = tkinter.Button(frm_translation_entry, text=">>>>>>",
                                            command=self.controller.unlink_translation,
                                            width=30, height=1, state=tkinter.DISABLED)
        self.bt_unlink_translation.grid(column=0, row=5, pady=5, padx=10)

        frm_translation_list = LabelFrame(frm_translation, height=70, text="Available translations")
        translation_scroll_bar = Scrollbar(frm_translation_list, orient=VERTICAL)
        self.list_all_translations = tkinter.Listbox(frm_translation_list, width=40, height=30,yscrollcommand=translation_scroll_bar)
        translation_scroll_bar.config(command=self.list_all_translations.yview)
        translation_scroll_bar.pack(side=RIGHT, fill=Y)
        self.list_all_translations.pack(padx=8, pady=10)
        frm_translation_list.grid(column=1, row=0, padx=8, pady=10)

        self.list_all_translations.bind("<<ListboxSelect>>", self.controller.all_translations_selection)
        self.list_translations.bind("<<ListboxSelect>>", self.controller.current_translations_selection)

    def onSelection(self, word_selected: bool, tr_selected: bool):
        if word_selected:
            self.bt_link_translation['state'] = tkinter.NORMAL
            self.bt_unlink_translation['state'] = tkinter.NORMAL
            self.bt_update['state'] = tkinter.NORMAL
            self.bt_remove['state'] = tkinter.NORMAL
        else:
            self.bt_link_translation['state'] = tkinter.DISABLED
            self.bt_unlink_translation['state'] = tkinter.DISABLED
            self.bt_update['state'] = tkinter.DISABLED
            self.bt_remove['state'] = tkinter.DISABLED

# *******************
# --- CONTROLLER ---
# *******************



class FillerController:
    ID_POS = 0
    WORD_POS = 1
    WORD_TYPE_POS = 2
    db_connection = []
    gui = []
    word_rows = []
    translation_rows = []
    current_translation_rows = []  # Translations for the current word
    current_word_index = -1;
    current_word = ""
    current_all_translations_index = -1;
    current_all_translations = ""
    current_word_translations_index = -1;
    current_word_translations = ""


    def __init__(self, db_connection):
        self.last_added_translation = None
        self.db_connection = db_connection

    def set_gui(self, gui) -> None:
        self.gui = gui

    # --->>> Words - Words - Words <<<---
    def fill_words(self) -> None:
        for word_row in self.word_rows:
            print(word_row)
            self.gui.list_words.insert(END, word_row[1])

    def populate_words(self, like_word="") -> None:
        self.word_rows = self.get_all_words(like_word)
        self.fill_words()

    def clear_words(self) -> None:
        self.gui.list_words.delete(0, END)

    def word_selection(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            new_index = selection[0]
            self.current_word_index = new_index
            type_word = self.word_rows[self.current_word_index][2]
            word = self.word_rows[self.current_word_index][1]
            self.current_word = word
            self.gui.set_word_type(type_word)
            self.gui.combo_word.set(word)
            self.gui.onSelection(True, self.current_all_translations_index > -1)
            print("Selection=", self.current_word_index, " type_word=", type_word)
            # Translations
            self.clear_current_translations()
            self.populate_current_translations()
        else:
            print("No Selection")


    def update_word(self) -> None:
        if self.current_word_index < 0:
            return
        wrd = self.gui.combo_word.get()
        new_word = wrd.strip()
        if new_word == "":
            return
        new_word_type = self.gui.get_word_type()
        print(new_word, new_word_type)
        unique_id = self.word_rows[self.current_word_index][0]
        print("updating: '" + new_word + "', type:" + str(new_word_type) + ", unique_id:" + str(unique_id))
        self.db_connection.update_word(new_word, new_word_type, unique_id)
        self.clear_words()
        self.populate_words()
        self.gui.list_words.select_set(self.current_word_index)

    def add_word(self) -> None:
        wrd = self.gui.combo_word.get()
        new_word = wrd.strip()
        print("new_word='" + new_word + "'")
        if new_word == "":
            return
        new_word_type = self.gui.get_word_type()
        if not self.db_connection.is_word_present(new_word, new_word_type):
            print(new_word, new_word_type)
            self.db_connection.insert_new_word(new_word, new_word_type)
            self.clear_words()
            self.populate_words()
        else:
            messagebox.showerror("Insertion error",
                                 "Word '" + new_word + "' with type '" + str(new_word_type) + "' already exists")

    def get_current_word(self):
        return self.current_word

    def remove_word(self, word_id) -> None:
        self.db_connection.remove_word_by_id(word_id)
        self.clear_words()
        self.populate_words()
        self.current_word_index = -1
        self.current_word = ""
        self.gui.set_word_type(1)
        self.gui.combo_word.set("")
        self.gui.onSelection(False, self.current_all_translations_index > -1)

    def remove_selected_word(self) -> None :
        if self.current_word_index > 0:
            word = self.get_current_word()
            word_id = self.word_rows[self.current_word_index][0]
        res = messagebox.askquestion('Removing a word', 'Do you really want to remove "' + word + '"?')
        if res == 'yes':
            self.remove_word(word_id)

    def clear_all_words(self) -> None:
        self.gui.list_words.delete(0, END)


    # --->>> Translations - Translations - Translations <<<---


    def fill_all_translations(self) -> None:
        idx = 0
        last_added_idx = -1
        for translation_row in self.translation_rows:
            #print("All: " + translation_row)
            if self.last_added_translation != "" and self.last_added_translation == translation_row[1]:
                last_added_idx = idx
                print("Last_added_translation Found: " + self.last_added_translation + " @" + str(idx))
            self.gui.list_all_translations.insert(END, translation_row[1])
            idx += 1
        if last_added_idx >= 0:
            self.current_all_translations = self.last_added_translation
            self.current_all_translations_index = last_added_idx
            self.gui.list_all_translations.select_set(last_added_idx)

    def fill_current_translations(self) -> None:
        for translation_row in self.current_translation_rows:
            #print("Current: " + translation_row)
            self.gui.list_translations.insert(END, translation_row[1])

    def populate_all_translations(self, tr_like="") -> None:
        if tr_like == "":
            self.translation_rows = self.get_all_translations()
        else:
            self.translation_rows = self.get_like_translations(tr_like)
        self.fill_all_translations()

    def clear_all_translations(self) -> None:
        self.gui.list_all_translations.delete(0, END)

    def clear_current_translations(self) -> None:
        self.gui.list_translations.delete(0, END)

    def add_new_translation(self) -> None:
        translation = self.gui.combo_translation.get()
        new_translation = translation.strip()
        print("new_translation='" + new_translation + "'")
        if new_translation == "":
            return
        if not self.db_connection.is_translation_present(new_translation):
            print(new_translation)
            self.db_connection.insert_new_translation(new_translation)
            self.clear_all_translations()
            self.last_added_translation = new_translation;  # Will point to this
            self.populate_all_translations()
        else:
            messagebox.showerror("Insertion error", "Translation '" + new_translation + "' already exists")

    def remove_selected_translation(self):
        if self.current_all_translations_index > 0:
            tr = self.get_current_all_translation()
            tr_id = self.translation_rows[self.current_all_translations_index][0]
            res = messagebox.askquestion('Removing a translation', 'Do you really want to remove "' + tr + '" ?')
            if res == 'yes':
                self.remove_translation(tr_id)
                self.current_all_translations_index = -1
                self.current_all_translations = ""
                self.gui.onSelection(self.current_word_index > -1, False)


    def remove_translation(self, tr_id : int) -> None:
        self.db_connection.remove_translation(tr_id)
        self.clear_all_translations()
        self.populate_all_translations()

    def word_key_stroke(self, event):
        print("Word Brutto event:", event)
        if event.char != '':
            print(event, event.char, ord(event.char))
            if ord(event.char) > 32:
                new_word = self.gui.get_current_word_value() + event.char
                print("new_word:", new_word)
                if len(new_word) > 1:
                    word_entries = self.db_connection.get_words(new_word, like=True, limit=10)
                    words = []
                    for entry in word_entries:
                        words.append(entry[1])
                    if len(words) > 0:
                        self.gui.set_word_choices(words)
                    print("Words: ", words)
            elif event.char == '\r':
                like_word = self.gui.get_current_word_value()
                self.clear_all_words()
                self.populate_words(like_word)


    def translation_key_stroke(self, event):
        print("Translation Brutto event:", event)
        if event.char != '':
            print(event, event.char, ord(event.char))
            if ord(event.char) > 32:
                new_translation = self.gui.get_current_translation_value() + event.char
                print("new_translation:", new_translation)
                if len(new_translation) > 1:
                    translation_entries = self.db_connection.get_translations(new_translation, like=True, limit=10)
                    translations = []
                    for entry in translation_entries:
                        translations.append(entry[1])
                    if len(translations) > 0:
                        self.gui.set_translation_choices(translations)
                    print(translations)
            elif event.char == '\r':
                like_translation = self.gui.get_current_translation_value()
                self.clear_all_translations()
                self.populate_all_translations(like_translation)

    def all_translations_selection(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            self.current_all_translations_index = selection[0]
            word = self.translation_rows[self.current_all_translations_index][1]
            self.gui.set_translation(word)
            self.current_all_translations = word
            self.gui.onSelection(self.current_word_index > -1, True)
            print("All Translation Selection=", self.current_all_translations_index, " translation=", word)
        else:
            print("All Translation No Selection")

    def current_translations_selection(self, event) -> None:
        selection = event.widget.curselection()
        if selection:
            self.current_word_translations_index = selection[0]
            print("Current Translation Selection=", self.current_word_translations_index)
            word = self.current_translation_rows[self.current_word_translations_index][1]
            self.current_word_translations = word
        else:
            print("Current Translation No Selection")


    def get_current_all_translation(self):
        return self.current_all_translations

    def get_all_words(self, like_word="") -> []:
        if like_word == "":
            rows = self.db_connection.get_words()
        else:
            rows = self.db_connection.get_words(like_word, True)
        return rows

    def get_all_translations(self) -> []:
        rows = self.db_connection.get_translations()
        return rows

    def get_like_translations(self, tr_like : str) -> []:
        rows = self.db_connection.get_translations(tr_like, True)
        return rows


    def populate_current_translations(self) -> None:
        if self.current_word_index >= 0:
            word_id = self.word_rows[self.current_word_index][0]
            self.current_translation_rows = self.db_connection.get_translations_4word(word_id)
            self.fill_current_translations()

    def clear_current_translations(self) -> None:
        self.gui.list_translations.delete(0, END)


    # adding new translation
    def link_translation(self) -> None:
        if (self.current_all_translations_index >= 0) and (self.current_word_index >= 0) :
            word_id = self.word_rows[self.current_word_index][0];
            word = self.word_rows[self.current_word_index][1];
            tr_id, tr = self.translation_rows[self.current_all_translations_index]
            if not self.db_connection.is_link_present(word_id, tr_id):
                print(tr + ":" + str(tr_id) + " is linked to " + word + "@" + str(word_id))
                self.gui.add_current_translation(tr)
                self.db_connection.add_link(word_id, tr_id)
                self.current_translation_rows.append(tr)

    def unlink_translation(self):
        if (self.current_word_translations_index >= 0) and (self.current_word_index >= 0) :
            self.db_connection.remove_link(self.word_rows[self.current_word_index][0],
                                           self.current_translation_rows[self.current_word_translations_index][0])
        self.clear_current_translations()
        self.populate_current_translations()

def run_filler(db_conx) -> None:
    controller = FillerController(db_conx)
    gui = FillerGui(controller)
    controller.set_gui(gui)
    controller.populate_words()
    controller.populate_all_translations()
    gui.getRoot().mainloop()
