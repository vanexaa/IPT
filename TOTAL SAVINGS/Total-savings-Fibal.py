import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("TrackU")
root.geometry("900x520")
root.configure(bg="#faf6ef")

# Header
header = tk.Frame(root, bg="#ffe0b2", height=80)
header.place(relx=0, rely=0, relwidth=1, height=80)

# Title
tk.Label(header, text="TrackU", font=("Georgia", 24, "bold"), bg="#ffe0b2", fg="#222").place(x=30, y=22)

# Total Savings (header right)
tk.Label(header, text="Total Savings", font=("Georgia", 18), bg="#ffe0b2", fg="#222").place(relx=0.65, y=28)

# Hamburger menu
tk.Label(header, text="≡", font=("Arial", 28, "bold"), bg="#ffe0b2").place(relx=0.93, y=18)

# Month dropdown
month_var = tk.StringVar(value="Month")
month_combo = ttk.Combobox(root, textvariable=month_var, values=["Month", "Week", "Year"], state="readonly", font=("Georgia", 12))
month_combo.place(x=175, y=100, width=110)

# Pie chart
fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)
sizes = [25, 25, 25, 25]
colors = ["#e57373", "#ffd54f", "#81c784", "#64b5f6"]
explode = (0.05, 0.05, 0.05, 0.05)
ax.pie(sizes, colors=colors, explode=explode, startangle=90, wedgeprops=dict(width=0.8, edgecolor='w'))
ax.axis('equal')
plt.tight_layout()
canvas_chart = FigureCanvasTkAgg(fig, master=root)
canvas_chart.get_tk_widget().place(x=95, y=150)

# Total Savings
tk.Label(root, text="Total Savings:", font=("Georgia", 18), bg="#faf6ef").place(x=130, y=410)
tk.Label(root, text="+ ₱ 100,000.00", font=("Georgia", 16), bg="#faf6ef").place(x=140, y=450)

# Recent Transaction box
rt_frame = tk.Frame(root, bg="#fff8f0", highlightbackground="#222", highlightthickness=2)
rt_frame.place(x=420, y=90, width=430, height=390)

# Recent Transaction title
tk.Label(rt_frame, text="Recent Transaction", font=("Georgia", 18), bg="#fff8f0").place(x=15, y=10)
tk.Label(rt_frame, text="+", font=("Arial", 24, "bold"), bg="#fff8f0").place(x=380, y=10)

# Category dropdown
cat_var = tk.StringVar(value="Category")
cat_combo = ttk.Combobox(rt_frame, textvariable=cat_var, values=["Emergency Fund", "Food", "Future Purchases", "Personal Goals", "General Savings"], state="readonly", font=("Georgia", 10))
cat_combo.place(x=15, y=50, width=100)

# Amount label
tk.Label(rt_frame, text="Amount", font=("Georgia", 12), bg="#fff8f0").place(x=320, y=55)

# Transaction list
transactions = [
    "Food", "Schoo Suplies", "Emergency Funds", "School Fees",
    "Food", "General Savings", "Personal Goal", "Future Purchases"
]
y_start = 90
for i, t in enumerate(transactions):
    tk.Label(rt_frame, text="• " + t, font=("Georgia", 12), bg="#fff8f0").place(x=25, y=y_start + i*32)
    tk.Label(rt_frame, text="-100", font=("Georgia", 12), bg="#fff8f0").place(x=350, y=y_start + i*32)

# Peso sign watermark (simulate with a large faded label)
tk.Label(rt_frame, text="₱", font=("Arial", 150, "bold"), fg="#ffe0b2", bg="#fff8f0", anchor="center").place(x=180, y=120)

root.mainloop()