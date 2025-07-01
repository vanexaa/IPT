# page_two.py (formerly 2.py)
import tkinter as tk

class PageTwo(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="#e0ffe0")
        self.controller = controller

        label = tk.Label(self, text="Welcome to Page Two!", font=("Arial", 24), bg="#e0ffe0")
        label.pack(pady=50)

        back_button = tk.Button(self, text="Go back to Page One",
                                command=lambda: self.controller.show_frame("PageOne"),
                                font=("Arial", 14), bg="#c0c0ff")
        back_button.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Page Two Standalone Test")
    page = PageTwo(root, None)
    page.pack(expand=True, fill="both")
    root.mainloop()