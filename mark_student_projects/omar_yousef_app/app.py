import customtkinter as ctk
from tkinter import messagebox, Canvas
from PIL import Image
import json
import os
from datetime import datetime, timedelta
from openpyxl import Workbook
import shutil
import re
import random
import time
import pygame
import hashlib

# ========== إعدادات الواجهة ==========
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "students_data.json"
BACKUP_FILE = "students_data_backup.json"
MAX_GRADES = 100
EDIT_DAYS_LIMIT = 5
FIREWORKS_SOUND = "fireworks.wav"
EMAIL = "omar.alyousef.19999@gmail.com"

# ============================================================
# 🔹 دالة تشفير كلمة المرور
# ============================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================================
# 🔹 دالة حفظ البيانات
# ============================================================
def save_data(data):
    try:
        if os.path.exists(DATA_FILE):
            shutil.copy(DATA_FILE, BACKUP_FILE)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل حفظ البيانات: {str(e)}")
        raise

# ============================================================
# 🔹 دالة تحميل البيانات
# ============================================================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"accounts": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "accounts" not in data:
                data = {"accounts": [data]}
            return data
    except json.JSONDecodeError:
        messagebox.showerror("خطأ", "ملف البيانات تالف. سيتم إنشاء ملف جديد.")
        return {"accounts": []}
    except Exception as e:
        messagebox.showerror("خطأ", f"فشل تحميل البيانات: {str(e)}")
        return {"accounts": []}

