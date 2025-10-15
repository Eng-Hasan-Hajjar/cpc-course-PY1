import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import json
import os

# =====================
# Daily Task Manager
# =====================
# English variable names, Arabic comments
# نافذة بحجم آلة حاسبة (تقريباً) وقابلة للتكبير

APP_TITLE = "مدير المهام اليومية"
DEFAULT_WIDTH = 320
DEFAULT_HEIGHT = 480
DATA_FILE = "tasks.json"

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # إعداد نافذة التطبيق
        self.title(APP_TITLE)
        self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
        self.minsize(280, 380)  # أصغر حجم معقول

        # قائمة المهام
        self.tasks = []  # ستحتوي على قواميس: {'text': str, 'done': bool}

        # أنشئ واجهة المستخدم
        self._setup_style()
        self._create_widgets()
        self._load_tasks()

    def _setup_style(self):
        # إعداد مظهر عصري باستخدام ttk
        style = ttk.Style(self)
        # استخدم النمط الافتراضي ولكن مع تحسينات
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TButton', font=('Segoe UI', 11))
        style.configure('TLabel', font=('Segoe UI', 11))
        style.configure('Header.TLabel', font=('Segoe UI', 13, 'bold'))

    def _create_widgets(self):
        # الحاوية الرئيسية - استخدام grid لمرونة التكبير
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # رأس الواجهة
        header = ttk.Label(self, text=APP_TITLE, style='Header.TLabel', anchor='center')
        header.grid(row=0, column=0, sticky='ew', padx=10, pady=(10,5))

        # إطار لإضافة مهمة جديدة
        add_frame = ttk.Frame(self)
        add_frame.grid(row=1, column=0, sticky='new', padx=10, pady=(0,8))
        add_frame.columnconfigure(0, weight=1)

        # مدخل النص
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(add_frame, textvariable=self.entry_var, font=('Segoe UI', 11))
        entry.grid(row=0, column=0, sticky='ew', padx=(0,8))
        entry.bind('<Return>', lambda e: self.add_task())  # اضغط Enter لإضافة

        # زر إضافة
        add_btn = ttk.Button(add_frame, text='أضف مهمة', command=self.add_task)
        add_btn.grid(row=0, column=1, sticky='e')

        # إطار لقائمة المهام مع شريط تمرير
        list_frame = ttk.Frame(self)
        list_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(0,8))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # استخدام Canvas + Frame لعمل قائمة قابلة للتمرير وبعناصر قابلة للتخصيص
        self.canvas = tk.Canvas(list_frame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.tasks_container = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.tasks_container, anchor='nw')
        self.tasks_container.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # التحكمات السفلية: حذف، تحرير، حفظ، تحميل
        controls = ttk.Frame(self)
        controls.grid(row=3, column=0, sticky='ew', padx=10, pady=(0,10))
        controls.columnconfigure((0,1,2,3), weight=1)

        self.delete_btn = ttk.Button(controls, text='حذف المحدد', command=self.delete_selected)
        self.delete_btn.grid(row=0, column=0, sticky='ew', padx=4)

        self.edit_btn = ttk.Button(controls, text='تعديل', command=self.edit_selected)
        self.edit_btn.grid(row=0, column=1, sticky='ew', padx=4)

        self.save_btn = ttk.Button(controls, text='حفظ', command=self.save_tasks)
        self.save_btn.grid(row=0, column=2, sticky='ew', padx=4)

        self.load_btn = ttk.Button(controls, text='تحميل', command=self._load_tasks_from_dialog)
        self.load_btn.grid(row=0, column=3, sticky='ew', padx=4)

        # ملصق حالة
        self.status_var = tk.StringVar(value='')
        status_label = ttk.Label(self, textvariable=self.status_var, anchor='w')
        status_label.grid(row=4, column=0, sticky='ew', padx=10)

        # استكمال ضبط السلوكيات المتعلقة بالتمرير
        self.bind('<Configure>', lambda e: self._on_resize())

    def _on_resize(self):
        # ضبط عرض قماش العناصر بحيث يناسب العرض الحالي
        width = self.winfo_width() - 40
        if width > 50:
            self.canvas.itemconfigure(1, width=width)

    # ------------------ وظائف المهام ------------------
    def add_task(self):
        # إضافة مهمة جديدة من مدخل النص
        text = self.entry_var.get().strip()
        if not text:
            self.status_var.set('اكتب نص المهمة أولاً')
            return
        new_task = {'text': text, 'done': False}
        self.tasks.append(new_task)
        self.entry_var.set('')
        self._refresh_tasks_view()
        self.status_var.set('تمت إضافة المهمة')

    def _refresh_tasks_view(self):
        # إعادة رسم قائمة المهام داخل الإطار القابل للتمرير
        for child in self.tasks_container.winfo_children():
            child.destroy()

        for index, task in enumerate(self.tasks):
            self._create_task_row(index, task)

    def _create_task_row(self, index, task):
        # صف يمثل مهمة واحدة: زر لتبديل الإنجاز، تسـمية للنص، وخيارات حدف
        row = ttk.Frame(self.tasks_container, padding=(6,4))
        row.grid(row=index, column=0, sticky='ew', pady=2)
        row.columnconfigure(1, weight=1)

        # زر الانجاز (نص عربي يوضح الحالة)
        done_text = 'تم' if task['done'] else 'قيد الانتظار'
        done_btn = ttk.Button(row, text=done_text, width=10, command=lambda i=index: self.toggle_done(i))
        done_btn.grid(row=0, column=0, sticky='w')

        # نص المهمة - يمكن النقر عليه لتحديده أو التعديل
        font_style = ('Segoe UI', 11, 'overstrike') if task['done'] else ('Segoe UI', 11)
        task_label = ttk.Label(row, text=task['text'], font=font_style, anchor='e')
        task_label.grid(row=0, column=1, sticky='ew', padx=(8,8))
        task_label.bind('<Button-1>', lambda e, i=index: self._on_task_click(i))
        task_label.bind('<Double-Button-1>', lambda e, i=index: self.edit_task(i))

        # زر حذف صغير على اليمين
        del_btn = ttk.Button(row, text='حذف', width=7, command=lambda i=index: self.delete_task(i))
        del_btn.grid(row=0, column=2, sticky='e')

    def _on_task_click(self, index):
        # عند النقر على مهمة: نحددها بصرياً (نغير لون الخلفية مؤقتاً)
        # ملاحظة: هنا نستخدم تغيير الحالة البسيط في status
        self.status_var.set(f'المهمة المحددة: {self.tasks[index]["text"]}')

    def toggle_done(self, index):
        # تبديل حالة الإنجاز للمهمة
        self.tasks[index]['done'] = not self.tasks[index]['done']
        self._refresh_tasks_view()
        self.status_var.set('تم تحديث حالة المهمة')

    def delete_task(self, index):
        # حذف مهمة محددة
        if messagebox.askyesno('تأكيد', 'هل تريد حذف هذه المهمة؟'):
            del self.tasks[index]
            self._refresh_tasks_view()
            self.status_var.set('تم حذف المهمة')

    def delete_selected(self):
        # حذف المهمة الأولى التي تحتوي على كلمة البحث (كمثال على اختيار)
        # تنفيذ حذف بسيط إذا كان هناك نص في entry
        key = self.entry_var.get().strip()
        if not key:
            messagebox.showinfo('تنبيه', 'ضع نص في حقل الإدخال لحذف المهمة المطابقة')
            return
        indices = [i for i, t in enumerate(self.tasks) if key in t['text']]
        if not indices:
            messagebox.showinfo('نتيجة', 'لم يتم العثور على مهام مطابقة')
            return
        # نحذف من الأخير للأول للحفاظ على صحة الفهارس
        for i in reversed(indices):
            del self.tasks[i]
        self._refresh_tasks_view()
        self.status_var.set('تم حذف المهام المطابقة')

    def edit_task(self, index):
        # فتح مربع حوار لتعديل نص المهمة
        current = self.tasks[index]['text']
        new_text = simpledialog.askstring('تعديل المهمة', 'عدل نص المهمة:', initialvalue=current, parent=self)
        if new_text is None:
            return
        new_text = new_text.strip()
        if new_text:
            self.tasks[index]['text'] = new_text
            self._refresh_tasks_view()
            self.status_var.set('تم تعديل المهمة')

    def edit_selected(self):
        # تعديل أول مهمة تحمل النص في entry (سلوك بسيط وعملي)
        key = self.entry_var.get().strip()
        if not key:
            messagebox.showinfo('تنبيه', 'ضع نص في حقل الإدخال لتحديد المهمة المراد تعديلها')
            return
        for i, t in enumerate(self.tasks):
            if key in t['text']:
                self.edit_task(i)
                return
        messagebox.showinfo('نتيجة', 'لم يتم العثور على مهمة مطابقة')

    # ------------------ الحفظ والتحميل ------------------
    def save_tasks(self):
        # حفظ إلى ملف json
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
            self.status_var.set(f'تم الحفظ في {DATA_FILE}')
        except Exception as e:
            messagebox.showerror('خطأ', f'فشل الحفظ: {e}')

    def _load_tasks(self):
        # محاولة تحميل ملف البيانات عند بدء التشغيل
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
                self._refresh_tasks_view()
                self.status_var.set(f'تم تحميل المهام من {DATA_FILE}')
            except Exception:
                self.tasks = []
        else:
            self.tasks = []

    def _load_tasks_from_dialog(self):
        # تحميل ملف json من اختيار المستخدم
        path = filedialog.askopenfilename(title='اختر ملف JSON للتحميل', filetypes=[('JSON files', '*.json'), ('All files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            if isinstance(loaded, list):
                self.tasks = loaded
                self._refresh_tasks_view()
                self.status_var.set(f'تم تحميل {path}')
            else:
                messagebox.showerror('خطأ', 'تنسيق الملف غير صحيح')
        except Exception as e:
            messagebox.showerror('خطأ', f'فشل التحميل: {e}')

    # ------------------ وظائف اختيارية مساعدة ------------------
    def _auto_save_on_close(self):
        # حفظ تلقائي عند الإغلاق
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def run(self):
        # ربط حدث الإغلاق لحفظ البيانات
        self.protocol('WM_DELETE_WINDOW', lambda: (self._auto_save_on_close(), self.destroy()))
        self.mainloop()


if __name__ == '__main__':
    app = TaskManagerApp()
    app.run()