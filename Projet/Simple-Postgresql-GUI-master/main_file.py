from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import postgresql_commands


# APPLICATION FUNCTIONS FOR THE GUI BUTTONS


def add_item():
    if first_name.get() == "" or last_name.get() == "" or gender.get() == "" or birth_date.get() == "" or \
            job.get() == "" or email.get() == "" or salary.get() == "" or hired_date.get() == "" or \
            warning_strike.get() == "":
        messagebox.showerror("Required Fields", "Please fill all fields!")
        return
    num = 0
    if re.match(r'\d\d\d\d-\d\d-\d\d', birth_date.get()) and re.match(r'\d\d\d\d-\d\d-\d\d', hired_date.get()):
        num += 1
    else:
        messagebox.showerror("Wrong Date", "Wrong date format please insert YYYY-MM-DD")
        return
    if not warning_strike.get().isdecimal():
        messagebox.showerror("Wrong Type", "Warning Strike needs to be an INT number")
        return
    if gender.get().lower() != "female" and gender.get().lower() != "male" and gender.get().lower() != "other":
        messagebox.showerror("Gender", "Gender options Female, Male and Other")
        return

    postgresql_commands.insert_data(first_name.get(), last_name.get(), gender.get(), birth_date.get(), job.get(),
                                    email.get(), salary.get(), hired_date.get(), warning_strike.get())

    database.insert("", END, (first_name.get(), last_name.get(), gender.get(), birth_date.get(), job.get(), email.get(),
                              salary.get(), hired_date.get(), warning_strike.get()))
    clear_item()
    order_id()


def delete_item():
    postgresql_commands.remove_data(item_id)
    clear_item()
    order_id()


def update_item():
    if first_name.get() == "" or last_name.get() == "" or gender.get() == "" or birth_date.get() == "" or \
            job.get() == "" or email.get() == "" or salary.get() == "" or hired_date.get() == "" or \
            warning_strike.get() == "":
        messagebox.showerror("Required Fields", "Please fill all fields!")
        return
    num = 0
    if re.match(r'\d\d\d\d-\d\d-\d\d', birth_date.get()) and re.match(r'\d\d\d\d-\d\d-\d\d', hired_date.get()):
        num += 1
    else:
        messagebox.showerror("Wrong Date", "Wrong date format please insert YYYY-MM-DD")
        return
    if not warning_strike.get().isdecimal():
        messagebox.showerror("Wrong Type", "Warning Strike needs to be an INT number")
        return
    if gender.get().lower() != "female" and gender.get().lower() != "male" and gender.get().lower() != "other":
        messagebox.showerror("Gender", "Gender options Female, Male and Other")
        return

    postgresql_commands.update_data(first_name.get(), last_name.get(), gender.get(), birth_date.get(), job.get(),
                                    email.get(), salary.get(), hired_date.get(), warning_strike.get(), item_id)
    clear_item()
    order_id()


def clear_item():
    person_id_entry.configure(state="normal")
    person_id_entry.delete(0, END)
    person_id_entry.configure(state="readonly")
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    gender_entry.delete(0, END)
    birth_date_entry.delete(0, END)
    job_entry.delete(0, END)
    email_entry.delete(0, END)
    salary_entry.delete(0, END)
    hired_date_entry.delete(0, END)
    warning_strike_entry.delete(0, END)


def find_person_name():
    if search_last_entry.get() == "" or search_last_entry.get() == "":
        messagebox.showerror("Required fields", "Please fill both First Name and Last Name before the search!")
        return
    index = 0
    database.delete(*database.get_children())
    for rows in postgresql_commands.search_by_name(search_first_entry.get(), search_last_entry.get()):
        database.insert("", index, values=rows)
        index = index + 1
    search_first_entry.delete(0, END)
    search_last_entry.delete(0, END)


def order_id():
    index = 0
    database.delete(*database.get_children())
    for rows in postgresql_commands.order_by_id():
        database.insert("", index, values=rows)
        index = index + 1


def order_name():
    index = 0
    database.delete(*database.get_children())
    for rows in postgresql_commands.order_by_name():
        database.insert("", index, values=rows)
        index = index + 1


def order_salary():
    index = 0
    database.delete(*database.get_children())
    for rows in postgresql_commands.order_by_salary():
        database.insert("", index, values=rows)
        index = index + 1


