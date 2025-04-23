'''
    Catabas, Jhana Marie D.
    BSIT 3A
    7:30 - 10:00 AM TTH
'''

import tkinter as tk
from tkinter import ttk
from tkinter import END, messagebox
import sqlite3

class Student():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management v1.0")
        self.position()
        self.root.resizable(False, False)
        self.addwidget()
        
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Verdana", 11),
                        background="white",
                        fieldbackground="gray",
                        foreground="black") 
        style.configure("Treeview.Heading", font=("Verdana", 12, "bold"), background="lightgray")
        
        # Define styles for alternate row colors
        self.tree = ttk.Treeview(self.records_frame, columns=('IDNO', 'NAME', 'COURSE-LEVEL'), show='headings', height=20)
        self.tree.heading('IDNO', text='IDNO')
        self.tree.heading('NAME', text='NAME')
        self.tree.heading('COURSE-LEVEL', text='COURSE-LEVEL')

        self.tree.column('IDNO', width=100, anchor='center')
        self.tree.column('NAME', width=200, anchor='center')
        self.tree.column('COURSE-LEVEL', width=150, anchor='center')

        self.tree.pack(padx=15, pady=15)

        # Tags for alternating colors
        self.tree.tag_configure('oddrow', background='lightblue')
        self.tree.tag_configure('evenrow', background='white')

        self.load_records()
        self.root.mainloop()
        
    def position(self) -> None:
        self.width = 900
        self.height = 480
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+{(self.screen_width-self.width)//2}+{(self.screen_height-self.height)//2}")
    
    def addwidget(self) -> None:
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_idno = tk.Label(self.frame, text="IDNO", font="Verdana,20")
        self.lbl_idno.grid(row=0, column=0, padx=20, pady=5, sticky="W")
        self.idno = tk.Entry(self.frame, width=30, font="Verdana,20")
        self.idno.grid(row=1, column=0, padx=20, pady=5)

        self.lbl_lname = tk.Label(self.frame, text="LASTNAME", font="Verdana,20")
        self.lbl_lname.grid(row=2, column=0, padx=20, pady=5, sticky="W")
        self.lname = tk.Entry(self.frame, width=30, font="Verdana,20")
        self.lname.grid(row=3, column=0, padx=20, pady=5)

        self.lbl_fname = tk.Label(self.frame, text="FIRSTNAME", font="Verdana,20")
        self.lbl_fname.grid(row=4, column=0, padx=20, pady=5, sticky="W")
        self.fname = tk.Entry(self.frame, width=30, font="Verdana,20")
        self.fname.grid(row=5, column=0, padx=20, pady=5)

        self.lbl_course = tk.Label(self.frame, text="COURSE", font="Verdana,20")
        self.lbl_course.grid(row=6, column=0, padx=20, pady=5, sticky="W")
        self.course = ttk.Combobox(self.frame, width=29, font="Verdana,20")
        self.course['values'] = ('BSIT', 'BSCS', 'BSCPE', 'BSBA', 'BSCJ', 'BSHM', 'BSE', 'BEED')
        self.course.grid(row=7, column=0, padx=20, pady=5, sticky="W")

        self.lbl_level = tk.Label(self.frame, text="LEVEL", font="Verdana,20")
        self.lbl_level.grid(row=8, column=0, padx=20, pady=5, sticky="W")
        self.level = ttk.Combobox(self.frame, width=29, font="Verdana,20")
        self.level['values'] = ('1', '2', '3', '4')
        self.level.grid(row=9, column=0, padx=20, pady=5, sticky="W")

        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.grid(row=10, column=0, columnspan=2, padx=20, pady=5)

        self.btn_save = tk.Button(self.btn_frame, text="Save", width=13, font="Verdana,20", command=self.save)
        self.btn_save.grid(row=0, column=0, padx=10)

        self.btn_cancel = tk.Button(self.btn_frame, text="Cancel", width=13, font="Verdana,20", command=self.cancel)
        self.btn_cancel.grid(row=0, column=1, padx=10)

        # saved records
        self.records_frame = tk.Frame(self.root)
        self.records_frame.grid(row=0, column=1, padx=5, pady=5)

    def save(self) -> None:
        # Check if any fields are empty
        if not self.idno.get() or not self.lname.get() or not self.fname.get() or not self.course.get() or not self.level.get():
            messagebox.showerror("Error", "All fields must be filled!")
            return

        # Validate IDNO (must be a string of digits)
        idno_value = self.idno.get()
        if not idno_value.isdigit():
            messagebox.showerror("Error", "IDNO must be numeric (digits only)!")
            return
        
        # Validate LASTNAME and FIRSTNAME (must not contain digits)
        if any(char.isdigit() for char in self.lname.get()):
            messagebox.showerror("Error", "LASTNAME must not contain numbers!")
            return

        if any(char.isdigit() for char in self.fname.get()):
            messagebox.showerror("Error", "FIRSTNAME must not contain numbers!")
            return
        
        # Validate course and level
        if self.course.get() not in self.course['values']:
            messagebox.showerror("Error", "Please select a valid course!")
            return
        if self.level.get() not in self.level['values']:
            messagebox.showerror("Error", "Please select a valid level!")
            return

        conn = sqlite3.connect('student.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO students (idno, lastname, firstname, course, level) VALUES (:a, :b, :c, :d, :e)", 
                      {
                        'a': idno_value,  # Store as a string to preserve leading zeros
                        'b': self.lname.get(),
                        'c': self.fname.get(),
                        'd': self.course.get(),
                        'e': self.level.get()
                      })
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "IDNO must be unique!")
        finally:
            conn.close()

        # Clear entries
        self.idno.delete(0, END)
        self.lname.delete(0, END)
        self.fname.delete(0, END)
        self.course.set('')
        self.level.set('')

        self.load_records()

    def load_records(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        conn = sqlite3.connect('student.db')
        c = conn.cursor()

        c.execute("SELECT idno, lastname || ', ' || firstname AS name, course || '-' || level AS course_level FROM students")
        records = c.fetchall()

        for index, record in enumerate(records):
            if index % 2 == 0:
                self.tree.insert('', 'end', values=record, tags=('evenrow',))
            else:
                self.tree.insert('', 'end', values=record, tags=('oddrow',))

        conn.close()

    def cancel(self) -> None:
        # Clears the input fields
        self.idno.delete(0, END)
        self.lname.delete(0, END)
        self.fname.delete(0, END)
        self.course.set('')
        self.level.set('')
        
def main() -> None:
    Student()
    
if __name__ == "__main__":
    main()
