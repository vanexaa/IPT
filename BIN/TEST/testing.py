import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 # Just an example database

class DataEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Editor")

        self.db_conn = self.create_database()

        self.create_widgets()
        self.load_data()

    def create_database(self):
        conn = sqlite3.connect('my_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value REAL
            )
        ''')
        # Insert some dummy data if the table is empty
        cursor.execute("SELECT COUNT(*) FROM items")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO items (name, value) VALUES ('Item A', 10.5)")
            cursor.execute("INSERT INTO items (name, value) VALUES ('Item B', 20.0)")
            cursor.execute("INSERT INTO items (name, value) VALUES ('Item C', 5.75)")
            conn.commit()
        return conn

    def create_widgets(self):
        # Frame for data display
        self.display_frame = ttk.LabelFrame(self.master, text="Existing Data")
        self.display_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.display_frame, columns=("ID", "Name", "Value"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Value", text="Value")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Value", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Frame for editing
        self.edit_frame = ttk.LabelFrame(self.master, text="Edit Selected Item")
        self.edit_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.edit_frame, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.id_entry = ttk.Entry(self.edit_frame, state="readonly")
        self.id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.edit_frame, text="Name:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.name_entry = ttk.Entry(self.edit_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.edit_frame, text="Value:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.value_entry = ttk.Entry(self.edit_frame)
        self.value_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        self.update_button = ttk.Button(self.edit_frame, text="Update Data", command=self.update_data)
        self.update_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.edit_frame.grid_columnconfigure(1, weight=1) # Allow column 1 to expand

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, name, value FROM items")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row, iid=row[0]) # Use ID as iid for easy lookup

    def on_item_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            self.clear_edit_fields()
            return

        item_id = selected_item[0] # The iid is the database ID
        values = self.tree.item(item_id, 'values')

        # Set the entries
        self.id_entry.config(state="normal") # Temporarily make editable to insert text
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, values[0])
        self.id_entry.config(state="readonly") # Make readonly again

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.value_entry.delete(0, tk.END)
        self.value_entry.insert(0, values[2])

    def clear_edit_fields(self):
        self.id_entry.config(state="normal")
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state="readonly")
        self.name_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def update_data(self):
        item_id = self.id_entry.get()
        new_name = self.name_entry.get()
        new_value_str = self.value_entry.get()

        if not item_id or not new_name or not new_value_str:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            new_value = float(new_value_str)
        except ValueError:
            messagebox.showerror("Error", "Value must be a number.")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE items SET name = ?, value = ? WHERE id = ?",
                           (new_name, new_value, item_id))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
            self.load_data() # Reload all data to show updated version
            self.clear_edit_fields() # Clear the edit form
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataEditorApp(root)
    root.mainloop()