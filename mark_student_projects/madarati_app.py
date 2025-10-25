import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import re

# ------------------------------
# إعداد قاعدة البيانات (SQLite)
# ------------------------------
DB_FILE = 'students_grades.db'

# إنشاء/فتح قاعدة البيانات والجدول إذا لم يكن موجوداً
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    institute TEXT,
    grade TEXT,
    reason TEXT,
    date_added TEXT
)
''')
conn.commit()

# ------------------------------
# واجهة المستخدم باستخدام Tkinter
# ------------------------------

class StudentGradesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # إعدادات النافذة
        self.title('تطبيق علامات الطلاب                            RED SULFUR بواسطة')
        self.geometry('950x600')
        self.minsize(820, 520)

        # ألوان عصرية
        self.primary_bg = "#094cb8"       # خلفية داكنة
        self.card_bg = "#120738"          # لون بطاقة الجدول
        self.accent = "#ed3a3a"           # لون مميز أرجواني
        self.text_color = '#e6eef8'       # لون نص فاتح

        self.configure(bg=self.primary_bg)

        # تكوين ستايل لـ ttk
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview',
                        background=self.card_bg,
                        foreground=self.text_color,
                        fieldbackground=self.card_bg,
                        rowheight=28,
                        font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', self.accent)])

        style.configure('TLabel', background=self.primary_bg, foreground=self.text_color, font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground="#444444", foreground=self.text_color)
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('Accent.TButton', background=self.accent, foreground='white')

        # إنشاء واجهة رئيسية
        self.create_widgets()
        # تحميل البيانات من القاعدة
        self.load_data()

    def create_widgets(self):
        # إطار الإدخال مع تصميم أكثر وضوحًا: كل تسمية بجانب حقلها
        input_frame = ttk.Frame(self, padding=(14,12,14,6), style='TFrame')
        input_frame.pack(fill='x')

        # ضبط شبكة الأعمدة لجعل التخطيط مرن
        for i in range(4):
            input_frame.columnconfigure(i, weight=1)

        # صف 0: اسم الطالب و المعهد
        ttk.Label(input_frame, text='اسم الطالب:').grid(row=0, column=0, sticky='e', padx=(0,6))
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var)
        # محاذاة نص الإدخال إلى اليمين للغة العربية
        self.name_entry.configure(justify='right')
        self.name_entry.grid(row=0, column=1, padx=6, pady=6, sticky='we')

        ttk.Label(input_frame, text='المعهد:').grid(row=0, column=2, sticky='e', padx=(0,6))
        self.institute_var = tk.StringVar()
        self.institute_entry = ttk.Entry(input_frame, textvariable=self.institute_var)
        self.institute_entry.configure(justify='right')
        self.institute_entry.grid(row=0, column=3, padx=6, pady=6, sticky='we')

        # صف 1: العلامات و السبب
        ttk.Label(input_frame, text='العلامات المضافة:').grid(row=1, column=0, sticky='e', padx=(0,6))
        self.grade_var = tk.StringVar()
        self.grade_entry = ttk.Entry(input_frame, textvariable=self.grade_var)
        self.grade_entry.configure(justify='right')
        self.grade_entry.grid(row=1, column=1, padx=6, pady=6, sticky='we')

        ttk.Label(input_frame, text='السبب:').grid(row=1, column=2, sticky='e', padx=(0,6))
        self.reason_var = tk.StringVar()
        self.reason_entry = ttk.Entry(input_frame, textvariable=self.reason_var)
        self.reason_entry.configure(justify='right')
        self.reason_entry.grid(row=1, column=3, padx=6, pady=6, sticky='we')

        # صف 2: تاريخ و أزرار
        ttk.Label(input_frame, text='تاريخ الإضافة (YYYY-MM-DD):').grid(row=2, column=0, sticky='e', padx=(0,6))
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.date_entry = ttk.Entry(input_frame, textvariable=self.date_var)
        self.date_entry.configure(justify='right')
        self.date_entry.grid(row=2, column=1, padx=6, pady=8, sticky='we')

        # أزرار
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=3, sticky='e')

        self.add_btn = ttk.Button(btn_frame, text='إضافة سجل', command=self.add_record, style='Accent.TButton')
        self.add_btn.pack(side='left', padx=6)

        self.update_btn = ttk.Button(btn_frame, text='تعديل محدد', command=self.update_record)
        self.update_btn.pack(side='left', padx=6)

        self.delete_btn = ttk.Button(btn_frame, text='حذف محدد', command=self.delete_record)
        self.delete_btn.pack(side='left', padx=6)

        # شريط بحث و تصدير
        search_frame = ttk.Frame(self, padding=(12,6))
        search_frame.pack(fill='x')
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text='بحث سريع:').grid(row=0, column=0, sticky='w')
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search_changed)
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.configure(justify='right')
        self.search_entry.grid(row=0, column=1, padx=6, sticky='we')

        self.export_btn = ttk.Button(search_frame, text='تصدير CSV', command=self.export_csv)
        self.export_btn.grid(row=0, column=2, sticky='e')

        # إطار الجدول
        table_frame = ttk.Frame(self, padding=(12,6))
        table_frame.pack(fill='both', expand=True)

        # إعداد Treeview (الجدول) مع ترتيب أعمدة واضح
        columns = ('student_name', 'institute', 'grade', 'reason', 'date_added')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # رؤوس الأعمدة
        self.tree.heading('student_name', text='اسم الطالب')
        self.tree.heading('institute', text='المعهد')
        self.tree.heading('grade', text='العلامات المضافة')
        self.tree.heading('reason', text='السبب')
        self.tree.heading('date_added', text='تاريخ الإضافة')

        # عرض الأعمدة ومواضعها لضمان التطابق مع القيم
        self.tree.column('student_name', width=230, anchor='w')
        self.tree.column('institute', width=150, anchor='w')
        self.tree.column('grade', width=120, anchor='center')
        self.tree.column('reason', width=250, anchor='w')
        self.tree.column('date_added', width=120, anchor='center')

        # ربط حدث اختيار السطر
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # إضافة شريط تمرير
        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

    # ------------------------------------
    # وظائف CRUD
    # ------------------------------------

    def validate_date(self, date_text):
        # تحقق بسيط لصيغة التاريخ YYYY-MM-DD
        if not date_text:
            return False
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_text))

    def add_record(self):
        # جلب القيم من الحقول
        name = self.name_var.get().strip()
        institute = self.institute_var.get().strip()
        grade = self.grade_var.get().strip()
        reason = self.reason_var.get().strip()
        date_added = self.date_var.get().strip()

        # تحقق أساسي من صحة البيانات
        if not name:
            messagebox.showwarning('حقل ناقص', 'الرجاء إدخال اسم الطالب.')
            return
        if not date_added or not self.validate_date(date_added):
            # إذا كان التاريخ غير صالح، نعطي التاريخ الحالي تلقائيًا
            date_added = datetime.now().strftime('%Y-%m-%d')

        # إدخال في قاعدة البيانات
        try:
            c.execute('INSERT INTO grades (student_name, institute, grade, reason, date_added) VALUES (?, ?, ?, ?, ?)',
                      (name, institute, grade, reason, date_added))
            conn.commit()
        except Exception as e:
            messagebox.showerror('خطأ', f'حدث خطأ أثناء الحفظ: {e}')
            return

        # تحديث الجدول في الواجهة
        self.load_data()
        self.clear_inputs()

    def load_data(self, filter_text=None):
        # مسح كل صفوف الـ Treeview
        for r in self.tree.get_children():
            self.tree.delete(r)

        # جلب السجلات من قاعدة البيانات
        if filter_text:
            filter_like = f'%{filter_text}%'
            c.execute('SELECT id, student_name, institute, grade, reason, date_added FROM grades WHERE student_name LIKE ? OR institute LIKE ? OR grade LIKE ? OR reason LIKE ? ORDER BY date_added DESC',
                      (filter_like, filter_like, filter_like, filter_like))
        else:
            c.execute('SELECT id, student_name, institute, grade, reason, date_added FROM grades ORDER BY date_added DESC')

        rows = c.fetchall()
        # إضافة الصفوف إلى Treeview مع ضمان تطابق القيم مع رؤوس الأعمدة
        for row in rows:
            rid, student_name, institute, grade, reason, date_added = row
            # حفظ id في "iid" حتى نتمكن من التعامل مع السجل لاحقًا
            self.tree.insert('', 'end', iid=str(rid), values=(student_name, institute, grade, reason, date_added))

    def on_tree_select(self, event):
        # عند اختيار صف، نُملأ الحقول للتعديل
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        values = self.tree.item(item_id, 'values')
        # ترتيب القيم كما في الأعمدة: تأكدنا أن الترتيب ثابت
        try:
            self.name_var.set(values[0])
            self.institute_var.set(values[1])
            self.grade_var.set(values[2])
            self.reason_var.set(values[3])
            self.date_var.set(values[4])
        except Exception:
            # إذا حدث أي اختلاف في الطول، نفرغ الحقول لتجنب الارتباك
            self.clear_inputs()

    def update_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('لم يتم التحديد', 'الرجاء اختيار سجل من الجدول لتعديله.')
            return
        item_id = selected[0]

        # جلب القيم المحدثة
        name = self.name_var.get().strip()
        institute = self.institute_var.get().strip()
        grade = self.grade_var.get().strip()
        reason = self.reason_var.get().strip()
        date_added = self.date_var.get().strip()

        if not name:
            messagebox.showwarning('حقل ناقص', 'الرجاء إدخال اسم الطالب.')
            return
        if not date_added or not self.validate_date(date_added):
            date_added = datetime.now().strftime('%Y-%m-%d')

        try:
            c.execute('UPDATE grades SET student_name=?, institute=?, grade=?, reason=?, date_added=? WHERE id=?',
                      (name, institute, grade, reason, date_added, item_id))
            conn.commit()
        except Exception as e:
            messagebox.showerror('خطأ', f'حدث خطأ أثناء التعديل: {e}')
            return

        self.load_data()
        self.clear_inputs()

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('لم يتم التحديد', 'الرجاء اختيار سجل من الجدول للحذف.')
            return
        item_id = selected[0]
        confirm = messagebox.askyesno('تأكيد الحذف', 'هل أنت متأكد من حذف السجل المحدد؟')
        if not confirm:
            return
        try:
            c.execute('DELETE FROM grades WHERE id=?', (item_id,))
            conn.commit()
        except Exception as e:
            messagebox.showerror('خطأ', f'حدث خطأ أثناء الحذف: {e}')
            return
        self.load_data()
        self.clear_inputs()

    def clear_inputs(self):
        # إعادة تعيين الحقول والبحث
        self.name_var.set('')
        self.institute_var.set('')
        self.grade_var.set('')
        self.reason_var.set('')
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
        try:
            self.tree.selection_remove(self.tree.selection())
        except Exception:
            pass

    def on_search_changed(self, *args):
        q = self.search_var.get().strip()
        if q:
            self.load_data(filter_text=q)
        else:
            self.load_data()

    def export_csv(self):
        # تصدير البيانات الحالية إلى ملف CSV
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], title='حفظ CSV')
        if not file_path:
            return
        try:
            # جلب كل السجلات
            c.execute('SELECT student_name, institute, grade, reason, date_added FROM grades ORDER BY date_added DESC')
            rows = c.fetchall()
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['اسم الطالب', 'المعهد', 'العلامات المضافة', 'السبب', 'تاريخ الإضافة'])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo('تم', 'تم تصدير البيانات بنجاح.')
        except Exception as e:
            messagebox.showerror('خطأ', f'حدث خطأ أثناء التصدير: {e}')

# ------------------------------------
# تشغيل التطبيق
# ------------------------------------
if __name__ == '__main__':
    app = StudentGradesApp()
    app.mainloop()

# إغلاق اتصال قاعدة البيانات بعد انتهاء التطبيق
conn.close()