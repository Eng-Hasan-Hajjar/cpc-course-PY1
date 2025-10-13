import tkinter as tk
from tkinter import ttk, messagebox
import math

# دالة لحساب المساحة والمحيط حسب نوع المثلث
def calculate():
    triangle_type = triangle_type_var.get()

    try:
        if triangle_type == "متساوي الأضلاع":
            a = float(entry_a.get())
            perimeter = 3 * a
            area = (math.sqrt(3) / 4) * (a ** 2)

        elif triangle_type == "متساوي الساقين":
            a = float(entry_a.get())
            b = float(entry_b.get())
            perimeter = 2 * a + b
            height = math.sqrt(a * 2 - (b / 2) * 2)
            area = 0.5 * b * height

        elif triangle_type == "مختلف الأضلاع":
            a = float(entry_a.get())
            b = float(entry_b.get())
            c = float(entry_c.get())
            s = (a + b + c) / 2  # نصف المحيط
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))
            perimeter = a + b + c

        elif triangle_type == "قائم الزاوية":
            a = float(entry_a.get())
            b = float(entry_b.get())
            hypotenuse = math.sqrt(a * 2 + b * 2)
            perimeter = a + b + hypotenuse
            area = 0.5 * a * b

        else:
            messagebox.showwarning("تحذير", "الرجاء اختيار نوع المثلث.")
            return

        # عرض النتائج
        label_result.config(text=f"المحيط = {perimeter:.2f}\nالمساحة = {area:.2f}")

    except ValueError:
        messagebox.showerror("خطأ", "الرجاء إدخال قيم صحيحة للأضلاع.")

# دالة لتحديث الحقول حسب نوع المثلث
def update_fields(event=None):
    triangle_type = triangle_type_var.get()

    # إخفاء كل الحقول أولاً
    for widget in [label_b, entry_b, label_c, entry_c]:
        widget.grid_remove()

    # إظهار الحقول اللازمة فقط
    if triangle_type == "متساوي الأضلاع":
        label_a.config(text="طول الضلع:")
        entry_a.grid(row=2, column=1, padx=5, pady=5)
    elif triangle_type == "متساوي الساقين":
        label_a.config(text="طول الساق:")
        label_b.config(text="طول القاعدة:")
        label_b.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_b.grid(row=3, column=1, padx=5, pady=5)
    elif triangle_type == "مختلف الأضلاع":
        label_a.config(text="الضلع الأول:")
        label_b.config(text="الضلع الثاني:")
        label_c.config(text="الضلع الثالث:")
        label_b.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_b.grid(row=3, column=1, padx=5, pady=5)
        label_c.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        entry_c.grid(row=4, column=1, padx=5, pady=5)
    elif triangle_type == "قائم الزاوية":
        label_a.config(text="الضلع الأول:")
        label_b.config(text="الضلع الثاني:")
        label_b.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        entry_b.grid(row=3, column=1, padx=5, pady=5)

# إنشاء نافذة البرنامج
root = tk.Tk()
root.title("حساب محيط ومساحة المثلث")
root.geometry("420x400")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

# العنوان الرئيسي
title_label = tk.Label(root, text="برنامج حساب مساحة ومحيط المثلث", font=("Tajawal", 16, "bold"), bg="#f2f2f2", fg="#333")
title_label.pack(pady=15)

# الإطار الأساسي
frame = ttk.Frame(root, padding=15)
frame.pack(padx=10, pady=10, fill="x")

# اختيار نوع المثلث
triangle_type_var = tk.StringVar()
label_type = ttk.Label(frame, text="اختر نوع المثلث:")
label_type.grid(row=0, column=0, sticky="e", padx=5, pady=5)

combo_type = ttk.Combobox(frame, textvariable=triangle_type_var, state="readonly",
                          values=["متساوي الأضلاع", "متساوي الساقين", "مختلف الأضلاع", "قائم الزاوية"])
combo_type.grid(row=0, column=1, padx=5, pady=5)
combo_type.bind("<<ComboboxSelected>>", update_fields)

# إدخال الأضلاع
label_a = ttk.Label(frame, text="الضلع:")
label_a.grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_a = ttk.Entry(frame)
entry_a.grid(row=2, column=1, padx=5, pady=5)

label_b = ttk.Label(frame, text="الضلع 2:")
entry_b = ttk.Entry(frame)

label_c = ttk.Label(frame, text="الضلع 3:")
entry_c = ttk.Entry(frame)

# زر الحساب
btn_calc = tk.Button(root, text="احسب", command=calculate, bg="#4CAF50", fg="white", font=("Tajawal", 12, "bold"), width=15)
btn_calc.pack(pady=10)

# خانة عرض النتيجة
label_result = tk.Label(root, text="", bg="#f2f2f2", fg="#000", font=("Tajawal", 14))
label_result.pack(pady=15)

# تذييل
footer = tk.Label(root, text="تصميم بواسطة مارسيل + Tkinter", bg="#f2f2f2", fg="#777", font=("Tajawal", 9))
footer.pack(side="bottom", pady=5)

root.mainloop()