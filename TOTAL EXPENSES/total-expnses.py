import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("TrackU")
root.geometry("900x520")
root.configure(bg="#ffffff")

# Header
header = tk.Frame(root, bg="#ffe0b2", height=70)
header.place(relx=0, rely=0, relwidth=1, height=70)

# Title
tk.Label(header, text="TrackU", font=("Georgia", 22, "bold"), bg="#ffe0b2", fg="#222").place(x=30, y=18)

# Total Expenses (header right)
tk.Label(header, text="Total Expenses", font=("Georgia", 16), bg="#ffe0b2", fg="#222").place(relx=0.67, y=22)

# Hamburger menu
tk.Label(header, text="≡", font=("Arial", 24, "bold"), bg="#ffe0b2").place(relx=0.93, y=15)

# Month dropdown
month_var = tk.StringVar(value="Month")
month_combo = ttk.Combobox(root, textvariable=month_var, values=["Month", "Week", "Year"], state="readonly", font=("Georgia", 12))
month_combo.place(x=180, y=80, width=110)

# Pie chart
fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)
sizes = [50, 30, 20]
colors = ["#4dd0e1", "#ff8a65", "#ffd54f"]
explode = (0.05, 0.05, 0.05)
ax.pie(sizes, colors=colors, explode=explode, startangle=140, wedgeprops=dict(width=0.8, edgecolor='w'))
ax.axis('equal')
plt.tight_layout()
canvas_chart = FigureCanvasTkAgg(fig, master=root)
canvas_chart.get_tk_widget().place(x=100, y=120)

# Total Expenses and School Expenses
tk.Label(root, text="Total Expenses:", font=("Georgia", 16), bg="#ffffff").place(x=60, y=370)
tk.Label(root, text="- ₱ 100,000.00", font=("Georgia", 15), bg="#ffffff").place(x=70, y=400)

tk.Label(root, text="School Expenses:", font=("Georgia", 16), bg="#ffffff").place(x=260, y=370)
tk.Label(root, text="- ₱ 6,000.00", font=("Georgia", 15), bg="#ffffff").place(x=270, y=400)

# Recent Transaction box
rt_frame = tk.Frame(root, bg="#fff8f0", highlightbackground="#222", highlightthickness=2)
rt_frame.place(x=470, y=80, width=380, height=390)

# Recent Transaction title
tk.Label(rt_frame, text="Recent Transaction", font=("Georgia", 16), bg="#fff8f0").place(x=15, y=10)
tk.Label(rt_frame, text="+", font=("Arial", 22, "bold"), bg="#fff8f0").place(x=330, y=10)

# Category dropdown
cat_var = tk.StringVar(value="Category")
cat_combo = ttk.Combobox(rt_frame, textvariable=cat_var, values=["Travel Fare", "Food", "Emergency Fund", "School Supplies", "Others"], state="readonly", font=("Georgia", 10))
cat_combo.place(x=15, y=45, width=100)

# Amount label
tk.Label(rt_frame, text="Amount", font=("Georgia", 12), bg="#fff8f0").place(x=270, y=48)

# Transaction list
transactions = [
    "Food", "School Suplies", "Emergency Funds", "School Fees",
    "Food", "General Savings", "Personal Goal", "Future Purchases"
]
y_start = 80
for i, t in enumerate(transactions):
    tk.Label(rt_frame, text="• " + t, font=("Georgia", 12), bg="#fff8f0").place(x=25, y=y_start + i*32)
    tk.Label(rt_frame, text="-100", font=("Georgia", 12), bg="#fff8f0").place(x=300, y=y_start + i*32)

# Peso sign watermark (simulate with a large faded label)
tk.Label(rt_frame, text="₱", font=("Arial", 150, "bold"), fg="#ffe0b2", bg="#fff8f0", anchor="center").place(x=180, y=120)

root.mainloop()