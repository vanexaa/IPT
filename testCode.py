import tkinter as tk

root = tk.Tk()

text = tk.Text(root, wrap='word', width=40, height=10)
text.pack()

# Create an invisible scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack_forget()  # Don't add it to the layout

# Connect the scrollbar to the text widget
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)

# Add sample content
for i in range(50):
    text.insert(tk.END, f"Line {i+1}\n")

root.mainloop()
