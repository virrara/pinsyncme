
########### Necessary Modul ###########
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage
from funct import get_user_id_from_database, insert_user, load_icon
from tkinter import messagebox
########### END of Necessary Modul ###########

########### Path to Asset ###########
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
########### END of Path to Asset ###########

class AddProfile:
    def __init__(self, parent, tree, update_treeview):  
        self.parent = parent
        self.tree = tree
        self.update_treeview = update_treeview
        self.parent.title("Add Profile")
        icon = load_icon("icon.png")
        self.parent.iconphoto(True, icon)
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))

        ########### GUI ###########
        canvas = Canvas(
            parent,
            bg = "#C5B3BB",
            height = 358,
            width = 329,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # start of bcg
        canvas.place(x = 0, y = 0)
        self.image_bcg = PhotoImage(
            file=relative_to_assets("bcg.png"))
        self.bcg = canvas.create_image(
            164.0,
            178.0,
            image=self.image_bcg
        )
        # start of bcg

        # end of the entry_password
        self.entry_pw_bg = PhotoImage(
            file=relative_to_assets("entry_password.png"))
        self.entry_bg_2 = canvas.create_image(
            164.0,
            143.5,
            image=self.entry_pw_bg
        )
        self.entry_email = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_email.place(
            x=55.5,
            y=128.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_password

        # start of the entry_email
        self.entry_bcg = PhotoImage(
            file=relative_to_assets("entry_email.png"))
        self.entry_bg_1 = canvas.create_image(
            164.0,
            225.5,
            image=self.entry_bcg
        )
        self.entry_password = Entry(
            parent,  
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_password.place(
            x=55.5,
            y=210.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_email
        # start of the email
        self.image_email = PhotoImage(
            file=relative_to_assets("email.png"))
        self.email = canvas.create_image(
            69.0,
            100.0,
            image=self.image_email
        )
        # end of the email

        # start of the add_profile
        self.image_add_profile = PhotoImage(
            file=relative_to_assets("add_profile.png"))
        self.label_add_profile = canvas.create_image(
            164.0,
            51.0,
            image=self.image_add_profile
        )
        # end of the add_profile

        # start of the password
        self.image_password = PhotoImage(
            file=relative_to_assets("password.png"))
        self.password = canvas.create_image(
            88.0,
            183.0,
            image=self.image_password
        )
        # end of the password

        # start of the button_add_profile
        self.button_bcg = PhotoImage(
            file=relative_to_assets("button_add_profile.png"))
        self.button_add_profile = Button(
            parent,
            image=self.button_bcg,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_profile,
            relief="flat"
        )
        self.button_add_profile.place(
            x=96.0,
            y=273.0,
            width=137.0,
            height=43.0
        )
        window_width = 329
        window_height = 358
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        parent.resizable(False, False)
        parent.mainloop()
    ########### END of GUI ###########
    
    ########### Function Add Profile ###########
    def show_message(self, *args, **kwargs):
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))
        messagebox.showwarning(*args, **kwargs)
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))

    def add_profile(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            self.show_message("Error", "Please enter both email and password.")
            return
        
        if "@" not in email or "." not in email:
            self.show_message("Error", "Please enter a valid email address.")
            return
        
        user_id = get_user_id_from_database(email)
        if user_id is not None:
            self.show_message("Error", "Email already exists in the database.")
            return

        insert_user(email, password)
        self.parent.after(100, self.update_treeview)

        # Show the success message with the AddProfile window still on top
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))
        messagebox.showinfo("Success", "Profile added successfully!")

        # Destroy the AddProfile window
        self.parent.destroy()
    ########### END of Function Add Profile ###########
