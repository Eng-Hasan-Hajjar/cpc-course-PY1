# تعليق: استيراد المكتبات الضرورية للتطبيق
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, Menu
import json
import os
from datetime import datetime

# تعليق: تعريف مسار ملف حفظ البيانات
DATA_FILE = "student_grades.json"
# تعليق: تعريف مسار ملف حفظ الإعدادات (ثيم فقط الآن)
SETTINGS_FILE = "app_settings.json"
# تعليق: مسار الأيقونة (استبدل بالمسار الفعلي إذا لزم الأمر)
ICON_PATH = r"D:\CPC-PY.1\Student grades\education_test_grade_assigment_icon_209591 (1).ico"

# تعليق: قاموس الترجمات للغة الإنجليزية فقط
TRANSLATIONS = {
    "en": {
        "app_title": "Student Grades",
        "add_student": "Add Student",
        "edit_student": "Edit Student",
        "delete_student": "Delete Student",
        "student_name": "Student Name",
        "grades": "Grades",
        "add_grade": "Add Grade",
        "grade_value": "Grade Value",
        "total_grades": "Total Grades",
        "reset_app": "Reset App",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "developed_by": "Developed by Programmer Marcel Soufi using Python",
        "email": "yousefsoufi2@gmail.com",
        "back": "Back",
        "confirm_delete_student": "Delete this student?",
        "confirm_reset": "Reset all data?",
        "error_invalid_grade": "Invalid grade value",
        "confirm_title": "Confirm",
        "error_title": "Error",
        "edit_grade": "Edit Grade",
        "delete_grade": "Delete Grade",
        "confirm_delete_grade": "Delete this grade?"
    }
}

# تعليق: دالة لتحميل البيانات من الملف
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"students": {}}

# تعليق: دالة لحفظ البيانات في الملف
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تعليق: دالة لتحميل الإعدادات (ثيم فقط)
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"theme": "dark"}

# تعليق: دالة لحفظ الإعدادات
def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

