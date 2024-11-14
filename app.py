########### Necessary Modul ###########
from colorama import init, Fore, Style
from pathlib import Path
import os
from ttkthemes import ThemedStyle
from pathlib import Path
from tkinter import *
###########> Driver <###########
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import webbrowser
###########> Our Modul <###########
from funct import *
from splash_screen import *
from common_funct import AutocompleteCombobox, get_accounts, get_email_and_password, open_change_account_window
from upload import Upload
from repin import Repin
from user_manager import UserManager
from createacc import CreateAcc
import socket
import requests
from threading import Thread
########### END of Modul ###########

########### Path to Asset ###########
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame6")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
########### END of Path to Asset ###########


########### END ofHandle Button ###########
########### Main GUI ###########
def main():
    ########### Change Account Function ###########
    def open_change_account_window_from_app():
        open_change_account_window(window, result_label)
    ########### END of Change Account Function ###########
    ########### Handle Button ###########
    def handle_button_press(btn_name):
        global current_window
        if btn_name == "createacc":
            createacc_button_clicked()
            current_window = CreateAcc(window)
        elif btn_name == "upload":
            upload_button_clicked()
            current_window = Upload(window)
        elif btn_name=="repin":
            repin_button_clicked()
            current_window = Repin(window)
        elif btn_name=="usermanager":
            usermanager_button_clicked()
            current_window = UserManager(window)
    ###########> Handle Function <###########
    def createacc_button_clicked(): # (coordinates : x= 0 , y= 133)
        canvas.itemconfig(page_navigator)
        sidebar_navigator.place(
            x=44.675048828125,
            y=242.35540771484375,
        )  

    def upload_button_clicked(): # (coordinates : x= 0 , y= 184)
        canvas.itemconfig(page_navigator)
        sidebar_navigator.place(
            x=44.675048828125,
            y=302.2,
        )
    def repin_button_clicked():
        canvas.itemconfig(page_navigator)
        sidebar_navigator.place(
            x=44.675048828125,
            y=362,
        )
    def usermanager_button_clicked():
        canvas.itemconfig(page_navigator)
        sidebar_navigator.place(
            x=44.675048828125,
            y=425.3,
        )
    status = show_splash_screen()
    
    if status:
        window = Tk()
        window.title("PinSyncMe")
        window.geometry("1008x594")
        window.configure(bg = "#C5B3BB")
        icon = load_icon("icon.png")
        window.iconphoto(True,icon)
        secret_key = read_secret_key()
        entry_secretKey = Entry(
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0,
            show=""
        )
        entry_secretKey.insert(0, secret_key)  # Initialize the entry with the read secret key
        entry_secretKey.place(
            x=68.5,
            y=137.0,
            width=431.0,
            height=33.0
        )
        # Start the API key availability check in a separate thread
        api_check_thread = Thread(target=check_api_key_availability, args=(entry_secretKey, window))
        api_check_thread.daemon = True  # The thread will be terminated when the main program exits
        api_check_thread.start()
        canvas = Canvas(
            window,
            bg = "#C5B3BB",
            height = 594,
            width = 1010,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # start of the bcg
        canvas.place(x = 0, y = 0)
        image_bcg = PhotoImage(
            file=relative_to_assets("bcg.png"))
        bcg = canvas.create_image(
            155.0,
            297.0,
            image=image_bcg
        )
        # end of the bcg
        current_window = CreateAcc(window)

        ########### SideBar Button ###########
        # start of the button_upload
        button__image_createacc = PhotoImage(
            file=relative_to_assets("button_createacc.png"))
        button_5 = Button(
            image=button__image_createacc,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_button_press("createacc"),
            relief="flat"
        )
        button_5.place(
            x=45.0,
            y=232.0,
            width=237.0,
            height=63.0
        )
        # end of the button_upload
        # start of the button_repin
        button_icon = PhotoImage(
            file=relative_to_assets("button_upload.png"))
        button_upload = Button(
            image=button_icon,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_button_press("upload"),
            relief="flat"
        )
        button_upload.place(
            x=45.0,
            y=293.0,
            width=237.0,
            height=63.0
        )
        # end of the button_repin
        # start of the button_user_manager
        button_image_4 = PhotoImage(
            file=relative_to_assets("button_repin.png"))
        button_repin = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_button_press("repin"),
            relief="flat"
        )
        button_repin.place(
            x=45.0,
            y=354.0,
            width=237.0,
            height=61.0
        )
        # end of the button_user_manager
        # start of the button_create
        button_line = PhotoImage(
            file=relative_to_assets("button_user_manager.png"))
        button_user_manager = Button(
            image=button_line,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_button_press("usermanager"),
            relief="flat"
        )
        button_user_manager.place(
            x=45.0,
            y=414.0,
            width=237.0,
            height=61.0
        )
        # end of the button_create
        ########### END of SideBar Button ###########
        ####### (i)  SIDEBAR NAVIGATOR #########
        sidebar_navigator = Frame(background="#C5B3BB")
        sidebar_navigator.place(
            x=44.675048828125,
            y=242.35540771484375,
            height=40, 
            width=7,
        ) 
        ########################################
        ####### (ii)  PAGE NAVIGATOR ###########
        page_navigator = canvas.create_text(
            251.0,
            37.0,
            anchor="nw",
            text="",
            fill="#171435",
            font=("Montserrat Bold", 26 * -1))
        ########################################
        ########################################

        ##################### END of Navigators ###############################
        # start of the button_user
        button_bcg = PhotoImage(
            file=relative_to_assets("button_user.png"))
        button_user = Button(
            image=button_bcg,
            borderwidth=0,
            highlightthickness=0,
            command=open_change_account_window_from_app,
            relief="flat"
        )
        button_user.place(
            x=90.0,
            y=126.0,
            width=130.0762939453125,
            height=37.63066101074219
        )
        # end of the button_user

        # start of the icon
        image_icon = PhotoImage(
            file=relative_to_assets("icon.png"))
        icon = canvas.create_image(
            153.7662353515625,
            90.0,
            image=image_icon
        )
        # end of the icon

        result_label = tk.Label(
            window, 
            text="", 
            anchor="n", 
            fg="#727272", 
            font=("Poppins Bold", 9 * -1))
        result_label.place(x=58, y=155)

        # start of the line
        image_line = PhotoImage(
            file=relative_to_assets("line.png"))
        line = canvas.create_image(
            153.96392822265625,
            220.03135681152344,
            image=image_line
        )
        # end of the line

        button_image_logout = PhotoImage(
            file=relative_to_assets("logout.png"))
        button_logout = Button(
            image=button_image_logout,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: logout_user(window),
            relief="flat"
        )
        button_logout.place(
            x=108.0,
            y=494.0,
            width=93.0,
            height=38.0
        )

        # Set the window dimensions
        window_width = 1008
        window_height = 594
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.resizable(False, False)
        window.mainloop()
    else:
        messagebox.showerror("Warning!","License check failed. The app cannot be displayed.")
        sys.exit(1)