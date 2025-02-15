import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
JSON_FILE = "data.json"

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as file:
        json.dump([], file)

def load_data():
    with open(JSON_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_record():
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()

    if not name or not age or not email:
        messagebox.showerror("Error", "All fields are required!")
        return

    data = load_data()
    data.append({"name": name, "age": int(age), "email": email}) 
    save_data(data)

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    
    messagebox.showinfo("Success", "Record added successfully!")
    refresh_table()

def refresh_table():
    for row in table.get_children():
        table.delete(row)
    data = load_data()
    for i, entry in enumerate(data):
        table.insert("", "end", values=(i+1, entry["name"], entry["age"], entry["email"]))

def delete_record():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No record selected!")
        return

    index = table.index(selected_item)
    data = load_data()
    del data[index]
    save_data(data)

    messagebox.showinfo("Success", "Record deleted successfully!")
    refresh_table()

def update_record():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No record selected!")
        return

    index = table.index(selected_item)
    data = load_data()

    new_name = entry_name.get()
    new_age = entry_age.get()
    new_email = entry_email.get()

    if not new_name or not new_age or not new_email:
        messagebox.showerror("Error", "All fields are required!")
        return

    data[index] = {"name": new_name, "age": int(new_age), "email": new_email}  
    save_data(data)

    messagebox.showinfo("Success", "Record updated successfully!")
    refresh_table()

def search_record():
    query = entry_search.get().lower()
    data = load_data()

    for row in table.get_children():
        table.delete(row)

    for i, entry in enumerate(data):
        if query in entry["name"].lower() or query in entry["email"].lower():
            table.insert("", "end", values=(i+1, entry["name"], entry["age"], entry["email"]))
          
sort_order = {"ID": True, "Name": True, "Age": True, "Email": True}  
def sort_table(column):
    data = load_data()
    if column == "ID":
        data = sorted(data, key=lambda x: data.index(x), reverse=not sort_order[column])
    elif column == "Name":
        data = sorted(data, key=lambda x: x["name"].lower(), reverse=not sort_order[column])
    elif column == "Age":
        data = sorted(data, key=lambda x: x["age"], reverse=not sort_order[column])
    elif column == "Email":
        data = sorted(data, key=lambda x: x["email"].lower(), reverse=not sort_order[column])
    sort_order[column] = not sort_order[column] 
    for row in table.get_children():
        table.delete(row)
    for i, entry in enumerate(data):
        table.insert("", "end", values=(i+1, entry["name"], entry["age"], entry["email"]))


root = tk.Tk()
root.title("JSON Data Manager")
root.geometry("600x450")
frame = tk.Frame(root)
frame.pack(pady=10)
tk.Label(frame, text="Name:").grid(row=0, column=0)

entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, padx=5)
tk.Label(frame, text="Age:").grid(row=1, column=0)

entry_age = tk.Entry(frame)
entry_age.grid(row=1, column=1, padx=5)
tk.Label(frame, text="Email:").grid(row=2, column=0)

entry_email = tk.Entry(frame)
entry_email.grid(row=2, column=1, padx=5)

btn_add = tk.Button(frame, text="Add Record", command=add_record)
btn_add.grid(row=0, column=2, padx=5)
btn_update = tk.Button(frame, text="Update Record", command=update_record)
btn_update.grid(row=1, column=2, padx=5)
btn_delete = tk.Button(frame, text="Delete Record", command=delete_record)
btn_delete.grid(row=2, column=2, padx=5)

tk.Label(root, text="Search:").pack()
entry_search = tk.Entry(root)
entry_search.pack(pady=5)

btn_search = tk.Button(root, text="Search", command=search_record)
btn_search.pack()

columns = ("ID", "Name", "Age", "Email")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col, command=lambda c=col: sort_table(c)) 
    table.column(col, width=100)

table.pack(expand=True, fill="both")
refresh_table()

root.mainloop()
