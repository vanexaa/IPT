import tkinter as tk
from tkinter import ttk
# Removed 'import math' as per your instruction.

class RoundedGUI:
    def __init__(self, master):
        """
        Initializes the Tkinter application with a main window and sets up the UI.
        """
        self.master = master
        master.title("Profile Page")
        master.geometry("350x600") # Adjusted window size as requested
        master.resizable(False, False) # Prevent resizing

        # Set a light background color for the main window
        master.configure(bg="#FBF7F0") # Light peach/cream color

        # --- Top Navigation Bar (Reverted to original frame, but with '<<' close function) ---
        top_frame = tk.Frame(master, bg="#F2D7B2", height=60) # Peach color
        top_frame.pack(fill="x", side="top")
        top_frame.pack_propagate(False) # Prevent frame from shrinking to content

        # Back icon (simplified using text for demonstration)
        back_label = tk.Label(top_frame, text="<<", bg="#F2D7B2", fg="black", font=("Arial", 20, "bold"))
        back_label.pack(side="left", padx=15)
        # ***MODIFIED: Bind click event to close the window***
        back_label.bind("<Button-1>", lambda event: self.master.destroy())

        # Profile title
        profile_label = tk.Label(top_frame, text="PROFILE", bg="#F2D7B2", fg="black", font=("Arial", 18, "bold"))
        # ***MODIFIED: Centered PROFILE in the navbar using .place()***
        profile_label.place(relx=0.5, rely=0.5, anchor="center")

        # Removed master.bind("<Configure>", self._on_master_configure) as it's no longer needed for tk.Frame navbar.
        # Removed self.top_navbar_canvas and related drawing logic for the top bar.

        # --- User Profile Section ---
        profile_frame = tk.Frame(master, bg="#FBF7F0")
        profile_frame.pack(pady=20)

        # "Hi! [username]" speech bubble - Drawn on a Canvas for customization
        self.speech_bubble_canvas = tk.Canvas(profile_frame, width=150, height=50, bg="#FBF7F0", highlightthickness=0)
        self.speech_bubble_canvas.pack(pady=5)
        self.draw_speech_bubble(self.speech_bubble_canvas, 75, 25, 60, 20, 10, "Hi! [username]")

        # User icon (placeholder)
        self.user_icon_canvas = tk.Canvas(profile_frame, width=100, height=100, bg="#FBF7F0", highlightthickness=0)
        self.user_icon_canvas.pack(pady=10)
        self.draw_rounded_circle(self.user_icon_canvas, 50, 50, 45, fill="#D9D9D9", outline="#D9D9D9") # Grey circle
        # Placeholder for person icon - Tkinter doesn't have built-in font icons easily
        self.user_icon_canvas.create_oval(30, 60, 70, 80, fill="#777777", outline="") # Body part
        self.user_icon_canvas.create_oval(40, 25, 60, 45, fill="#777777", outline="") # Head part

        # ***MODIFIED: "Edit Profile" is now a title (tk.Label) instead of a button***
        tk.Label(profile_frame, text="Edit Profile", bg="#FBF7F0", fg="black", font=("Arial", 12, "bold")).pack(pady=10)


        # --- Main Rounded Box for Settings ---
        self.main_rounded_canvas = tk.Canvas(master, width=280, height=200, bg="#FBF7F0", highlightthickness=0)
        self.main_rounded_canvas.pack(pady=20)
        self.draw_rounded_rectangle(self.main_rounded_canvas, 140, 100, 260, 180, radius=20,
                                    fill="#FBF7F0", outline="black", border_width=1)

        # Add content inside the rounded box
        # We'll use a frame placed directly over the canvas to hold Tkinter widgets
        self.inner_frame = tk.Frame(self.main_rounded_canvas, bg="#FBF7F0")
        self.main_rounded_canvas.create_window(140, 100, window=self.inner_frame, anchor="center")

        # ***MODIFIED: "Edit username" is a typable Entry field with placeholder logic***
        self.username_entry = tk.Entry(self.inner_frame,
                                       font=("Arial", 10),
                                       bg="#F2D7B2",
                                       fg="black",
                                       insertbackground="black", # Cursor color
                                       highlightthickness=1, # Border thickness when focused/unfocused
                                       highlightbackground="black", # Border color when unfocused
                                       highlightcolor="blue", # Border color when focused
                                       relief="flat", # Flat border for a cleaner look
                                       justify="center") # Center the text inside the entry
        self.username_entry.insert(0, "Enter a username") # Placeholder text for Entry
        self.username_entry_placeholder_active = True # Flag to track placeholder state
        self.username_entry.pack(pady=15, ipadx=10, ipady=5) # Internal padding for visual size

        # Bind events to clear/restore placeholder text
        self.username_entry.bind("<FocusIn>", self._on_username_entry_focus_in)
        self.username_entry.bind("<FocusOut>", self._on_username_entry_focus_out)


        # Save Changes button
        self.save_changes_button = self.create_rounded_button(self.inner_frame, "Save Changes", self.save_changes_action,
                                                              width=180, height=35, bg_color="#F2D7B2", border_color="black")
        self.save_changes_button.pack(pady=15)

        # --- Delete Account Button ---
        self.delete_account_button = self.create_rounded_button(master, "DELETE ACCOUNT", self.delete_account_action,
                                                                width=200, height=45, bg_color="red", border_color="red",
                                                                text_color="white", text_font=("Arial", 12, "bold"))
        self.delete_account_button.pack(pady=30)

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Draws a rounded rectangle on a Tkinter canvas.
        Args:
            canvas: The Tkinter Canvas widget.
            x1, y1: Top-left coordinates.
            x2, y2: Bottom-right coordinates.
            radius: Radius of the rounded corners.
            **kwargs: Other options for create_polygon or create_arc (e.g., fill, outline).
        """
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
        """
        Draws a rounded rectangle centered at (center_x, center_y) on the canvas.
        """
        x1 = center_x - width / 2
        y1 = center_y - height / 2
        x2 = center_x + width / 2
        y2 = center_y + height / 2
        return self.round_rectangle(canvas, x1, y1, x2, y2, radius, fill=fill, outline=outline, width=border_width)

    def draw_rounded_circle(self, canvas, center_x, center_y, radius, fill="", outline="black", border_width=1):
        """
        Draws a circle on the canvas. Tkinter's create_oval handles circles.
        """
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        return canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=border_width)

    def draw_speech_bubble(self, canvas, center_x, center_y, width, height, tail_offset, text_content):
        """
        Draws a speech bubble shape with text.
        """
        # Rounded rectangle part
        rect_x1 = center_x - width / 2
        rect_y1 = center_y - height / 2
        rect_x2 = center_x + width / 2
        rect_y2 = center_y + height / 2
        radius = 10 # Rounded corners for the bubble
        self.round_rectangle(canvas, rect_x1, rect_y1, rect_x2, rect_y2, radius=radius, fill="white", outline="black")

        # Tail part (triangle)
        tail_base_x = center_x + tail_offset
        tail_base_y = rect_y2 # Connects to the bottom of the bubble
        canvas.create_polygon(tail_base_x - 10, tail_base_y, # Left base point
                              tail_base_x + 10, tail_base_y, # Right base point
                              tail_base_x, tail_base_y + 15, # Tip of the tail
                              fill="white", outline="black")

        # Text inside the bubble
        canvas.create_text(center_x, center_y, text=text_content, font=("Arial", 10))

    def create_rounded_button(self, parent, text, command, width, height, bg_color, border_color, text_color="black", text_font=("Arial", 10, "bold")):
        """
        Creates a custom rounded button using a Canvas and a text item.
        """
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        canvas.pack_propagate(False) # Prevent canvas from shrinking

        # Draw the rounded rectangle for the button background
        # ***MODIFIED: Store the ID of the drawn rectangle for proper hover effect***
        button_rect_id = self.round_rectangle(canvas, 1, 1, width-1, height-1, radius=height/2 - 5,
                                             fill=bg_color, outline=border_color, width=1)

        # Add the text label on top of the canvas
        button_text_id = canvas.create_text(width / 2, height / 2, text=text, font=text_font, fill=text_color)

        # Bind click events to the canvas (which represents the button)
        canvas.bind("<Button-1>", lambda event: command())
        # ***MODIFIED: Add hover effects using itemconfig on the stored rectangle ID***
        canvas.bind("<Enter>", lambda event: canvas.itemconfig(button_rect_id, outline="blue", width=2))
        canvas.bind("<Leave>", lambda event: canvas.itemconfig(button_rect_id, outline=border_color, width=1))

        return canvas

    # Removed _on_master_configure method as it's no longer needed for the tk.Frame based navbar.

    # --- Entry Placeholder Logic ---
    def _on_username_entry_focus_in(self, event):
        """Clears placeholder text when the entry field gains focus."""
        if self.username_entry_placeholder_active:
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="black") # Change text color to normal
            self.username_entry_placeholder_active = False

    def _on_username_entry_focus_out(self, event):
        """Restores placeholder text if the entry field is left empty."""
        if not self.username_entry.get():
            self.username_entry.insert(0, "Enter a username")
            self.username_entry.config(fg="gray") # Optional: Change text color for placeholder
            self.username_entry_placeholder_active = True

    # --- Button Actions (Placeholder Functions) ---
    def edit_profile_action(self):
        # This function is no longer called by a button, but kept as a placeholder if needed later.
        print("Edit Profile action (now a title) triggered.")

    def edit_username_action(self):
        # This function is no longer called by a button.
        pass # The entry field itself handles the input

    def save_changes_action(self):
        # ***MODIFIED: Retrieve value from Entry field***
        username_text = self.username_entry.get()
        # If placeholder is active, do not save placeholder text
        if self.username_entry_placeholder_active and username_text == "Enter a username":
            print("No username entered to save.")
        else:
            print(f"Save Changes button clicked! Username: {username_text}")
        # Add your logic here for saving changes.

    def delete_account_action(self):
        print("DELETE ACCOUNT button clicked!")
        # Add your logic here for deleting the account

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = RoundedGUI(root)
    root.mainloop()
