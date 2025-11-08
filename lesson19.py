#lesson19
import tkinter as tk

# إنشاء النافذة الرئيسية
window = tk.Tk()
window.title("برنامجي الأول")
window.geometry("300x200")

# دالة تُنفّذ عند الضغط على الزر
def on_button_click():
    label.config(text="مرحبا! لقد ضغطت على الزر 😊")

# إضافة تسمية (label)
label = tk.Label(window, text="اضغط الزر أدناه", font=("Arial", 42))
label.pack(pady=20)

# إضافة زر
button = tk.Button(window, text="اضغط هنا", command=on_button_click, font=("Arial", 42))
button.pack(padx=40,pady=100)

# تشغيل النافذة
window.mainloop()