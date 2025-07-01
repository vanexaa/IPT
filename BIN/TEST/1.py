# 1.py
import tkinter as tk
from tkinter import ttk
from collections import OrderedDict

# Import our second page from the renamed file
from page_two import PageTwo # Make sure you've renamed 2.py to page_two.py

class PageOne(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="#ffe0e0") # Light red background
        self.controller = controller

        label = tk.Label(self, text="Welcome to Page One!", font=("Arial", 24), bg="#ffe0e0")
        label.pack(pady=50)

        next_button = tk.Button(self, text="Go to Page Two",
                                command=lambda: self.controller.show_frame("PageTwo"),
                                font=("Arial", 14), bg="#c0c0ff")
        next_button.pack(pady=10)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Natural Window Transition Demo") # Updated title
        self.geometry("800x600")
        self.resizable(False, False)

        container = tk.Frame(self, bg="gray")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = OrderedDict()

        for F in (PageOne, PageTwo):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.current_frame = None
        self.show_frame("PageOne") # No animate=False needed anymore

    def show_frame(self, page_name): # Removed 'animate' parameter
        """
        Switches to a new frame instantly. This is Tkinter's natural behavior.
        """
        new_frame = self.frames[page_name]

        if self.current_frame is not None:
            # If there's an old frame, ensure it's hidden.
            # tkraise() on the new frame will usually hide the old one if they
            # occupy the same grid/pack/place area, but explicitly hiding can be clearer.
            self.current_frame.place_forget() # Remove the old frame from layout

        new_frame.tkraise() # Bring the new frame to the top
        new_frame.place(x=0, y=0, relwidth=1, relheight=1) # Ensure new frame is visible at correct position
        self.current_frame = new_frame


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()