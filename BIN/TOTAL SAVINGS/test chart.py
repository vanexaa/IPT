import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def create_interactive_pie_chart_gui():
    root = tk.Tk()
    root.title("Interactive Pie Chart Example")
    root.geometry("700x600")

    fig = Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)

    labels = ['Apples', 'Bananas', 'Oranges', 'Grapes', 'Mangoes']
    sizes = [30, 25, 15, 20, 10]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    explode = (0.05, 0, 0, 0, 0) # explode the first slice slightly

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%1.1f%%', shadow=True, startangle=140,
                                      pctdistance=0.85) # pctdistance moves the percentage text closer to the center
    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Interactive Pie Chart - Hover for Percentage")

    # Make the wedges pickable and store original labels for percentage
    for i, wedge in enumerate(wedges):
        wedge.set_picker(True) # Make each wedge pickable
        wedge.set_gid(i) # Assign a unique ID to each wedge (index)

    # Dictionary to store original percentage values
    original_percentages = {i: size / sum(sizes) * 100 for i, size in enumerate(sizes)}

    # Annotation object to display percentage on hover
    annotation = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                             bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="b", lw=2, alpha=0.8),
                             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="black"))
    annotation.set_visible(False) # Hide it initially

    # --- Event Handler ---
    def on_hover(event):
        # Check if the mouse is over the canvas
        if event.inaxes == ax:
            found_slice = False
            for wedge in wedges:
                # Check if the event is picking a wedge
                cont, ind = wedge.contains(event)
                if cont:
                    found_slice = True
                    # Get the index of the hovered slice
                    slice_index = wedge.get_gid()
                    percentage = original_percentages[slice_index]

                    # Get the position for the annotation
                    # We can use the center of the wedge for placement
                    x_center, y_center = wedge.center
                    theta = (wedge.theta1 + wedge.theta2) / 2
                    r = wedge.r * 0.8 # Position annotation slightly inside the radius

                    # Convert polar to Cartesian for annotation position
                    ann_x = x_center + r * np.cos(np.deg2rad(theta))
                    ann_y = y_center + r * np.sin(np.deg2rad(theta))

                    annotation.xy = (ann_x, ann_y)
                    annotation.set_text(f"{labels[slice_index]}: {percentage:.1f}%")
                    annotation.set_visible(True)
                    fig.canvas.draw_idle() # Redraw the canvas to show annotation
                    break
            if not found_slice:
                if annotation.get_visible():
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()
        else: # Mouse moved out of the axes
            if annotation.get_visible():
                annotation.set_visible(False)
                fig.canvas.draw_idle()

    # Connect the motion event to our handler
    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    # --- Embed in Tkinter ---
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

    ttk.Label(root, text="Hover over a slice to see its percentage.").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_interactive_pie_chart_gui()