def order_job():
    index = 0
    database.delete(*database.get_children())
    for rows in postgresql_commands.order_by_job():
        database.insert("", index, values=rows)
        index = index + 1


# CLICK EVENTS TO ERASE TEXT FROM ENTRY BOX WHEN CLICKED


def clear_first(event):
    search_first_entry.delete(0, END)


def clear_last(event):
    search_last_entry.delete(0, END)


# CLICK EVENT TO GET DATA FROM TREE VIEW TO ENTRY BOXES WHEN CLICKED


def select_item(event):
    global item_id
    global selected_item
    index = database.selection()
    selected_item = database.item(index)
    item_id = selected_item['values'][0]

    person_id_entry.configure(state="normal")
    person_id_entry.delete(0, END)
    person_id_entry.insert(END, selected_item['values'][0])
    person_id_entry.configure(state="readonly")
    first_name_entry.delete(0, END)
    first_name_entry.insert(END, selected_item['values'][1])
    last_name_entry.delete(0, END)
    last_name_entry.insert(END, selected_item['values'][2])
    gender_entry.delete(0, END)
    gender_entry.insert(END, selected_item['values'][3])
    birth_date_entry.delete(0, END)
    birth_date_entry.insert(END, selected_item['values'][4])
    job_entry.delete(0, END)
    job_entry.insert(END, selected_item['values'][5])
    email_entry.delete(0, END)
    email_entry.insert(END, selected_item['values'][6])
    salary_entry.delete(0, END)
    salary_entry.insert(END, selected_item['values'][7])
    hired_date_entry.delete(0, END)
    hired_date_entry.insert(END, selected_item['values'][8])
    warning_strike_entry.delete(0, END)
    warning_strike_entry.insert(END, selected_item['values'][9])


# TKINTER WINDOW CONFIGURATION


app = Tk()
app.title("Emplpoyees Database")
app.geometry("1020x650")
app.resizable(height=FALSE, width=FALSE)


# ###############################  MAIN GRID LABELS, BUTTONS AND ENTRY BOXES  ######################################


# INFO ENTRY BOXES AND INFO LABELS


person_id = StringVar()
person_id_label = Label(app, text='Person ID:', pady=20)
person_id_label.grid(row=0, column=0, sticky=W)
person_id_entry = Entry(app, textvariable=person_id, state='readonly')
person_id_entry.grid(row=0, column=1)

first_name = StringVar()
first_name_label = Label(app, text='First Name:')
first_name_label.grid(row=0, column=2, sticky=W)
first_name_entry = Entry(app, textvariable=first_name)
first_name_entry.grid(row=0, column=3)

last_name = StringVar()
last_name_label = Label(app, text='Last Name:')
last_name_label.grid(row=0, column=4, sticky=W)
last_name_entry = Entry(app, textvariable=last_name)
last_name_entry.grid(row=0, column=5)

gender = StringVar()
gender_label = Label(app, text='Gender:')
gender_label.grid(row=0, column=6, sticky=W)
gender_entry = Entry(app, textvariable=gender)
gender_entry.grid(row=0, column=7)

birth_date = StringVar()
birth_date_label = Label(app, text='Birth date:')
birth_date_label.grid(row=0, column=8, sticky=W)
birth_date_entry = Entry(app, textvariable=birth_date)
birth_date_entry.grid(row=0, column=9)

job = StringVar()
job_label = Label(app, text='Job:')
job_label.grid(row=1, column=0, sticky=W)
job_entry = Entry(app, textvariable=job)
job_entry.grid(row=1, column=1)

email = StringVar()
email_label = Label(app, text='E-mail:')
email_label.grid(row=1, column=2, sticky=W)
email_entry = Entry(app, textvariable=email)
email_entry.grid(row=1, column=3)

salary = StringVar()
salary_label = Label(app, text='Gross Salary:')
salary_label.grid(row=1, column=4, sticky=W)
salary_entry = Entry(app, textvariable=salary)
salary_entry.grid(row=1, column=5)

hired_date = StringVar()
hired_date_label = Label(app, text='Hired Date:')
hired_date_label.grid(row=1, column=6, sticky=W)
hired_date_entry = Entry(app, textvariable=hired_date)
hired_date_entry.grid(row=1, column=7)

warning_strike = StringVar()
warning_strike_label = Label(app, text='Warning Strike:')
warning_strike_label.grid(row=1, column=8, sticky=W)
warning_strike_entry = Entry(app, textvariable=warning_strike)
warning_strike_entry.grid(row=1, column=9)


