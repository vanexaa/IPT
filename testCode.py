import tkinter as tk

class FullscreenContentApp:
    def __init__(self, master):
        self.master = master
        master.title("Borderless Window") # This title won't be shown

        # Completely remove the native title bar and window borders
        master.overrideredirect(True)

        # Set an initial size (or it might be very small)
        master.geometry("800x600")

        # Optional: Make it full screen
        # master.attributes('-fullscreen', True)

        # Your application content goes directly into the root window
        # without a separate title bar frame
        label = tk.Label(master, text="This window has no title bar!",
                         font=("Arial", 20), bg="lightblue")
        label.pack(expand=True, fill="both")

        # Since there's no title bar, you need a way to close the window
        close_button = tk.Button(master, text="Close Window", command=master.destroy,
                                 font=("Arial", 14), bg="red", fg="white")
        close_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullscreenContentApp(root)
    root.mainloop()