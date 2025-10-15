import tkinter as tk
from tkinter import messagebox
import json
import os

# ===== إنشاء أو تحميل ملف المهام =====
FILE_NAME = "tasks.json"

# دالة لتحميل المهام من الملف إذا كان موجود
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

# دالة لحفظ المهام في ملف JSON
def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ===== دوال التعامل مع المهام =====
def add_task():
    task = entry_task.get().strip()
    if task == "":
        messagebox.showwarning("تحذير", "لا يمكن إضافة مهمة فارغة!")
        return
    tasks.append({"task": task, "done": False})
    entry_task.delete(0, tk.END)
    update_listbox()
    save_tasks()

def delete_task():
    try:
        index = listbox_tasks.curselection()[0]
        del tasks[index]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showinfo("ملاحظة", "الرجاء اختيار مهمة لحذفها.")

def toggle_done():
    try:
        index = listbox_tasks.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showinfo("ملاحظة", "الرجاء اختيار مهمة لتغيير حالتها.")

def update_listbox():
    listbox_tasks.delete(0, tk.END)
    for t in tasks:
        # نضيف علامة ✓ إذا كانت المهمة منجزة
        status = "✓" if t["done"] else "✗"
        listbox_tasks.insert(tk.END, f"[{status}] {t['task']}")

# ===== إنشاء واجهة المستخدم =====
root = tk.Tk()
root.title("📋 Daily Task Manager")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="#2C2C2C")  # خلفية داكنة

# ===== عنوان التطبيق =====
title_label = tk.Label(root, text="إدارة المهام اليومية", fg="white", bg="#2C2C2C",
                       font=("Arial", 18, "bold"))
title_label.pack(pady=15)

# ===== إدخال المهام =====
frame_entry = tk.Frame(root, bg="#2C2C2C")
frame_entry.pack(pady=5)

entry_task = tk.Entry(frame_entry, width=25, font=("Arial", 14))
entry_task.grid(row=0, column=0, padx=10)

btn_add = tk.Button(frame_entry, text="➕ إضافة", font=("Arial", 12, "bold"),
                    bg="#4CAF50", fg="white", command=add_task)
btn_add.grid(row=0, column=1)

# ===== قائمة المهام =====
frame_list = tk.Frame(root, bg="#2C2C2C")
frame_list.pack(pady=10)

listbox_tasks = tk.Listbox(frame_list, width=45, height=12, font=("Arial", 12),
                           bg="#1E1E1E", fg="white", selectbackground="#4CAF50", activestyle="none")
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

# شريط تمرير (Scroll bar)
scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
listbox_tasks.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_tasks.yview)

# ===== أزرار التحكم =====
frame_buttons = tk.Frame(root, bg="#2C2C2C")
frame_buttons.pack(pady=15)

btn_delete = tk.Button(frame_buttons, text="🗑️ حذف", font=("Arial", 12, "bold"),
                       bg="#E74C3C", fg="white", width=10, command=delete_task)
btn_delete.grid(row=0, column=0, padx=5)

btn_done = tk.Button(frame_buttons, text="✔️ منجزة", font=("Arial", 12, "bold"),
                     bg="#3498DB", fg="white", width=10, command=toggle_done)
btn_done.grid(row=0, column=1, padx=5)

btn_exit = tk.Button(frame_buttons, text="🚪 خروج", font=("Arial", 12, "bold"),
                     bg="#9B59B6", fg="white", width=10, command=root.destroy)
btn_exit.grid(row=0, column=2, padx=5)

# ===== تحميل المهام وعرضها =====
tasks = load_tasks()
update_listbox()

# ===== تشغيل التطبيق =====
root.mainloop()