# تعليق: كلاس التطبيق الرئيسي
class StudentGradesApp:
    def __init__(self):
        # تعليق: تحميل الإعدادات (ثيم فقط)
        self.settings = load_settings()
        self.theme = self.settings["theme"]
        self.language = "en"  # اللغة الافتراضية الإنجليزية
        
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme("blue")  # ثيم احترافي
        
        self.root = ctk.CTk()
        self.root.title(TRANSLATIONS[self.language]["app_title"])
        if os.path.exists(ICON_PATH):
            self.root.iconbitmap(ICON_PATH)
        
        # تعليق: جعل النافذة تفتح في منتصف الشاشة
        width = 800
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self.data = load_data()
        self.students = self.data["students"]
        
        # تعليق: إنشاء الواجهات
        self.create_main_frame()
        self.create_grade_frame()
        
        # تعليق: عرض الواجهة الرئيسية أولاً
        self.show_frame("main")
        
        # تعليق: إضافة label المتطور في الأسفل مع حدث النقر لعرض الإيميل وتغيير المؤشر عند الهوفر
        self.developed_label = ctk.CTkLabel(self.root, text=TRANSLATIONS[self.language]["developed_by"], font=("Arial", 10, "italic"), cursor="hand2")
        self.developed_label.pack(side="bottom", pady=5)
        self.developed_label.bind("<Button-1>", lambda e: self.show_email())
        
        self.root.mainloop()

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # تعليق: قائمة الطلاب (استخدام Listbox لعرض قائمة)
        self.student_list = tk.Listbox(self.main_frame, font=("Arial", 14))
        self.student_list.pack(fill="both", expand=True, padx=20, pady=20)
        self.student_list.bind("<<ListboxSelect>>", self.show_student_grades)
        self.update_student_list()
        
        # تعليق: أزرار إضافة، تعديل، حذف بتصميم دائري
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)
        
        self.add_button = ctk.CTkButton(button_frame, text=TRANSLATIONS[self.language]["add_student"], command=self.add_student, corner_radius=32, width=120)
        self.add_button.grid(row=0, column=0, padx=10)
        
        self.edit_button = ctk.CTkButton(button_frame, text=TRANSLATIONS[self.language]["edit_student"], command=self.edit_student, corner_radius=32, width=120)
        self.edit_button.grid(row=0, column=1, padx=10)
        
        self.delete_button = ctk.CTkButton(button_frame, text=TRANSLATIONS[self.language]["delete_student"], command=self.delete_student, corner_radius=32, width=120)
        self.delete_button.grid(row=0, column=2, padx=10)
        
        # تعليق: خيارات الثيم فقط
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(pady=10)
        
        self.theme_label = ctk.CTkLabel(settings_frame, text=TRANSLATIONS[self.language]["dark_mode"] if self.theme == "dark" else TRANSLATIONS[self.language]["light_mode"])
        self.theme_label.grid(row=0, column=0, padx=10)
        
        self.theme_switch = ctk.CTkSwitch(settings_frame, command=self.toggle_theme, text="")
        self.theme_switch.grid(row=0, column=1, padx=10)
        if self.theme == "dark":
            self.theme_switch.select()
        
        # تعليق: زر التصفير
        self.reset_button = ctk.CTkButton(self.main_frame, text=TRANSLATIONS[self.language]["reset_app"], command=self.reset_app, corner_radius=32, fg_color="red")
        self.reset_button.pack(pady=20)

    def create_grade_frame(self):
        self.grade_frame = ctk.CTkFrame(self.root)
        
        # تعليق: إضافة اسم الطالب في الأعلى
        self.student_name_label = ctk.CTkLabel(self.grade_frame, text="", font=("Arial", 20, "bold"))
        self.student_name_label.pack(pady=10)
        
        self.back_button = ctk.CTkButton(self.grade_frame, text=TRANSLATIONS[self.language]["back"], command=lambda: self.show_frame("main"), corner_radius=32)
        self.back_button.pack(pady=10)
        
        self.grade_list = tk.Listbox(self.grade_frame, font=("Arial", 12))
        self.grade_list.pack(fill="both", expand=True, padx=20, pady=20)
        self.grade_list.bind("<Button-3>", self.show_grade_menu)  # bind right-click for menu
        
        self.total_label = ctk.CTkLabel(self.grade_frame, text="", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)
        
        add_grade_frame = ctk.CTkFrame(self.grade_frame)
        add_grade_frame.pack(pady=10)
        
        self.grade_entry = ctk.CTkEntry(add_grade_frame, placeholder_text=TRANSLATIONS[self.language]["grade_value"], corner_radius=20)
        self.grade_entry.grid(row=0, column=0, padx=10)
        
        self.add_grade_button = ctk.CTkButton(add_grade_frame, text=TRANSLATIONS[self.language]["add_grade"], command=self.add_grade, corner_radius=32)
        self.add_grade_button.grid(row=0, column=1, padx=10)

    def show_frame(self, frame_name):
        if frame_name == "main":
            self.grade_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
        else:
            self.main_frame.pack_forget()
            self.grade_frame.pack(fill="both", expand=True)

    def update_student_list(self):
        self.student_list.delete(0, tk.END)
        for student in sorted(self.students.keys()):
            self.student_list.insert(tk.END, student)

    def add_student(self):
        name = self.prompt_input(TRANSLATIONS[self.language]["student_name"])
        if name and name not in self.students:
            self.students[name] = []
            self.update_student_list()
            self.save_data()

    def edit_student(self):
        selected = self.student_list.curselection()
        if selected:
            old_name = self.student_list.get(selected[0])
            new_name = self.prompt_input(TRANSLATIONS[self.language]["student_name"], old_name)
            if new_name and new_name != old_name:
                self.students[new_name] = self.students.pop(old_name)
                self.update_student_list()
                self.save_data()

    def delete_student(self):
        selected = self.student_list.curselection()
        if selected:
            name = self.student_list.get(selected[0])
            if messagebox.askyesno(TRANSLATIONS[self.language]["confirm_title"], TRANSLATIONS[self.language]["confirm_delete_student"]):
                del self.students[name]
                self.update_student_list()
                self.save_data()

    def show_student_grades(self, event):
        selected = self.student_list.curselection()
        if selected:
            self.current_student = self.student_list.get(selected[0])
            self.student_name_label.configure(text=self.current_student)
            self.show_frame("grades")
            self.update_grade_list()

    def update_grade_list(self):
        self.grade_list.delete(0, tk.END)
        total = 0
        for grade in self.students[self.current_student]:
            value, date = grade["value"], grade["date"]
            self.grade_list.insert(tk.END, f"{value} - {date}")
            total += value
        self.total_label.configure(text=f"{TRANSLATIONS[self.language]['total_grades']}: {total}")

    def add_grade(self):
        try:
            value = float(self.grade_entry.get())
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.students[self.current_student].append({"value": value, "date": date})
            self.update_grade_list()
            self.grade_entry.delete(0, tk.END)
            self.save_data()
        except ValueError:
            messagebox.showerror(TRANSLATIONS[self.language]["error_title"], TRANSLATIONS[self.language]["error_invalid_grade"])

    def show_grade_menu(self, event):
        selected = self.grade_list.curselection()
        if selected:
            self.selected_grade_index = selected[0]
            menu = Menu(self.root, tearoff=0)
            menu.add_command(label=TRANSLATIONS[self.language]["edit_grade"], command=self.edit_grade)
            menu.add_command(label=TRANSLATIONS[self.language]["delete_grade"], command=self.delete_grade)
            menu.post(event.x_root, event.y_root)

    def edit_grade(self):
        current_grade = self.students[self.current_student][self.selected_grade_index]
        new_value = self.prompt_input(TRANSLATIONS[self.language]["grade_value"], str(current_grade["value"]))
        try:
            self.students[self.current_student][self.selected_grade_index]["value"] = float(new_value)
            self.students[self.current_student][self.selected_grade_index]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تحديث التاريخ
            self.update_grade_list()
            self.save_data()
        except ValueError:
            messagebox.showerror(TRANSLATIONS[self.language]["error_title"], TRANSLATIONS[self.language]["error_invalid_grade"])

    def delete_grade(self):
        if messagebox.askyesno(TRANSLATIONS[self.language]["confirm_title"], TRANSLATIONS[self.language]["confirm_delete_grade"]):
            del self.students[self.current_student][self.selected_grade_index]
            self.update_grade_list()
            self.save_data()

    def reset_app(self):
        if messagebox.askyesno(TRANSLATIONS[self.language]["confirm_title"], TRANSLATIONS[self.language]["confirm_reset"]):
            self.students.clear()
            self.update_student_list()
            self.save_data()

    def toggle_theme(self):
        self.theme = "dark" if self.theme_switch.get() else "light"
        ctk.set_appearance_mode(self.theme)
        self.settings["theme"] = self.theme
        save_settings(self.settings)
        self.theme_label.configure(text=TRANSLATIONS[self.language]["dark_mode"] if self.theme == "dark" else TRANSLATIONS[self.language]["light_mode"])

    def prompt_input(self, title, default=""):
        dialog = ctk.CTkInputDialog(text=title, title=title)
        input_value = dialog.get_input()
        return input_value if input_value else default

    def show_email(self):
        messagebox.showinfo("Contact", TRANSLATIONS[self.language]["email"])

    def save_data(self):
        self.data["students"] = self.students
        save_data(self.data)

# تعليق: تشغيل التطبيق
if __name__ == "__main__":
    app = StudentGradesApp()