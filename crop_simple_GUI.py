import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for generating random data
fake = Faker()

# MySQL Database Connection Details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "2005",
    "database": "crop_management"
}

# List of sample crop names
crop_names = ["Wheat", "Rice", "Corn", "Soybean", "Barley", "Sugarcane", "Cotton", "Potato", "Tomato", "Lettuce"]

# List of possible growth stages
growth_stages = ["Seedling", "Vegetative", "Flowering", "Fruiting", "Maturity"]

# List of sample pest control measures
pest_control_measures_list = [
    "Use of organic pesticides",
    "Crop rotation",
    "Neem oil application",
    "Biological pest control",
    "Chemical pesticides",
    "Regular field monitoring",
]

# Database Connection Function
def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Function to Insert Manual Crop Record
def insert_manual_record():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        crop_name = crop_name_entry.get()
        planting_date = planting_date_entry.get()
        harvest_date = harvest_date_entry.get()
        growth_stage = growth_stage_entry.get()
        pest_control = pest_control_entry.get()
        yield_prediction = yield_entry.get()

        if not crop_name or not planting_date or not harvest_date or not growth_stage or not pest_control or not yield_prediction:
            messagebox.showwarning("⚠️ Input Error", "All fields must be filled!")
            return

        try:
            cursor.execute("""
                INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction))
            conn.commit()
            messagebox.showinfo("✅ Success", "Crop record inserted successfully!")
            conn.close()
            display_records()
        except mysql.connector.Error as e:
            messagebox.showerror("❌ Database Error", f"Error inserting record: {e}")

# Function to Generate Random Data for Bulk Insert
def generate_data():
    crop_name = random.choice(crop_names)
    planting_date = fake.date_between(start_date="-2y", end_date="today")
    harvest_date = planting_date + timedelta(days=random.randint(60, 180))
    growth_stage = random.choice(growth_stages)
    pest_control = random.choice(pest_control_measures_list)
    yield_prediction = random.randint(500, 5000)
    return (crop_name, planting_date, harvest_date, growth_stage, pest_control, yield_prediction)

# Function to Insert Bulk Records
def insert_bulk_records():
    num_records = int(record_count_var.get())
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        batch_size = 10000

        for i in range(0, num_records, batch_size):
            data_batch = [generate_data() for _ in range(min(batch_size, num_records - i))]
            cursor.executemany("""
                INSERT INTO crops (crop_name, planting_date, harvest_date, growth_stage, pest_control_measures, yield_prediction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data_batch)
            conn.commit()

            progress_label.config(text=f"🌱 {i + len(data_batch)} records inserted...")
            root.update_idletasks()

        messagebox.showinfo("✅ Success", f"{num_records} records inserted successfully!")
        conn.close()
        display_records()

# Function to Display Records
def display_records():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crops ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", "end", values=row)

# GUI Setup
root = tk.Tk()
root.title("🌾 Crop Management System")
root.geometry("900x700")
root.configure(bg="#f0f8ff")

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=20)

# Input Fields
labels = ["📋 Crop Name", "📅 Planting Date", "📅 Harvest Date", "🌱 Growth Stage", "🐜 Pest Control Measures", "🚜 Yield Prediction (kg)"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame, text=label, bg="#ffffff", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="w")
    entry = tk.Entry(frame)
    entry.grid(row=i, column=1)
    entries.append(entry)

crop_name_entry, planting_date_entry, harvest_date_entry, growth_stage_entry, pest_control_entry, yield_entry = entries

insert_button = tk.Button(frame, text="➕ Insert Record", command=insert_manual_record, bg="#32CD32", fg="white", font=("Arial", 12, "bold"))
insert_button.grid(row=6, column=0, columnspan=2, pady=10)

record_count_var = tk.StringVar(value="10000")
tk.Label(frame, text="🔢 Select Number of Records", bg="#ffffff", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky="w")
ttk.Combobox(frame, textvariable=record_count_var, values=["10000", "190000"]).grid(row=7, column=1)

bulk_insert_button = tk.Button(frame, text="🚀 Insert Bulk Records", command=insert_bulk_records, bg="#FF8C00", fg="white", font=("Arial", 12, "bold"))
bulk_insert_button.grid(row=8, column=0, columnspan=2, pady=10)

progress_label = tk.Label(frame, text="", bg="#ffffff", font=("Arial", 10))
progress_label.grid(row=9, column=0, columnspan=2)

# Table to Display Records
tree = ttk.Treeview(root, columns=("ID", "Crop Name", "Planting Date", "Harvest Date", "Growth Stage", "Pest Control", "Yield Prediction"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(pady=20)

# Load initial records
display_records()

# Run the GUI
root.mainloop()
