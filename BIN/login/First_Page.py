# First_Page.py
import tkinter as tk

def show_first_page(window):
    # Clear existing widgets in the window
    for widget in window.winfo_children():
        widget.destroy()

    # Create the next page
    next_frame = tk.Frame(window, bg="#ffdcdc")
    next_frame.pack(fill="both", expand=True)

    tk.Label(next_frame, text="Hello World", font=("Times New Roman", 18), bg="#ffdcdc").pack(pady=100)

    tk.Button(next_frame, text="Back", font=("Times New Roman", 12),
              command=lambda: go_back(window)).pack()

def go_back(window):
    from main_app import main  # Import here to avoid circular imports at the top
    for widget in window.winfo_children():
        widget.destroy()
    main(reuse_window=window)
