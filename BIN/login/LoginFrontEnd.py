import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def go_to_next_page():
    from First_Page import show_first_page  # Import only when needed
    first_frame.destroy()
    show_first_page(window)

def back_to_login():
    window.destroy()
    main()  # Recreate the main window

def main(reuse_window=None):
    global window, first_frame
    window = reuse_window if reuse_window else tk.Tk()

    if not reuse_window:
        window.geometry("1000x500")
        window.title("Prototype")
        window.minsize(width=1000, height=500)
        window.configure(bg="#ffdcdc")

    first_frame = tk.Frame(window, bg="#ffdcdc")
    first_frame.pack(fill="both", expand=True)

    content_frame = tk.Frame(first_frame, bg="#ffdcdc")
    content_frame.pack(expand=True)

    try:
        img = Image.open("LOGO.png")
        img = img.resize((320, 120))
        logo = ImageTk.PhotoImage(img)

        logo_label = tk.Label(content_frame, image=logo, bg="#ffdcdc")
        logo_label.image = logo
        logo_label.pack(pady=(0, 10))

    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}")

    try:
        img2 = Image.open("COIN.png")
        img2 = img2.resize((350, 350))
        coin_img = ImageTk.PhotoImage(img2)

        canvas = tk.Canvas(content_frame, width=350, height=350, bg="#ffdcdc", highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=coin_img)
        content_frame.coin_img = coin_img

        entry = tk.Entry(canvas, font=("Times New Roman", 14), justify="center")
        canvas.create_window(175, 150, window=entry, width=180)

        login_btn = tk.Button(canvas, text="Login", font=("Times New Roman", 12), command=go_to_next_page)
        canvas.create_window(175, 210, window=login_btn, width=100)

    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load coin image:\n{e}")

    if not reuse_window:
        window.mainloop()

if __name__ == "__main__":
    main()