# ============================================================
# 🔹 دالة عرض الألعاب النارية
# ============================================================
def show_fireworks(master, lang):
    try:
        pygame.mixer.init()
        if os.path.exists(FIREWORKS_SOUND):
            pygame.mixer.music.load(FIREWORKS_SOUND)
            pygame.mixer.music.play()
        else:
            messagebox.showwarning(
                "تحذير" if lang == "ar" else "Warning",
                f"ملف الصوت {FIREWORKS_SOUND} غير موجود." if lang == "ar" else f"Sound file {FIREWORKS_SOUND} not found."
            )
    except Exception as e:
        messagebox.showerror(
            "خطأ" if lang == "ar" else "Error",
            f"فشل تشغيل الصوت: {str(e)}" if lang == "ar" else f"Failed to play sound: {str(e)}"
        )

    popup = ctk.CTkToplevel(master)
    popup.title("الألعاب النارية" if lang == "ar" else "Fireworks")
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.5)
    popup.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
    popup.transient(master)
    popup.grab_set()

    canvas = Canvas(popup, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    particles = []
    colors = ["red", "yellow", "blue", "green", "purple", "white"]

    def create_particle():
        x = random.randint(50, window_width - 50)
        y = random.randint(50, window_height - 50)
        size = random.randint(5, 15)
        color = random.choice(colors)
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
        particle = canvas.create_oval(x, y, x + size, y + size, fill=color)
        return {"id": particle, "dx": dx, "dy": dy, "life": 50}

    def animate():
        nonlocal particles
        if len(particles) < 20:
            particles.append(create_particle())
        new_particles = []
        for p in particles:
            canvas.move(p["id"], p["dx"], p["dy"])
            p["life"] -= 1
            if p["life"] > 0:
                new_particles.append(p)
            else:
                canvas.delete(p["id"])
        particles = new_particles
        if particles:
            popup.after(50, animate)
        else:
            popup.destroy()

    for _ in range(10):
        particles.append(create_particle())
    animate()
    popup.after(3000, lambda: [pygame.mixer.music.stop(), popup.destroy()])

# ============================================================
# 🔹 واجهة إدارة الحسابات
# ============================================================
class AccountManagerWindow(ctk.CTk):
    def __init__(self, lang="ar"):
        super().__init__()
        self.title("إدارة الحسابات" if lang == "ar" else "Account Manager")
        self.lang = lang
        self.data = load_data()
        self.accounts = self.data.get("accounts", [])

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")


        try:
            ima_path = r"C:\Users\hasanha\Desktop\py-cpc-1\mark_student_projects\omar_yousef_app\background.jpg"
            self.background_image = ctk.CTkImage(dark_image=Image.open("background.png"), size=(window_width, window_height))
        except FileNotFoundError:
            messagebox.showwarning(
                "تحذير" if lang == "ar" else "Warning",
                "ملف الخلفية غير موجود." if lang == "ar" else "Background image not found."
            )
            self.background_image = None

        self.canvas = Canvas(self, width=window_width, height=window_height, bg="#1E1E1E" if not self.background_image else None)
        self.canvas.pack(fill="both", expand=True)
        if self.background_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_frame,
            text="إدارة الحسابات" if lang == "ar" else "Manage Accounts",
            font=("Cairo" if lang == "ar" else "Arial", 24, "bold")
        ).pack(pady=15)

        self.account_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        self.account_frame.pack(pady=10, fill="both", expand=True)

        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.pack(pady=10, fill="x", padx=10)

        lang_btn = ctk.CTkButton(
            button_frame,
            text="🇬🇧 English" if lang == "ar" else "🇸🇦 العربية",
            font=("Cairo" if lang == "ar" else "Arial", 12),
            command=self.toggle_language,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        lang_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ إنشاء حساب جديد" if lang == "ar" else "➕ Create New Account",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.create_new_account,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        add_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.load_accounts()

    def load_accounts(self):
        for widget in self.account_frame.winfo_children():
            widget.destroy()

        for i, account in enumerate(self.accounts):
            row = ctk.CTkFrame(self.account_frame, corner_radius=5, fg_color="#424242")
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(
                row,
                text=f"{i+1}. {account['teacher']} - {account['institute']}",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                anchor="w" if self.lang == "ar" else "e"
            ).pack(side="left" if self.lang == "ar" else "right", padx=10, fill="x", expand=True)

            open_btn = ctk.CTkButton(
                row,
                text="📂 فتح" if self.lang == "ar" else "📂 Open",
                width=80,
                command=lambda acc=account: self.show_password_prompt(acc)
            )
            open_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

            delete_btn = ctk.CTkButton(
                row,
                text="🗑️ حذف" if self.lang == "ar" else "🗑️ Delete",
                width=80,
                fg_color="#D32F2F",
                hover_color="#F44336",
                command=lambda idx=i: self.delete_account(idx)
            )
            delete_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

    def toggle_language(self):
        new_lang = "en" if self.lang == "ar" else "ar"
        self.destroy()
        AccountManagerWindow(new_lang).mainloop()

    def create_new_account(self):
        self.destroy()
        CreateAccountWindow(self.lang).mainloop()

    def show_password_prompt(self, account):
        popup = ctk.CTkToplevel(self)
        popup.title("تأكيد كلمة المرور" if self.lang == "ar" else "Password Confirmation")
        popup.geometry("400x300")
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="أدخل كلمة المرور:" if self.lang == "ar" else "Enter Password:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=10)

        password_entry = ctk.CTkEntry(
            frame,
            show="*",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        password_entry.pack(pady=10, padx=20, fill="x")
        password_entry.focus_set()

        password_entry.bind("<Return>", lambda event: verify_password())

        show_password_switch = ctk.CTkSwitch(
            frame,
            text="إظهار كلمة المرور" if self.lang == "ar" else "Show Password",
            command=lambda: password_entry.configure(show="" if show_password_switch.get() else "*"),
            font=("Cairo" if self.lang == "ar" else "Arial", 12)
        )
        show_password_switch.pack(pady=10)

        def verify_password():
            entered_password = password_entry.get().strip()
            hashed_entered_password = hash_password(entered_password)
            if hashed_entered_password == account.get("password", ""):
                popup.destroy()
                self.destroy()
                StudentWindow(account, self.lang).mainloop()
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "كلمة المرور غير صحيحة." if self.lang == "ar" else "Incorrect password."
                )

        verify_btn = ctk.CTkButton(
            frame,
            text="تحقق" if self.lang == "ar" else "Verify",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=verify_password,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        verify_btn.pack(pady=10)

        cancel_btn = ctk.CTkButton(
            frame,
            text="إلغاء" if self.lang == "ar" else "Cancel",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=popup.destroy,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        cancel_btn.pack(pady=5)

        forgot_password_btn = ctk.CTkButton(
            frame,
            text="نسيت كلمة المرور؟" if self.lang == "ar" else "Forgot Password?",
            font=("Cairo" if self.lang == "ar" else "Arial", 12),
            command=lambda: self.show_forgot_password(account, popup),
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        forgot_password_btn.pack(pady=10)

    def show_forgot_password(self, account, parent_popup):
        forgot_popup = ctk.CTkToplevel(self)
        forgot_popup.title("نسيت كلمة المرور" if self.lang == "ar" else "Forgot Password")
        forgot_popup.geometry("400x250")
        forgot_popup.transient(self)
        forgot_popup.grab_set()

        frame = ctk.CTkFrame(forgot_popup, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="أدخل بريدك الإلكتروني:" if self.lang == "ar" else "Enter your email:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=10)

        email_entry = ctk.CTkEntry(
            frame,
            placeholder_text="البريد الإلكتروني" if self.lang == "ar" else "Email",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        email_entry.pack(pady=10, padx=20, fill="x")
        email_entry.focus_set()

        def verify_email():
            entered_email = email_entry.get().strip()
            if entered_email == EMAIL:
                parent_popup.destroy()
                forgot_popup.destroy()
                messagebox.showinfo(
                    "تم" if self.lang == "ar" else "Success",
                    f"كلمة المرور الخاصة بك هي: {account.get('raw_password', 'غير متوفرة')}" if self.lang == "ar" else f"Your password is: {account.get('raw_password', 'Not available')}"
                )
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "البريد الإلكتروني غير صحيح." if self.lang == "ar" else "Incorrect email."
                )

        email_entry.bind("<Return>", lambda event: verify_email())

        verify_email_btn = ctk.CTkButton(
            frame,
            text="تحقق" if self.lang == "ar" else "Verify",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=verify_email,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        verify_email_btn.pack(pady=15)

        cancel_email_btn = ctk.CTkButton(
            frame,
            text="إلغاء" if self.lang == "ar" else "Cancel",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=forgot_popup.destroy,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        cancel_email_btn.pack(pady=5)

    def delete_account(self, index):
        if messagebox.askyesno(
            "تأكيد" if self.lang == "ar" else "Confirm",
            "هل تريد حذف هذا الحساب؟" if self.lang == "ar" else "Do you want to delete this account?"
        ):
            del self.accounts[index]
            self.data["accounts"] = self.accounts
            save_data(self.data)
            self.load_accounts()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم حذف الحساب بنجاح." if self.lang == "ar" else "Account deleted successfully."
            )

# ============================================================
# 🔹 واجهة إنشاء الحساب
# ============================================================
class CreateAccountWindow(ctk.CTk):
    def __init__(self, lang="ar"):
        super().__init__()
        self.title("نظام المعهد - إنشاء حساب" if lang == "ar" else "Institute System - Create Account")
        self.lang = lang
        self.data = load_data()
        self.students = []

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        try:
            self.background_image = ctk.CTkImage(dark_image=Image.open("background.png"), size=(window_width, window_height))
        except FileNotFoundError:
            messagebox.showwarning(
                "تحذير" if lang == "ar" else "Warning",
                "ملف الخلفية غير موجود." if lang == "ar" else "Background image not found."
            )
            self.background_image = None

        self.canvas = Canvas(self, width=window_width, height=window_height, bg="#1E1E1E" if not self.background_image else None)
        self.canvas.pack(fill="both", expand=True)
        if self.background_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_frame,
            text="إنشاء حساب أستاذ" if lang == "ar" else "Create Teacher Account",
            font=("Cairo" if lang == "ar" else "Arial", 24, "bold")
        ).pack(pady=15)

        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="اسم الأستاذ" if lang == "ar" else "Teacher Name",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.name_entry.pack(pady=10, padx=40, fill="x")

        self.inst_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="اسم المعهد" if lang == "ar" else "Institute Name",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.inst_entry.pack(pady=10, padx=40, fill="x")

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="كلمة المرور" if lang == "ar" else "Password",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40,
            show="*"
        )
        self.password_entry.pack(pady=10, padx=40, fill="x")

        self.show_password_switch = ctk.CTkSwitch(
            self.main_frame,
            text="إظهار كلمة المرور" if lang == "ar" else "Show Password",
            command=self.toggle_password_visibility,
            font=("Cairo" if lang == "ar" else "Arial", 14)
        )
        self.show_password_switch.pack(pady=5)

        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.pack(pady=10, fill="x", padx=10)

        self.add_students_btn = ctk.CTkButton(
            button_frame,
            text="➕ إضافة الطلاب" if lang == "ar" else "➕ Add Students",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.open_student_input,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        self.add_students_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.create_btn = ctk.CTkButton(
            button_frame,
            text="✅ إنشاء الحساب" if lang == "ar" else "✅ Create Account",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.create_account,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        self.create_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.manager_btn = ctk.CTkButton(
            button_frame,
            text="📋 إدارة الحسابات" if lang == "ar" else "📋 Manage Accounts",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.goto_account_manager,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        self.manager_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        lang_btn = ctk.CTkButton(
            button_frame,
            text="🇬🇧 English" if lang == "ar" else "🇸🇦 العربية",
            font=("Cairo" if lang == "ar" else "Arial", 12),
            command=self.toggle_language,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        lang_btn.pack(side="right" if lang == "ar" else "left", padx=5)

    def toggle_password_visibility(self):
        if self.show_password_switch.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def toggle_language(self):
        new_lang = "en" if self.lang == "ar" else "ar"
        self.destroy()
        CreateAccountWindow(new_lang).mainloop()

    def goto_account_manager(self):
        if self.data["accounts"]:
            self.destroy()
            AccountManagerWindow(self.lang).mainloop()
        else:
            messagebox.showinfo(
                "تنبيه" if self.lang == "ar" else "Alert",
                "لم يتم إنشاء أي حساب بعد." if self.lang == "ar" else "No accounts have been created yet."
            )

    def open_student_input(self):
        self.student_input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.student_input_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            self.student_input_frame,
            text="إضافة طالب" if self.lang == "ar" else "Add Student",
            font=("Cairo" if self.lang == "ar" else "Arial", 16, "bold")
        ).pack(pady=5)

        self.student_entry = ctk.CTkEntry(
            self.student_input_frame,
            placeholder_text="اسم الطالب" if self.lang == "ar" else "Student Name",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.student_entry.pack(side="left" if self.lang == "ar" else "right", padx=5, fill="x", expand=True)
        self.student_entry.bind("<Return>", lambda event: self.add_student())

        add_btn = ctk.CTkButton(
            self.student_input_frame,
            text="➕ إضافة" if self.lang == "ar" else "➕ Add",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.add_student,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        add_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        remove_btn = ctk.CTkButton(
            self.student_input_frame,
            text="🗑️ حذف" if self.lang == "ar" else "🗑️ Remove",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.remove_student,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        remove_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        self.student_list_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        self.student_list_frame.pack(pady = 10, padx=40, fill="both", expand=True)
        self.refresh_student_list()

    def add_student(self):
        name = self.student_entry.get().strip()
        print(f"محاولة إضافة طالب: {name}")
        if not name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الرجاء إدخال اسم الطالب." if self.lang == "ar" else "Please enter a student name."
            )
            return
        if not re.match(r"^[a-zA-Z\sأ-ي]+$", name):
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الاسم يجب أن يحتوي على حروف فقط (بدون أرقام أو رموز)." if self.lang == "ar" else "Name must contain letters only (no numbers or symbols)."
            )
            return
        if any(s["name"] == name for s in self.students):
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "اسم الطالب موجود بالفعل." if self.lang == "ar" else "Student name already exists."
            )
            return

        self.students.append({"name": name, "grades": [], "info": ""})
        print(f"تمت إضافة الطالب: {name}, القائمة الآن: {self.students}")
        self.student_entry.delete(0, "end")
        self.refresh_student_list()
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            f"تم إضافة الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} added successfully."
        )

    def remove_student(self):
        name = self.student_entry.get().strip()
        if not name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الرجاء إدخال اسم الطالب لحذفه." if self.lang == "ar" else "Please enter a student name to remove."
            )
            return
        if any(s["name"] == name for s in self.students):
            self.students = [s for s in self.students if s["name"] != name]
            self.student_entry.delete(0, "end")
            self.refresh_student_list()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حذف الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} removed successfully."
            )
        else:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "اسم الطالب غير موجود." if self.lang == "ar" else "Student name not found."
            )

    def refresh_student_list(self):
        for widget in self.student_list_frame.winfo_children():
            widget.destroy()

        if not self.students:
            ctk.CTkLabel(
                self.student_list_frame,
                text="لا يوجد طلاب مضافين بعد." if self.lang == "ar" else "No students added yet.",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                text_color="gray"
            ).pack(pady=10)
        else:
            for i, student in enumerate(self.students):
                row = ctk.CTkFrame(self.student_list_frame, corner_radius=5, fg_color="#424242")
                row.pack(fill="x", pady=5, padx=5)
                ctk.CTkLabel(
                    row,
                    text=f"{i+1}. {student['name']}",
                    font=("Cairo" if self.lang == "ar" else "Arial", 14),
                    anchor="w" if self.lang == "ar" else "e"
                ).pack(pady=5, padx=10, fill="x")
        print(f"تم تحديث قائمة الطلاب: {self.students}")

    def create_account(self):
        name = self.name_entry.get().strip()
        inst = self.inst_entry.get().strip()
        raw_password = self.password_entry.get().strip()

        if not name or not inst or not raw_password:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الرجاء إدخل جميع البيانات بما في ذلك كلمة المرور." if self.lang == "ar" else "Please enter all fields including password."
            )
            return

        if not self.students:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الرجاء إضافة الطلاب أولاً." if self.lang == "ar" else "Please add students first."
            )
            return

        hashed_password = hash_password(raw_password)
        creation_date = datetime.now().strftime("%Y-%m-%d")
        new_account = {
            "teacher": name,
            "institute": inst,
            "created_at": creation_date,
            "students": self.students,
            "password": hashed_password,
            "raw_password": raw_password
        }

        self.data["accounts"].append(new_account)
        save_data(self.data)
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            "تم إنشاء الحساب بنجاح 🎉" if self.lang == "ar" else "Account created successfully 🎉"
        )

        self.destroy()
        AccountManagerWindow(self.lang).mainloop()

