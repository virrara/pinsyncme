########### Necessary Modul ###########
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from funct import *
from funct import delete_user
from common_funct import *
from add_profile import AddProfile
from edit_profile import EditProfile
from tkinter import Scrollbar
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import csv
import sqlite3
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
########### END of Necessary Modul ###########

########### Path to Asset ###########
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame5")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
########### END of Path to Asset ###########

########### Function GUI ###########
def create_user_manager_gui(canvas):
    root = canvas.winfo_toplevel()
    style = ThemedStyle(root)
    style.set_theme("arc")  

    tree_frame = tk.Frame(canvas, bg="#C5B3BB")
    tree_frame.place(x=68.5, y=230, width=587, height=289) 

    tree = ttk.Treeview(tree_frame, columns=("ID", "Email", "Password", "Note1", "Note2", "Note3"), show="headings")
    tree.heading("ID", text="ID", command=lambda: sort_column(tree, "ID", False))
    tree.heading("Email", text="Email", command=lambda: sort_column(tree, "Email", False))
    tree.heading("Password", text="Password")
    tree.heading("Note1", text="Note 1", command=lambda: sort_column(tree, "Note1", False))
    tree.heading("Note2", text="Note 2", command=lambda: sort_column(tree, "Note2", False))
    tree.heading("Note3", text="Note 3", command=lambda: sort_column(tree, "Note3", False))

    tree.column("ID", width=30, anchor=tk.CENTER)
    tree.column("Email", width=150, anchor=tk.CENTER)
    tree.column("Password", width=70, anchor=tk.CENTER)
    tree.column("Note1", width=100, anchor=tk.CENTER)
    tree.column("Note2", width=100, anchor=tk.CENTER)
    tree.column("Note3", width=100, anchor=tk.CENTER)

    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)

        for index, (value, child) in enumerate(data):
            tree.move(child, "", index)
        
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))
    
    def on_edit_button_click():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            EditProfile(root, user_id, tree)
            update_treeview()

    def update_treeview():
        try:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            tree.delete(*tree.get_children())
            for user in users:
                user_id = str(user[0])
                email = user[1]
                password = '*' * len(user[2])
                note1 = user[3]
                note2 = user[4]
                note3 = user[5]

                note1 = note1 if note1 is not None else " "
                note2 = note2 if note2 is not None else " "
                note3 = note3 if note3 is not None else " "

                tree.insert("", "end", values=(user_id, email, password, note1, note2, note3))

            cursor.close()
            connection.close()

        except Exception as e:
            print("Error:", e)

    def open_edit_profile_window():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            edit_profile_window = tk.Toplevel(root)
            edit_profile_window.title("Edit Profile")
            edit_profile_window.geometry("640x358")

            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()
            cursor.execute("SELECT Email, Password, note1, note2, note3 FROM users WHERE ID=?", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            connection.close()

            if user_data:
                email = user_data[0]
                password = user_data[1]
                note1 = user_data[2]
                note2 = user_data[3]
                note3 = user_data[4]

                EditProfile(edit_profile_window, user_id, email, password, note1, note2, note3, tree)
            else:
                success_msg = f"User with ID {user_id} not found."
                messagebox.showerror("Error", success_msg)

            update_treeview()

    def delete_selected_user():
        selected_item = tree.selection()
        if selected_item:
            user_id = tree.item(selected_item, "values")[0]
            response = messagebox.askyesno("Confirm Deletion", f"Do you want to delete user with ID {user_id}?")
            if response:
                delete_user(user_id)
                tree.delete(selected_item)
                update_treeview()

    def search_users(event=None):
        query = entry_search.get()
        if not query: 
            query = "%"  
        tree.delete(*tree.get_children()) 

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE ID LIKE ? OR Email LIKE ? OR note1 LIKE ? OR note2 LIKE ? OR note3 LIKE ?",
                    (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
        users = cursor.fetchall()

        for user in users:
            user_id = str(user[0])
            email = user[1]
            password = '*' * len(user[2])
            note1 = user[3] if user[3] is not None else " "
            note2 = user[4] if user[4] is not None else " "
            note3 = user[5] if user[5] is not None else " "

            tree.insert("", "end", values=(user_id, email, password, note1, note2, note3))

        cursor.close()
        connection.close()

    def open_add_profile_window():
        add_profile_window = Toplevel()
        add_profile_window.geometry("329x358")
        add_profile_window.configure(bg="#C5B3BB")
        AddProfile(add_profile_window, tree, update_treeview) 

    def import_from_csv():
        file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        import_success_count = 0
        duplicate_count = 0

        try:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            with open(file_path, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)

                headings_skipped = False

                for row in reader:
                    if not headings_skipped:
                        headings_skipped = True
                        continue

                    if len(row) >= 2:
                        email = row[0]
                        password = row[1]
                        note1 = row[2] if len(row) >= 3 else None
                        note2 = row[3] if len(row) >= 4 else None
                        note3 = row[4] if len(row) >= 5 else None

                        cursor.execute("SELECT COUNT(*) FROM users WHERE Email=?", (email,))
                        result = cursor.fetchone()

                        if result[0] == 0:  
                            cursor.execute("INSERT INTO users (Email, Password, note1, note2, note3) VALUES (?, ?, ?, ?, ?)",
                                        (email, password, note1, note2, note3))
                            import_success_count += 1
                        else:
                            duplicate_count += 1

            connection.commit()
            cursor.close()
            connection.close()
            update_treeview()  

            messagebox.showinfo("Import Successful",
                                f"Data imported successfully!\nImported: {import_success_count} accounts.\nDuplicates found: {duplicate_count} accounts.")

        except Exception as e:
            messagebox.showerror("Error", f"Error importing data from CSV: {e}")

    def export_to_csv():
        file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            cursor.execute("SELECT Email, Password, note1, note2, note3 FROM users")
            users = cursor.fetchall()

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(["Email", "Password", "Note1", "Note2", "Note3"])

                for user in users:
                    writer.writerow(user)

            cursor.close()
            connection.close()

            messagebox.showinfo("Export Successful", "Data exported successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error exporting data to CSV: {e}")

    # start of the entry_search
    global entry_image_1
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_search.png"))
    global entry_bg_1
    entry_bg_1 = canvas.create_image(
        296.0,
        181,
        image=entry_image_1
    )
    global entry_search
    entry_search = Entry(
        bd=0,
        bg="#F3F3F3",
        fg="#000716",
        highlightthickness=0
    )
    entry_search.bind("<KeyRelease>", search_users)
    entry_search.place(
        x=388.5,
        y=161.0,
        width=255.0,
        height=39.0
    )
    # end of the entry_search

    # start of the button_add_profile
    global button_bcg_white
    button_bcg_white = PhotoImage(
        file=relative_to_assets("button_add_profile.png"))
    global button_add_profile
    button_add_profile = Button(
        image=button_bcg_white,
        borderwidth=0,
        highlightthickness=0,
        command=open_add_profile_window,
        relief="flat"
    )
    button_add_profile.place(
        x=783.0,
        y=58.0,
        width=171.0,
        height=47.0
    )
    # end of the button_add_profile

    # start of the search
    global image_search
    image_search = PhotoImage(
        file=relative_to_assets("search.png"))
    global search
    search = canvas.create_image(
        419.0,
        181.0,
        image=image_search
    )
    # end of the search

    # start of the button_edit
    global button_bcg_pink
    button_bcg_pink = PhotoImage(
    file=relative_to_assets("button_edit.png"))
    global button_edit
    button_edit = Button(
        image=button_bcg_pink,
        borderwidth=0,
        highlightthickness=0,
        command=open_edit_profile_window,
        relief="flat"
    )
    button_edit.place(
        x=845.0,
        y=169.0,
        width=27.0,
        height=28.0
    )
    # end of the button_edit

    # start of the button_sampah
    global button_bcg_sampah
    button_bcg_sampah = PhotoImage(
        file=relative_to_assets("button_sampah.png"))
    global button_sampah
    button_sampah = Button(
        image=button_bcg_sampah,
        borderwidth=0,
        highlightthickness=0,
        command=delete_selected_user,
        relief="flat"
    )
    button_sampah.place(
        x=895,
        y=168.0,
        width=25.0,
        height=29.0
    )

        #import
    global button_image_import
    button_image_import = PhotoImage(
        file=relative_to_assets("button_4.png"))
    global button_import
    button_import = Button(
        image=button_image_import,
        borderwidth=0,
        highlightthickness=0,
        command=import_from_csv,
        relief="flat"
    )
    button_import.place(
        x=747.0,
        y=168.0,
        width=28.0,
        height=29.0
    )

    #export
    global button_image_export
    button_image_export = PhotoImage(
        file=relative_to_assets("button_5.png"))
    global button_export
    button_export = Button(
        image=button_image_export,
        borderwidth=0,
        highlightthickness=0,
        command=export_to_csv,
        relief="flat"
    )
    button_export.place(
        x=796.0,
        y=167.0,
        width=28.0,
        height=30.0
    )
        
    update_treeview()

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar for the Treeview
    scrollbar = Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.config(yscrollcommand=scrollbar.set)
    return tree

def UserManager(parent):
    canvas = Canvas(
        parent,
        bg = "#C5B3BB",
        height = 594,
        width = 730,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    #tree = create_user_manager_gui(canvas)
    # start of the bcg_white
    canvas.place(x = 285, y = 0)
    global image_bcg_white
    image_bcg_white = PhotoImage(
        file=relative_to_assets("bcg_white.png"))
    global bcg_white
    bcg_white = canvas.create_image(
        363.0,
        301.0,
        image=image_bcg_white
    )
    # end of the bcg_white

    # start of the bcg_pink
    global image_bcg_pink
    image_bcg_pink = PhotoImage(
        file=relative_to_assets("bcg_pink.png"))
    global bcg_pink
    bcg_pink = canvas.create_image(
        362.0,
        338.0,
        image=image_bcg_pink
    )
    # end of the bcg_pink

    # start of the bcg_sampah
    global image_bcg_sampah
    image_bcg_sampah = PhotoImage(
        file=relative_to_assets("bcg_sampah.png"))
    global bcg_sampah
    bcg_sampah = canvas.create_image(
        573.0,
        182.0,
        image=image_bcg_sampah
    )
    # end of the bcg_sampah

    # start of the bcg_edit
    global image_bcg_edit
    image_bcg_edit = PhotoImage(
        file=relative_to_assets("bcg_edit.png"))
    global bcg_edit
    bcg_edit = canvas.create_image(
        622.0,
        182.0,
        image=image_bcg_edit
    )
    # end of the bcg_edit
    #export
    global image_bcg_export
    image_bcg_export = PhotoImage(
        file=relative_to_assets("bcg_export.png"))
    global bcg_export
    bcg_export = canvas.create_image(
        525.0,
        182.0,
        image=image_bcg_export
    )

    #import
    global image_bcg_import
    image_bcg_import = PhotoImage(
        file=relative_to_assets("bcg_import.png"))
    global bcg_import
    bcg_import = canvas.create_image(
        476.0,
        182.0,
        image=image_bcg_import
    )

    # start of the pinterest
    global image_pinterest
    image_pinterest = PhotoImage(
        file=relative_to_assets("pinterest.png"))
    global pinterest
    pinterest = canvas.create_image(
        212.0,
        77.0,
        image=image_pinterest
    )
    # end of the pinterest
    # start of the bcg_entry
    
    global image_bcg_entry
    image_bcg_entry = PhotoImage(
        file=relative_to_assets("bcg_entry.png"))
    global bcg_entry
    bcg_entry = canvas.create_image(
        259.0,
        181.0,
        image=image_bcg_entry
    )
    # end of the bcg_entry
    # end of the button_sampah
    create_user_manager_gui(canvas)