# MAIN BUTTONS

insert_data = Button(app, text='Insert Data', width=9, command=add_item)
insert_data.grid(row=2, column=0, pady=20, columnspan=12, sticky=W, padx=14)

delete_data = Button(app, text='Delete Data', width=9, command=delete_item)
delete_data.grid(row=2, column=0, columnspan=12, sticky=W, padx=89)

update_data = Button(app, text='Update Data', width=9, command=update_item)
update_data.grid(row=2, column=0, columnspan=12, sticky=W, padx=164)

clear_data = Button(app, text='Clear Entries', width=9, command=clear_item)
clear_data.grid(row=2, column=0, columnspan=12, sticky=W, padx=239)


# ORDER BUTTONS


order_label = Label(app, text='Ordered by:')
order_label.grid(row=2, column=7, sticky=W, padx=100, columnspan=40)

ord_id = Button(app, text='ID', width=4, command=order_id)
ord_id.grid(row=2, column=8, columnspan=12, sticky=W, padx=52)

ord_name = Button(app, text='Name', width=4, command=order_name)
ord_name.grid(row=2, column=8, columnspan=12, sticky=W, padx=91)

ord_salary = Button(app, text='Salary', width=4, command=order_salary)
ord_salary.grid(row=2, column=8, columnspan=12, sticky=W, padx=130)

ord_job = Button(app, text='Job', width=4, command=order_job)
ord_job.grid(row=2, column=9, columnspan=12, sticky=W, padx=80)


# SEARCH BUTTONS AND LABEL


find_label = Label(app, text='Find:')
find_label.grid(row=2, column=3, columnspan=12, sticky=W, padx=85)

find_first_name = StringVar()
search_first_entry = Entry(app, textvariable=find_first_name)
search_first_entry.insert(0, "First Name")
search_first_entry.grid(row=2, column=3, columnspan=12, sticky=W, padx=120)
search_first_entry.bind("<Button-1>", clear_first)

find_last_name = StringVar()
search_last_entry = Entry(app, textvariable=find_last_name)
search_last_entry.insert(0, "Last Name")
search_last_entry.grid(row=2, column=5, columnspan=12, sticky=W, padx=60)
search_last_entry.bind("<Button-1>", clear_last)

search_button = Button(app, text='Search Name', width=10, command=find_person_name)
search_button.grid(row=2, column=7, columnspan=12, sticky=W)


# TREE VIEW BOX


database = ttk.Treeview(app, height=23)
database.grid(row=3, column=0, columnspan=13, rowspan=5, padx=15, sticky=W)
database["columns"] = ("id", "First Name", "Last Name", "Gender", "Birth Date", "Job", "E-mail", "Gross Salary",
                       "Hired Date", "Warning Strikes")
database["show"] = "headings"
database.heading("#0", text="ID", anchor="w")
database.column("#0", width=100)
database.heading("id", text="ID", anchor="w")
database.column("id", width=33)
database.heading("First Name", text="First Name", anchor="w")
database.column("First Name", width=78)
database.heading("Last Name", text="Last Name", anchor="w")
database.column("Last Name", width=78)
database.heading("Gender", text="Gender", anchor="w")
database.column("Gender", width=50)
database.heading("Birth Date", text="Birth Date", anchor="w")
database.column("Birth Date", width=67)
database.heading("Job", text="Job", anchor="w")
database.column("Job", width=220)
database.heading("E-mail", text="E-mail", anchor="w")
database.column("E-mail", width=220)
database.heading("Gross Salary", text="Gross Salary", anchor="w")
database.column("Gross Salary", width=75)
database.heading("Hired Date", text="Hired Date", anchor="w")
database.column("Hired Date", width=67)
database.heading("Warning Strikes", text="Warning Strikes", anchor="w")
database.column("Warning Strikes", width=85)


# SCROLL BAR FOR THE TREE VIEW BOX

database_scrollbar = ttk.Scrollbar(app)
database_scrollbar.grid(row=3, column=10, sticky="ns", rowspan=5, padx=12)
database_scrollbar.configure(command=database.yview)
database.config(yscrollcommand=database_scrollbar.set)


# BIND MOUSE CLICK EVENT TO THE TREE VIEW


database.bind("<<TreeviewSelect>>", select_item)


# ORDER TREE VIEW AND INITIATES APP

order_id()
mainloop()
