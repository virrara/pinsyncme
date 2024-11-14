
from colorama import init, Fore, Style
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from funct import *
import webbrowser
import os
from pathlib import Path
from tkinter import *
from funct import *
import tkinter as tk
import tkinter.font as tkfont
########### Path to Asset ###########
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame1")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
########### END of Path to Asset ###########

########### Choose Account ###########
class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self.position = 0
        self['values'] = self._completion_list
        self.var = self["textvariable"]
        if self.var == "":
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace("w", self.handle_keyrelease)

    def autocomplete(self):
        self.position = len(self.get())
        _hits = [item for item in self._completion_list if item.lower().startswith(self.get().lower())]

        if not self.get() or not _hits:
            self._hits = []
            self['values'] = self._completion_list
        else:
            self._hits = _hits
            self['values'] = self._hits

        # Automatically open the dropdown when there are matching results
        if _hits:
            self.event_generate('<Down>')
            self.selection_range(self.position, tk.END)

    def handle_keyrelease(self, *args):
        self.autocomplete()

# Function to fetch accounts from SQLite database

def get_accounts():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users")
    accounts = [row[0] for row in cursor.fetchall()]
    conn.close()
    return accounts

# Function to retrieve email and password based on selected email
def get_email_and_password(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, password FROM users WHERE email=?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row  # Returns a tuple (email, password) or None if not found

selected_email = None
selected_password = None

# Create a dictionary to store the PhotoImage objects
images = {}

def open_change_account_window(window, result_label):
    change_account_window = tk.Toplevel(window)
    change_account_window.geometry("329x208")
    change_account_window.configure(bg="#C5B3BB")
    change_account_window.title("Choose Account")
    icon = load_icon("icon.png")
    change_account_window.iconphoto(True,icon)
    change_account_window.attributes("-topmost", not change_account_window.attributes("-topmost"))
    window_width = 329
    window_height = 208
    screen_width = change_account_window.winfo_screenwidth()
    screen_height = change_account_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    change_account_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    change_account_window.resizable(False, False)


    canvas = Canvas(
        change_account_window,
        bg="#C5B3BB",
        height = 208,
        width = 329,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x=0, y=0)

    # start of the bcg
    images["image_bcg"] = PhotoImage(
        file=relative_to_assets("bcg.png"))
    bcg = canvas.create_image(
        164.0,
        103.0,
        image=images["image_bcg"]
    )
    # end of the bcg

    # start of the choose_account
    images["image_choose_account"] = PhotoImage(
        file=relative_to_assets("choose_account.png"))
    choose_account = canvas.create_image(
        163.0,
        66.0,
        image=images["image_choose_account"]
    )
    # end of the choose_account

    canvas.create_rectangle(
        60.0,
        107.0,
        270.0,
        140.0,
        fill="#C5B3BB",
        outline="")


    custom_width = '29'
    all_accounts = get_accounts()
    account_combobox = AutocompleteCombobox(change_account_window, width=custom_width)
    account_combobox.set_completion_list(all_accounts)
    account_combobox.place(x=67, y=113)

    def on_account_selected(event):
        global selected_email, selected_password

        selected_account = account_combobox.get()
        if selected_account:
            email_and_password = get_email_and_password(selected_account)
            if email_and_password:
                selected_email, selected_password = email_and_password
                result_label.config(text=f"Hi! {selected_email}")
                custom_font = tkfont.Font(family="Poppins", weight="bold", size=8)
                result_label.config(font=custom_font)
                # Calculate the center of the window horizontally
                window_x_offset = 78
                window_width = 155
                center_x = window_x_offset + (window_width - result_label.winfo_reqwidth()) // 2

                result_label.place(x=center_x, y=168)
                change_account_window.destroy()
            else:
                result_label.config(text="Invalid account!")
        else:
            result_label.config(text="Choose Account")

    account_combobox.bind("<<ComboboxSelected>>", on_account_selected)
########### END of Choose Account ###########
def get_selected_email_and_password():
    return selected_email, selected_password

