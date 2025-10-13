# استيراد المكتبات الضرورية
import tkinter as tk
from tkinter import messagebox
import math

# إنشاء نافذة رئيسية
root = tk.Tk()
root.title("حساب محيط ومساحة الدائرة")  # عنوان النافذة
root.geometry("400x300")  # حجم النافذة

# دالة لحساب المحيط والمساحة
def حساب_المحيط_والمساحة():
    try:
        # الحصول على قيمة نصف القطر من المدخل النصي
        نصف_القطر = float(entry_radius.get())
        
        if نصف_القطر <= 0:
            raise ValueError("نصف القطر يجب أن يكون أكبر من صفر.")
        
        # حساب المحيط (2 * π * نصف القطر)
        المحيط = 2 * math.pi * نصف_القطر
        
        # حساب المساحة (π * نصف القطر^2)
        المساحة = math.pi * (نصف_القطر ** 2)
        
        # عرض النتيجة للمستخدم
        label_result.config(text=f"المحيط: {المحيط:.2f}\nالمساحة: {المساحة:.2f}")
    
    except ValueError as e:
        # في حال وجود خطأ في الإدخال
        messagebox.showerror("خطأ", "يرجى إدخال قيمة صحيحة لنصف القطر.")
        
# إنشاء مكونات الواجهة
label_radius = tk.Label(root, text="أدخل نصف القطر:", font=("Arial", 14))
label_radius.pack(pady=10)

entry_radius = tk.Entry(root, font=("Arial", 14))
entry_radius.pack(pady=10)

# زر لحساب المحيط والمساحة
button_calculate = tk.Button(root, text="حساب", font=("Arial", 14), command=حساب_المحيط_والمساحة)
button_calculate.pack(pady=20)

# لعرض النتيجة
label_result = tk.Label(root, text="المحيط: 0\nالمساحة: 0", font=("Arial", 14))
label_result.pack(pady=20)

# تشغيل البرنامج
root.mainloop()
