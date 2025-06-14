import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


categories = ["Food", "School Supplies", "Emergency Funds", "School Fees", "General Savings", "Personal Goal", "Future Purchases"]
amounts = [100, 100, 100, 100, 100, 100, 100]


root = tk.Tk()
root.title("TrackU")
root.geometry("800x500")
root.configure(bg='#fefae0')


header = tk.Frame(root, bg='#fcd5b5', height=60)
header.pack(fill=tk.X)


tk.Label(header, text="TrackU", font=("Helvetica", 18, "bold"), bg='#fcd5b5').pack(side=tk.LEFT, padx=20)
tk.Label(header, text="Total Savings", font=("Helvetica", 14), bg='#fcd5b5').pack(side=tk.RIGHT, padx=20)


content = tk.Frame(root, bg='#fefae0')
content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)


left_frame = tk.Frame(content, bg='#fefae0')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


month_dropdown = ttk.Combobox(left_frame, values=["Month", "January", "February", "March"])
month_dropdown.current(0)
month_dropdown.pack(pady=10)


fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
colors = ['red', 'gold', 'green', 'blue', 'purple', 'orange', 'pink']
ax.pie(amounts, labels=categories, colors=colors, startangle=90, wedgeprops={'edgecolor': 'white'})
ax.axis('equal')


canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.get_tk_widget().pack()


tk.Label(left_frame, text="Total Savings:\n₱ 100,000.00", font=("Helvetica", 14), bg='#fefae0').pack(pady=10)


right_frame = tk.Frame(content, bg='#fefae0', bd=2, relief=tk.GROOVE)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)


tk.Label(right_frame, text="Recent Transaction", font=("Helvetica", 14, "bold"), bg='#fefae0').pack(pady=5)


category_filter = ttk.Combobox(right_frame, values=["Category"] + categories)
category_filter.current(0)
category_filter.pack(pady=5)


transactions = [
   ("Food", "-100"),
   ("School Supplies", "-100"),
   ("Emergency Funds", "-100"),
   ("School Fees", "-100"),
   ("Food", "-100"),
   ("General Savings", "-100"),
   ("Personal Goal", "-100"),
   ("Future Purchases", "-100"),
]


for cat, amt in transactions:
   tk.Label(right_frame, text=f"• {cat:<20} {amt}", font=("Helvetica", 11), bg='#fefae0').pack(anchor='w', padx=10)


tk.Button(right_frame, text="+", font=("Helvetica", 16), bg='black', fg='white', width=2).pack(pady=10)


# VERY IMPORTANT!
root.mainloop()
