########### Modul ###########
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sqlite3
from funct import load_icon
########### END of Modul ###########

########### Path to Asset ###########
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame2")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
########### END of Path to Asset ###########

class EditProfile:
    def __init__(self, parent, user_id, email, password, note1, note2, note3, tree):
        self.parent = parent
        self.user_id = user_id
        self.email = email
        self.password = password
        self.note1 = note1
        self.note2 = note2
        self.note3 = note3
        self.tree = tree
        self.parent.title("Edit Profile")
        icon = load_icon("icon.png")
        self.parent.iconphoto(True,icon)
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))

        canvas = Canvas(
            parent,
            bg = "#C5B3BB",
            height = 358,
            width = 640,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # start of the bcg
        canvas.place(x = 0, y = 0)
        self.image_bcg = PhotoImage(
            file=relative_to_assets("bcg.png"))
        self.bcg = canvas.create_image(
            320.0,
            179.0,
            image=self.image_bcg
        )
        # end of the bcg
        # start of the email
        self.email_image = PhotoImage(
            file=relative_to_assets("entry_email.png"))
        self.entry_bg_5 = canvas.create_image(
            180.0,
            133.5,
            image=self.email_image
        )
        self.entry_email = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_email.place(
            x=71.5,
            y=116.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_email
        self.entry_email.insert(0, email)
        # start of the email
        self.image_email = PhotoImage(
            file=relative_to_assets("email.png"))
        self.email = canvas.create_image(
            85.0,
            92.0,
            image=self.image_email
        )
        # end of the email
        # start of the entry_password
        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_password.png"))
        self.entry_bg_4 = canvas.create_image(
            460.0,
            133.5,
            image=self.entry_image_4
        )
        self.entry_password = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_password.place(
            x=351.5,
            y=116.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_password
        self.entry_password.insert(0, password)
        # start of the password
        self.image_password = PhotoImage(
            file=relative_to_assets("password.png"))
        self.password = canvas.create_image(
            384.0,
            92.0,
            image=self.image_password
        )
        # end of the password

        # start of the entry_note1
        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_note1.png"))
        self.entry_bg_3 = canvas.create_image(
            180.0,
            215.5,
            image=self.entry_image_3
        )
        self.entry_note1 = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_note1.place(
            x=71.5,
            y=198.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_note1
        # start of the note1
        self.image_note1 = PhotoImage(
            file=relative_to_assets("note1.png"))
        self.note1_image = canvas.create_image(
            87.0,
            176.0,
            image=self.image_note1
        )
        # end of the note1
        if note1 is not None:
            self.entry_note1.insert(0, note1)
        else:
            self.entry_note1.insert(0, "")  
        # start of the entry_note2
        self.entry_bcg = PhotoImage(
            file=relative_to_assets("entry_note2.png"))
        self.entry_bg_1 = canvas.create_image(
            464.0,
            215.5,
            image=self.entry_bcg
        )
        self.entry_note2 = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_note2.place(
            x=355.5,
            y=198.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_note2
        # start of the note2
        self.image_note2 = PhotoImage(
            file=relative_to_assets("note2.png"))
        self.note2_image = canvas.create_image(
            368.0,
            174.0,
            image=self.image_note2
        )
        # end of the note2
        if note2 is not None:
            self.entry_note2.insert(0, note2)
        else:
            self.entry_note2.insert(0, "")  
        # start of the entry_note3
        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_note3.png"))
        self.entry_bg_2 = canvas.create_image(
            180.0,
            297.5,
            image=self.entry_image_2
        )
        self.entry_note3 = Entry(
            parent,
            bd=0,
            bg="#C5B3BB",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_note3.place(
            x=71.5,
            y=280.0,
            width=217.0,
            height=33.0
        )
        # end of the entry_note3

        # start of the note3
        self.image_note3 = PhotoImage(
            file=relative_to_assets("note3.png"))
        self.note3_image = canvas.create_image(
            90.0,
            258.0,
            image=self.image_note3
        )
        if note3 is not None:
            self.entry_note3.insert(0, note3)
        else:
            self.entry_note3.insert(0, "")  
        # end of the note3

        # start of the button_discard
        self.button_bcg = PhotoImage(
            file=relative_to_assets("button_discard.png"))
        self.button_discard = Button(
            parent,
            image=self.button_bcg,
            borderwidth=0,
            highlightthickness=0,
            command=self.discard_changes,
            relief="flat"
        )
        self.button_discard.place(
            x=492.336181640625,
            y=280.0,
            width=93.66372680664062,
            height=41.0
        )
        # end of the button_discard

        # start of the button_update
        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_update.png"))
        self.button_update = Button(
            parent,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_changes,
            relief="flat"
        )
        self.button_update.place(
            x=390.0,
            y=280.0,
            width=93.66372680664062,
            height=41.0
        )
        # end of the button_update

        # start of the edit_profile
        self.image_edit_profile = PhotoImage(
            file=relative_to_assets("edit_profile.png"))
        self.edit_profile = canvas.create_image(
            320.0,
            40.0,
            image=self.image_edit_profile 
        )
        
        # end of the edit_profile
        window_width = 640
        window_height = 358
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        parent.geometry(f"{window_width}x{window_height}+{x}+{y}")
        parent.resizable(False, False)
        parent.mainloop() 
    ########### Function Save Changes ###########
        ########### Function Add Profile ###########
    def show_message(self, *args, **kwargs):
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))
        messagebox.showwarning(*args, **kwargs)
        self.parent.attributes("-topmost", not self.parent.attributes("-topmost"))
    def save_changes(self):
        new_email = self.entry_email.get()
        new_password = self.entry_password.get()
        new_note1 = self.entry_note1.get()
        new_note2 = self.entry_note2.get()
        new_note3 = self.entry_note3.get()
        if "@" not in new_email or "." not in new_email:
            self.show_message("Error", "Please enter a valid email address.")
            return
        # Update the user's data in the database
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET Email=?, Password=?, note1=?, note2=?, note3=? WHERE ID=?",
                    (new_email, new_password, new_note1, new_note2, new_note3, self.user_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Find the item in the Treeview and update its values
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values[0] == str(self.user_id):
                self.tree.item(item, values=(values[0], new_email, '*' * len(new_password), new_note1, new_note2, new_note3))
                break

        # Close the EditProfile window after saving changes
        self.parent.destroy()
        messagebox.showinfo("Success", "Edit profile Success.")

    ########### END of Function Save Changes ###########
    ########### Function Discard Changes ###########
    def discard_changes(self):
        # Close the edit window without saving changes
        self.parent.destroy()
    ########### END of Function Discard Changes ###########