# ============================================================
# 🔹 واجهة إدارة الطلاب
# ============================================================
class StudentWindow(ctk.CTk):
    def __init__(self, account, lang="ar"):
        super().__init__()
        self.account = account
        self.lang = lang
        self.title("إدارة الطلاب" if lang == "ar" else "Manage Students")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        try:
            self.background_image = ctk.CTkImage(dark_image=Image.open("background.png"), size=(window_width, window_height))
        except FileNotFoundError:
            messagebox.showwarning(
                "تحذير" if lang == "ar" else "Warning",
                "ملف الخلفية غير موجود." if lang == "ar" else "Background image not found."
            )
            self.background_image = None

        self.canvas = Canvas(self, width=window_width, height=window_height, bg="#1E1E1E" if not self.background_image else None)
        self.canvas.pack(fill="both", expand=True)
        if self.background_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_frame,
            text=f"المعهد: {account['institute']}" if lang == "ar" else f"Institute: {account['institute']}",
            font=("Cairo" if lang == "ar" else "Arial", 24, "bold")
        ).pack(pady=15)

        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        search_frame.pack(pady=10, padx=40, fill="x")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث عن طالب..." if lang == "ar" else "Search for a student...",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.search_entry.pack(side="right" if lang == "ar" else "left", fill="x", expand=True, padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 بحث" if lang == "ar" else "🔍 Search",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.filter_students,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8,
            width=100
        )
        search_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#37474F")
        self.stats_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            self.stats_frame,
            text="📈 الإحصائيات" if lang == "ar" else "📈 Statistics",
            font=("Cairo" if lang == "ar" else "Arial", 16, "bold")
        ).pack(pady=5)

        self.stats_labels = {
            "count": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "avg": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "max": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "min": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "above_90": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14))
        }
        for label in self.stats_labels.values():
            label.pack(pady=2, anchor="w" if lang == "ar" else "e")

        student_input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        student_input_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            student_input_frame,
            text="إضافة طالب" if self.lang == "ar" else "Add Student",
            font=("Cairo" if self.lang == "ar" else "Arial", 16, "bold")
        ).pack(pady=5)

        self.student_entry = ctk.CTkEntry(
            student_input_frame,
            placeholder_text="اسم الطالب" if lang == "ar" else "Student Name",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.student_entry.pack(side="left" if self.lang == "ar" else "right", padx=5, fill="x", expand=True)
        self.student_entry.bind("<Return>", lambda event: self.add_student())

        add_btn = ctk.CTkButton(
            student_input_frame,
            text="➕ إضافة" if self.lang == "ar" else "➕ Add",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.add_student,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        add_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        remove_btn = ctk.CTkButton(
            student_input_frame,
            text="🗑️ حذف" if self.lang == "ar" else "🗑️ Remove",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.remove_student,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        remove_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        save_btn = ctk.CTkButton(
            student_input_frame,
            text="💾 حفظ" if self.lang == "ar" else "💾 Save",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.save_students,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        save_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.pack(pady=10, fill="x")

        export_btn = ctk.CTkButton(
            button_frame,
            text="📊 تصدير إلى Excel" if lang == "ar" else "📊 Export to Excel",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.export_to_excel,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        export_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        restart_btn = ctk.CTkButton(
            button_frame,
            text="🔄 إعادة بدء" if lang == "ar" else "🔄 Restart",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.restart_students,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        restart_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        return_btn = ctk.CTkButton(
            button_frame,
            text="⬅️ رجوع إلى إدارة الحسابات" if lang == "ar" else "⬅️ Back to Account Manager",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.back_to_manager,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        return_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8, width=window_width - 100)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        # إعداد الرأس باستخدام grid
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#37474F")
        header_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        header_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = [
            ("رقم" if self.lang == "ar" else "No.", 50),
            ("الاسم" if self.lang == "ar" else "Name", 200),
            ("المجموع" if self.lang == "ar" else "Total", 100),
            ("ملاحظات" if self.lang == "ar" else "Notes", 300),
            ("إجراءات" if self.lang == "ar" else "Actions", 100)
        ]

        for col, (text, width) in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Cairo" if self.lang == "ar" else "Arial", 14, "bold"),
                width=width
            ).grid(row=0, column=col, padx=5, sticky="ew")

        self.load_students()

    def update_stats(self):
        students = self.account["students"]
        count = len(students)
        totals = [sum(s.get("grades", [])) for s in students]
        avg = sum(totals) / count if count > 0 else 0
        max_grade = max(totals) if totals else 0
        min_grade = min(totals) if totals else 0
        above_90 = sum(1 for t in totals if (t / MAX_GRADES) * 100 >= 90) if totals else 0

        stats_text = {
            "count": f"عدد الطلاب: {count}" if self.lang == "ar" else f"Number of Students: {count}",
            "avg": f"متوسط العلامات: {avg:.2f}" if self.lang == "ar" else f"Average Grade: {avg:.2f}",
            "max": f"أعلى درجة: {max_grade}" if self.lang == "ar" else f"Highest Grade: {max_grade}",
            "min": f"أدنى درجة: {min_grade}" if self.lang == "ar" else f"Lowest Grade: {min_grade}",
            "above_90": f"الطلاب فوق 90%: {above_90}" if self.lang == "ar" else f"Students above 90%: {above_90}"
        }

        for key, label in self.stats_labels.items():
            label.configure(text=stats_text[key])

    def toggle_language(self):
        new_lang = "en" if self.lang == "ar" else "ar"
        self.destroy()
        StudentWindow(self.account, new_lang).mainloop()

    def filter_students(self):
        search_term = self.search_entry.get().strip().lower()
        filtered_students = [
            s for s in self.account["students"]
            if search_term in s["name"].lower()
        ]
        self.load_students(filtered_students if search_term else self.account["students"])

    def load_students(self, students=None):
        # إزالة جميع العناصر باستثناء الرأس
        for widget in self.table_frame.winfo_children()[1:]:
            widget.destroy()

        students = students or self.account["students"]
        sorted_students = sorted(students, key=lambda x: sum(x.get("grades", [])), reverse=True)

        # إعداد grid للصفوف
        self.table_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        for i, student in enumerate(sorted_students):
            total = sum(student.get("grades", []))
            row = ctk.CTkFrame(self.table_frame, corner_radius=5, fg_color="#424242")
            row.grid(row=i+1, column=0, sticky="ew", pady=2, padx=5)
            row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            rank_icon = ""
            if i == 0 and len(sorted_students) >= 1:
                rank_icon = "🥇"
            elif i == 1 and len(sorted_students) >= 2:
                rank_icon = "🥈"
            elif i == 2 and len(sorted_students) >= 3:
                rank_icon = "🥉"
            elif i == len(sorted_students) - 1 and len(sorted_students) >= 1:
                rank_icon = "🦓"

            ctk.CTkLabel(
                row,
                text=str(i+1),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=50
            ).grid(row=0, column=0, padx=5, sticky="ew")

            name_label = ctk.CTkLabel(
                row,
                text=f"{rank_icon} {student['name']}" if rank_icon else student["name"],
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=200,
                anchor="w" if self.lang == "ar" else "e"
            )
            name_label.grid(row=0, column=1, padx=5, sticky="ew")
            if rank_icon == "🥇":
                name_label.configure(cursor="hand2")
                name_label.bind("<Button-1>", lambda e: show_fireworks(self, self.lang))

            ctk.CTkLabel(
                row,
                text=str(total),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=100
            ).grid(row=0, column=2, padx=5, sticky="ew")

            ctk.CTkLabel(
                row,
                text=student.get("info", "")[:30] + ("..." if len(student.get("info", "")) > 30 else ""),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=300,
                anchor="w" if self.lang == "ar" else "e"
            ).grid(row=0, column=3, padx=5, sticky="ew")

            ctk.CTkButton(
                row,
                text="✏️ تعديل" if self.lang == "ar" else "✏️ Edit",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=100,
                command=lambda s=student: self.edit_student(s),
                fg_color="#0288D1",
                hover_color="#03A9F4",
                corner_radius=8
            ).grid(row=0, column=4, padx=5, sticky="ew")

        self.update_stats()

    def add_student(self):
        name = self.student_entry.get().strip()
        if name and re.match(r"^[a-zA-Z\sأ-ي]+$", name):
            if any(s["name"] == name for s in self.account["students"]):
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب موجود بالفعل." if self.lang == "ar" else "Student name already exists."
                )
                return
            self.account["students"].append({"name": name, "grades": [], "info": ""})
            self.student_entry.delete(0, "end")
            self.load_students()
            self.update_stats()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم إضافة الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} added successfully."
            )
        elif name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الاسم يجب أن يحتوي على حروف فقط." if self.lang == "ar" else "Name must contain letters only."
            )

    def remove_student(self):
        name = self.student_entry.get().strip()
        if name and any(s["name"] == name for s in self.account["students"]):
            self.account["students"] = [s for s in self.account["students"] if s["name"] != name]
            self.student_entry.delete(0, "end")
            self.load_students()
            self.update_stats()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حذف الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} removed successfully."
            )
        elif name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "اسم الطالب غير موجود." if self.lang == "ar" else "Student name not found."
            )

    def save_students(self):
        full_data = load_data()
        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                acc["students"] = self.account["students"]
                break
        save_data(full_data)
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            "تم حفظ قائمة الطلاب بنجاح ✅" if self.lang == "ar" else "Student list saved successfully ✅"
        )

    def restart_students(self):
        if messagebox.askyesno(
            "تأكيد" if self.lang == "ar" else "Confirm",
            "هل تريد إعادة بدء وتفريغ قائمة الطلاب؟" if self.lang == "ar" else "Do you want to restart and clear the student list?"
        ):
            self.account["students"] = []
            self.load_students()
            self.update_stats()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم تفريغ قائمة الطلاب بنجاح." if self.lang == "ar" else "Student list cleared successfully."
            )

    def edit_student(self, student):
        creation_date = datetime.strptime(self.account["created_at"], "%Y-%m-%d")
        if datetime.now() > creation_date + timedelta(days=EDIT_DAYS_LIMIT):
            messagebox.showinfo(
                "تنبيه" if self.lang == "ar" else "Alert",
                "انتهت فترة تعديل البيانات." if self.lang == "ar" else "Editing period has expired."
            )
            return

        popup = ctk.CTkToplevel(self)
        popup.title(f"تعديل بيانات {student['name']}" if self.lang == "ar" else f"Edit {student['name']} Data")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.7)
        popup.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
        popup.transient(self)
        popup.grab_set()

        edit_frame = ctk.CTkFrame(popup, corner_radius=10)
        edit_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            edit_frame,
            text="اسم الطالب:" if self.lang == "ar" else "Student Name:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)
        name_entry = ctk.CTkEntry(
            edit_frame,
            width=400,
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        name_entry.insert(0, student["name"])
        name_entry.pack(pady=10)

        ctk.CTkLabel(
            edit_frame,
            text="العلامات (مفصولة بمسافة):" if self.lang == "ar" else "Grades (space-separated):",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)
        grades_text = ctk.CTkEntry(
            edit_frame,
            width=400,
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        grades_text.insert(0, " ".join(map(str, student.get("grades", []))))
        grades_text.pack(pady=10)

        ctk.CTkLabel(
            edit_frame,
            text="ملاحظات:" if self.lang == "ar" else "Notes:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)
        info_entry = ctk.CTkTextbox(
            edit_frame,
            width=400,
            height=120,
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8
        )
        info_entry.insert("end", student.get("info", ""))
        info_entry.pack(pady=10)

        def save_changes():
            new_name = name_entry.get().strip()
            if new_name and re.match(r"^[a-zA-Z\sأ-ي]+$", new_name):
                student["name"] = new_name
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب غير صالح." if self.lang == "ar" else "Invalid student name."
                )
                return

            grades_str = grades_text.get().strip()
            if grades_str:
                try:
                    grades = list(map(int, grades_str.split()))
                    if any(g < 0 or g > MAX_GRADES for g in grades):
                        messagebox.showerror(
                            "خطأ" if self.lang == "ar" else "Error",
                            f"العلامات يجب أن تكون بين 0 و {MAX_GRADES}." if self.lang == "ar" else f"Grades must be between 0 and {MAX_GRADES}."
                        )
                        return
                    student["grades"] = grades
                except ValueError:
                    messagebox.showerror(
                        "خطأ" if self.lang == "ar" else "Error",
                        "يجب أن تكون العلامات أرقام صحيحة مفصولة بمسافة." if self.lang == "ar" else "Grades must be space-separated integers."
                    )
                    return
            else:
                student["grades"] = []

            student["info"] = info_entry.get("1.0", "end").strip()
            self.load_students()
            self.update_stats()
            popup.destroy()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم حفظ التغييرات بنجاح ✅" if self.lang == "ar" else "Changes saved successfully ✅"
            )

        ctk.CTkButton(
            edit_frame,
            text="💾 حفظ" if self.lang == "ar" else "💾 Save",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=save_changes,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        ).pack(pady=15)

    def back_to_manager(self):
        self.destroy()
        AccountManagerWindow(self.lang).mainloop()

    def export_to_excel(self):
        self.attributes("-disabled", True)
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Students"
            ws.append([
                "الاسم" if self.lang == "ar" else "Name",
                "العلامات" if self.lang == "ar" else "Grades",
                "المجموع" if self.lang == "ar" else "Total",
                "ملاحظات" if self.lang == "ar" else "Notes"
            ])

            for student in self.account["students"]:
                total = sum(student.get("grades", []))
                ws.append([
                    student["name"],
                    " ".join(map(str, student.get("grades", []))),
                    total,
                    student.get("info", "")
                ])

            wb.save("students_data.xlsx")
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم تصدير البيانات إلى ملف Excel بنجاح ✅" if self.lang == "ar" else "Data exported to Excel successfully ✅"
            )
        except PermissionError:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الملف مفتوح في برنامج آخر. أغلق الملف وحاول مجدداً." if self.lang == "ar" else "File is open in another program. Close it and try again."
            )
        except Exception as e:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                f"حدث خطأ أثناء التصدير: {str(e)}" if self.lang == "ar" else f"Error during export: {str(e)}"
            )
        finally:
            self.attributes("-disabled", False)

# ============================================================
# 🟢 تشغيل التطبيق
# ============================================================
if __name__ == "__main__":
    data = load_data()
    if not data["accounts"]:
        CreateAccountWindow().mainloop()
    else:
        AccountManagerWindow().mainloop()
