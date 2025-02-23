import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import random

# Database setup
conn = sqlite3.connect("crop_management.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT,
        planting_date TEXT,
        harvest_date TEXT,
        growth_stage TEXT,
        pest_control TEXT,
        yield_kg INTEGER
    )
""")
conn.commit()

# Insert record function
def insert_record():
    crop = crop_var.get()
    planting_date = planting_date_entry.get()
    harvest_date = harvest_date_entry.get()
    growth_stage = growth_stage_var.get()
    pest_control = pest_control_var.get()
    yield_kg = yield_entry.get()

    if not all([crop, planting_date, harvest_date, growth_stage, pest_control, yield_kg]):
        messagebox.showerror("Error", "All fields must be filled!")
        return

    cursor.execute("INSERT INTO crops (crop, planting_date, harvest_date, growth_stage, pest_control, yield_kg) VALUES (?, ?, ?, ?, ?, ?)",
                   (crop, planting_date, harvest_date, growth_stage, pest_control, yield_kg))
    conn.commit()
    messagebox.showinfo("Success", "Record inserted successfully!")

# Bulk insert function
def insert_bulk():
    try:
        count = int(bulk_var.get())
        for _ in range(count):
            cursor.execute("INSERT INTO crops (crop, planting_date, harvest_date, growth_stage, pest_control, yield_kg) VALUES (?, ?, ?, ?, ?, ?)", 
                           (random.choice(crop_options), "01/01/25", "12/12/25", random.choice(growth_stages), random.choice(pest_controls), random.randint(100, 1000)))
        conn.commit()
        messagebox.showinfo("Success", f"{count} records inserted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert bulk data: {str(e)}")

# Display records function
def display_records():
    records_window = tk.Toplevel(root)
    records_window.title("Database Records")
    records_window.geometry("600x400")

    tree = ttk.Treeview(records_window, columns=("ID", "Crop", "Planting Date", "Harvest Date", "Growth Stage", "Pest Control", "Yield (kg)"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    cursor.execute("SELECT * FROM crops")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

# UI Setup
root = tk.Tk()
root.title("Crop Management System")
root.geometry("700x500")
root.configure(bg="#FFDAB9")

frame = tk.Frame(root, bg="white", bd=3, relief="ridge", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = tk.Label(frame, text="🌾 Crop Management System 🌾", font=("Arial", 16, "bold"), fg="purple", bg="white")
title_label.grid(row=0, columnspan=2, pady=10)

# Dropdown Options
crop_options = ["Wheat", "Rice", "Maize", "Barley", "Millet", "Soybean"]
growth_stages = ["Germination", "Vegetative", "Flowering", "Maturity"]
pest_controls = ["Pesticide", "Neem Oil", "Biological Control"]

# Input Fields
tk.Label(frame, text="🌱 Select Crop:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
crop_var = ttk.Combobox(frame, values=crop_options, width=20)
crop_var.grid(row=1, column=1, pady=5)

tk.Label(frame, text="📅 Planting Date:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5)
planting_date_entry = DateEntry(frame, width=18)
planting_date_entry.grid(row=2, column=1, pady=5)

tk.Label(frame, text="📆 Harvest Date:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", pady=5)
harvest_date_entry = DateEntry(frame, width=18)
harvest_date_entry.grid(row=3, column=1, pady=5)

tk.Label(frame, text="🌿 Growth Stage:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w", pady=5)
growth_stage_var = ttk.Combobox(frame, values=growth_stages, width=20)
growth_stage_var.grid(row=4, column=1, pady=5)

tk.Label(frame, text="🦟 Pest Control:", font=("Arial", 12), bg="white").grid(row=5, column=0, sticky="w", pady=5)
pest_control_var = ttk.Combobox(frame, values=pest_controls, width=20)
pest_control_var.grid(row=5, column=1, pady=5)

tk.Label(frame, text="📊 Yield (kg):", font=("Arial", 12), bg="white").grid(row=6, column=0, sticky="w", pady=5)
yield_entry = tk.Entry(frame, width=22)
yield_entry.grid(row=6, column=1, pady=5)

# Bulk Insert Option
tk.Label(frame, text="📂 Bulk Insert:", font=("Arial", 12), bg="white").grid(row=7, column=0, sticky="w", pady=5)
bulk_var = ttk.Combobox(frame, values=["10", "100", "1000", "2000", "5000", "10000"], width=20)
bulk_var.grid(row=7, column=1, pady=5)

# Buttons
insert_btn = tk.Button(frame, text="✅ Insert Record", font=("Arial", 12, "bold"), fg="white", bg="green", width=18, command=insert_record)
insert_btn.grid(row=8, columnspan=2, pady=10)

bulk_btn = tk.Button(frame, text="📦 Bulk Insert", font=("Arial", 12, "bold"), fg="white", bg="blue", width=18, command=insert_bulk)
bulk_btn.grid(row=9, columnspan=2, pady=5)

display_btn = tk.Button(frame, text="📜 Display Records", font=("Arial", 12, "bold"), fg="white", bg="purple", width=18, command=display_records)
display_btn.grid(row=10, columnspan=2, pady=5)

root.mainloop()
