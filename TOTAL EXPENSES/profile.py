import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox # Import for pop-up messages
import sys
import os

current_script_dir = os.path.dirname(__file__)
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)

import database_manager # Import the database manager

class RoundedGUI:
    def __init__(self, master):
        self.master = master
        master.title("Profile Page")
        master.geometry("350x600")
        master.resizable(False, False)
        master.configure(bg="#FBF7F0")

        # Make the title bar disappear
        master.overrideredirect(True)

        # Center the window on the screen
        master.update_idletasks() # Ensure window dimensions are calculated
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = master.winfo_width()
        window_height = master.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"+{x}+{y}")

        # Initialize database (important to do once at startup)
        database_manager.initialize_db()

        # --- User ID and Username Handling ---
        # For testing, we'll use a sample user. In a real app, this would come from a login.
        self.user_id = 1 # Example: Assume user ID 1 exists. Adjust as needed for your testing.
        self.current_username = database_manager.get_username_by_id(self.user_id)
        if not self.current_username:
            # If user ID 1 doesn't exist, create a default user for demonstration
            # In a real app, this would lead to a registration/login flow
            default_username = "GuestUser"
            if database_manager.add_user(default_username):
                self.user_id = database_manager.get_user_id(default_username)
                self.current_username = default_username
                print(f"Created default user '{default_username}' with ID {self.user_id}")
            else:
                # If adding default user fails (e.g., username already exists)
                # Try to get the ID of the existing default user
                self.user_id = database_manager.get_user_id(default_username)
                self.current_username = database_manager.get_username_by_id(self.user_id)
                print(f"Using existing default user '{self.current_username}' with ID {self.user_id}")


        # --- Top Navigation Bar (Rounded Bottom Only, Full Width) ---
        # Make the height of the navbar a little smaller (from 70 to 60)
        self.top_nav_canvas = tk.Canvas(master, width=350, height=60, bg="#FBF7F0", highlightthickness=0)
        self.top_nav_canvas.pack(fill="x", side="top")
        # Draw the rounded navbar background on the canvas
        # Adjust y2 for draw_bottom_rounded_navbar to match new height
        self.draw_bottom_rounded_navbar(self.top_nav_canvas, 0, 0, 350, 60, radius=25, fill="#F2D7B2")

        # Back icon (double chevron)
        # Adjusted font size for "≪" to be less thick and more proportionate
        back_label = tk.Label(self.top_nav_canvas, text="≪", bg="#F2D7B2", fg="black", font=("Arial", 18, "normal"), bd=0)
        # Adjust y-coordinate for vertical centering in the new navbar height (60/2 = 30)
        self.top_nav_canvas.create_window(25, 30, window=back_label, anchor="w")
        back_label.bind("<Button-1>", lambda event: self.master.destroy())

        # Profile title (centered, bold, serif)
        # Make the "PROFILE" word in navbar smaller (from 28 to 16)
        profile_label = tk.Label(self.top_nav_canvas, text="PROFILE", bg="#F2D7B2", fg="black",
                                 font=("Playfair Display", 16, "bold"), bd=0)
        # Adjust y-coordinate for vertical centering in the new navbar height (60/2 = 30)
        self.top_nav_canvas.create_window(175, 30, window=profile_label, anchor="center")

        # --- User Profile Section ---
        profile_frame = tk.Frame(master, bg="#FBF7F0")
        profile_frame.pack(pady=10)

        # Speech bubble
        self.speech_bubble_canvas = tk.Canvas(profile_frame, width=150, height=50, bg="#FBF7F0", highlightthickness=0)
        self.speech_bubble_canvas.pack(pady=0)
        # Display actual username in speech bubble
        self.speech_bubble_text_id = self.draw_speech_bubble(self.speech_bubble_canvas, 75, 25, 90, 30, 20, f"Hi! {self.current_username}")

        # User icon (avatar)
        self.user_icon_canvas = tk.Canvas(profile_frame, width=110, height=110, bg="#FBF7F0", highlightthickness=0)
        self.user_icon_canvas.pack(pady=0)
        self.user_icon_canvas.create_oval(10, 10, 100, 100, fill="#E2E3E7", outline="")
        self.user_icon_canvas.create_oval(40, 35, 70, 65, fill="#555B66", outline="")
        self.user_icon_canvas.create_oval(35, 65, 75, 95, fill="#555B66", outline="")

        # "Edit Profile" is now a canvas with a rounded box (not clickable)
        edit_profile_width = 120
        edit_profile_height = 35
        self.edit_profile_canvas = tk.Canvas(profile_frame, width=edit_profile_width, height=edit_profile_height,
                                             bg=profile_frame["bg"], highlightthickness=0)
        self.edit_profile_canvas.pack(pady=10)
        # Draw the rounded rectangle on this canvas
        self.edit_profile_rect_id = self.round_rectangle(self.edit_profile_canvas, 2, 2,
                                                         edit_profile_width - 2, edit_profile_height - 2,
                                                         radius=edit_profile_height/2 - 5,
                                                         fill="#F9F3D6", outline="black", width=1)
        # Place text inside the canvas
        self.edit_profile_text_id = self.edit_profile_canvas.create_text(
            edit_profile_width / 2, edit_profile_height / 2,
            text="Edit Profile", font=("Arial", 10, "bold"), fill="black"
        )
        # No click event or hover effects for this non-clickable element


        # --- Main Rounded Box for Settings ---
        self.main_rounded_canvas = tk.Canvas(master, width=240, height=180, bg="#FBF7F0", highlightthickness=0)
        self.main_rounded_canvas.pack(pady=10)
        # Using draw_rounded_rectangle which uses round_rectangle (polygon smooth)
        self.draw_rounded_rectangle(self.main_rounded_canvas, 120, 90, 220, 160, radius=25,
                                    fill="#FDF4EA", outline="black", border_width=2)

        # Frame inside rounded box - this frame will hold the Entry and Button
        self.inner_frame = tk.Frame(self.main_rounded_canvas, bg="#FDF4EA")
        self.main_rounded_canvas.create_window(120, 90, window=self.inner_frame, anchor="center")

        # "Enter username" is now bigger and in a rounded box
        username_entry_canvas_width = 160
        username_entry_canvas_height = 40
        self.username_rounded_canvas = tk.Canvas(self.inner_frame, width=username_entry_canvas_width,
                                                  height=username_entry_canvas_height,
                                                  bg=self.inner_frame["bg"], highlightthickness=0)
        self.username_rounded_canvas.pack(pady=(20, 10))

        # Draw the rounded rectangle for the username entry
        self.username_rounded_rect_id = self.round_rectangle(self.username_rounded_canvas, 2, 2,
                                                              username_entry_canvas_width - 2,
                                                              username_entry_canvas_height - 2,
                                                              radius=username_entry_canvas_height / 2 - 5,
                                                              fill="white", outline="black", width=1)

        self.username_entry_var = tk.StringVar(value=self.current_username) # Set initial value to current username
        # Embed the Entry widget inside its new canvas
        self.username_entry = tk.Entry(self.username_rounded_canvas, textvariable=self.username_entry_var,
                                       font=("Arial", 12, "normal"),
                                       justify="center", bd=0, relief="flat",
                                       fg="black", insertbackground="black")
        # Place the entry perfectly centered within its canvas
        self.username_rounded_canvas.create_window(username_entry_canvas_width / 2,
                                                   username_entry_canvas_height / 2,
                                                   window=self.username_entry, anchor="center",
                                                   width=username_entry_canvas_width - 10,
                                                   height=username_entry_canvas_height - 10)

        # Bind events for username entry focus
        self.username_entry.bind("<FocusIn>", self.on_username_entry_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_username_entry_focus_out)


        # Save Changes button (remains a rounded button)
        # Make save button green
        self.save_changes_btn = self.create_rounded_button(self.inner_frame, "Save Changes", self.save_changes_action,
                                                          width=140, height=35, bg_color="#8BC34A", border_color="black")
        self.save_changes_btn.pack(pady=(0, 10))

        # --- Delete Account Button ---
        self.delete_account_btn = self.create_rounded_button(master, "DELETE ACCOUNT", self.delete_account_action,
                                                            width=170, height=38, bg_color="red", border_color="red",
                                                            text_color="white", text_font=("Arial", 11, "bold"))
        self.delete_account_btn.pack(pady=18)

    def draw_bottom_rounded_navbar(self, canvas, x1, y1, x2, y2, radius=25, fill="#F2D7B2"):
        """Draws a rectangle with only the bottom corners rounded."""
        # Top rectangular part
        canvas.create_rectangle(x1, y1, x2, y2 - radius, fill=fill, outline="")

        # Bottom-left rounded corner
        canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2,
                          start=180, extent=90, fill=fill, outline="")
        canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2,
                          start=270, extent=90, fill=fill, outline="")
        canvas.create_rectangle(x1 + radius, y2 - radius, x2 - radius, y2, fill=fill, outline="")


    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_rounded_rectangle(self, canvas, center_x, center_y, width, height, radius=20, fill="", outline="black", border_width=1):
        x1 = center_x - width / 2
        y1 = center_y - height / 2
        x2 = center_x + width / 2
        y2 = center_y + height / 2
        return self.round_rectangle(canvas, x1, y1, x2, y2, radius, fill=fill, outline=outline, width=border_width)


    def draw_speech_bubble(self, canvas, center_x, center_y, width, height, tail_offset, text_content):
        rect_x1 = center_x - width / 2
        rect_y1 = center_y - height / 2
        rect_x2 = center_x + width / 2
        rect_y2 = center_y + height / 2
        radius = 12
        self.round_rectangle(canvas, rect_x1, rect_y1, rect_x2, rect_y2, radius=radius, fill="white", outline="black")
        tail_base_x = center_x + tail_offset - 30
        tail_base_y = rect_y2
        polygon_id = canvas.create_polygon(tail_base_x - 10, tail_base_y,
                              tail_base_x + 10, tail_base_y,
                              tail_base_x, tail_base_y + 15,
                              fill="white", outline="black")
        text_id = canvas.create_text(center_x, center_y, text=text_content, font=("Arial", 9))
        return text_id # Return the text ID so it can be updated

    def create_rounded_button(self, parent, text, command, width, height, bg_color, border_color, text_color="black", text_font=("Arial", 10, "bold")):
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        canvas.pack_propagate(False)
        button_rect_id = self.round_rectangle(canvas, 2, 2, width-2, height-2, radius=height/2 - 5,
                                              fill=bg_color, outline=border_color, width=1)
        button_text_id = canvas.create_text(width / 2, height / 2, text=text, font=text_font, fill=text_color)
        canvas.bind("<Button-1>", lambda event: command())
        canvas.bind("<Enter>", lambda event: canvas.itemconfig(button_rect_id, outline="blue", width=2))
        canvas.bind("<Leave>", lambda event: canvas.itemconfig(button_rect_id, outline=border_color, width=1))
        return canvas

    def edit_profile_action(self):
        # This function is now just a placeholder since the "Edit Profile" box is not clickable
        print("Edit Profile box (now non-clickable) clicked!")

    def on_username_entry_focus_in(self, event):
        # When focus is gained, if the text is the current username, clear it only if it's the default/placeholder.
        # Otherwise, just set fg to black for typing.
        if self.username_entry_var.get() == self.current_username:
             self.username_entry.config(fg="black")
        # If it's the placeholder, clear it
        if self.username_entry_var.get() == "[username]":
            self.username_entry_var.set("")
            self.username_entry.config(fg="black")

    def on_username_entry_focus_out(self, event):
        # When focus is lost, if the entry is empty, restore the current username as visual cue.
        if not self.username_entry_var.get().strip(): # Check if it's empty or only whitespace
            self.username_entry_var.set(self.current_username)
            self.username_entry.config(fg="black") # Keep current username black
        else:
            self.username_entry.config(fg="black") # Ensure text remains black after typing


    def save_changes_action(self):
        new_username = self.username_entry_var.get().strip() # Get and strip whitespace
        if not new_username or new_username == "[username]": # Check for empty or placeholder
            messagebox.showwarning("Save Changes", "Please enter a valid username.")
            return

        if new_username == self.current_username:
            messagebox.showinfo("Save Changes", "Username is already up-to-date.")
            return

        # Call database_manager to update the username
        success = database_manager.update_username(self.user_id, new_username)
        if success:
            self.current_username = new_username # Update current username in GUI instance
            self.speech_bubble_canvas.itemconfig(self.speech_bubble_text_id, text=f"Hi! {self.current_username}")
            messagebox.showinfo("Save Changes", f"Username updated to '{new_username}' successfully!")
            self.username_entry.config(fg="black") # Ensure text remains black after save
        else:
            # This might happen if new_username already exists (UNIQUE constraint)
            messagebox.showerror("Save Changes", f"Failed to update username. It might already exist or be invalid.")

    def delete_account_action(self):
        print("DELETE ACCOUNT button clicked!")
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account and all associated data? This action will permanently delete the entire database file."):
            print("Account deletion confirmed. Attempting to delete database file...")
            # Close the database connection if it's open anywhere in the profile GUI itself
            # Although the database_manager functions open and close connections,
            # it's good practice to ensure no lingering connections from the GUI side
            # that might prevent file deletion.

            # It's crucial to call delete_database_file() first, as deleting the user from the
            # database file is pointless if the file itself is about to be removed.
            # However, if you want to log that the user was 'deleted' from the
            # perspective of the database records *before* the file is gone,
            # you'd reverse the order or handle it carefully.
            # For a full 'account wipe' including the file, deleting the file is the primary goal.

            db_delete_success = database_manager.delete_database_file()

            if db_delete_success:
                messagebox.showinfo("Account Deleted", "Your account and all associated data (database file) have been successfully deleted.")
                self.master.destroy() # Close the window after deletion
            else:
                messagebox.showerror("Account Deletion Failed", "An error occurred while trying to delete the database file. Please ensure the application has permissions and the file is not in use.")
        else:
            print("Account deletion cancelled.")

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = RoundedGUI(root)
    root.mainloop()