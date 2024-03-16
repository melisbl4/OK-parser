from tkinter import *
import sqlite3
from tkinter import messagebox


def output(col, data):
    Label(frame, bg="#ffffff").place(relwidth=1, relheight=0.9, rely=0.1)
    n = len(col)
    for i in range(n):
        if i % 2 == 0:
            Label(frame, bg="#d0d0d0", text=col[i]).place(relwidth=(1 / n), relx=(i / n), relheight=0.03, rely=0.1)
        else:
            Label(frame, bg="#dfdfdf", text=col[i]).place(relwidth=(1 / n), relx=(i / n), relheight=0.03, rely=0.1)
    for j in range(len(data)):
        for i in range(n):
            if (i + j) % 2 == 0:
                Label(frame, bg="#ffffff", text=str(data[j][i])).place(relwidth=(1 / n), relx=(i / n), relheight=0.03,
                                                                       rely=(0.13 + 0.03 * j))
            else:
                Label(frame, bg="#f0f0f0", text=str(data[j][i])).place(relwidth=(1 / n), relx=(i / n), relheight=0.03,
                                                                       rely=(0.13 + 0.03 * j))


def create_request(tab, col, con):
    if col == "":
        req = "SELECT * FROM " + tab
        desc = conn.execute(req).description
        for i in desc:
            col = col + i[0] + " "
        col = col[0:-1]
    else:
        req = "SELECT "
        for i in col.split():
            req = req + i + ", "
        req = req[0:-2] + " FROM " + tab
    if con != "":
        req = req + " WHERE "
        for i in con.split():
            req = req + i + " AND "
        req = req[0:-5]
    return req, col


def search_click():
    global res
    global first_index
    global col
    first_index = 0
    tab = str(table.get())
    col = str(column.get())
    con = str(condition.get())

    req, col = create_request(tab, col, con)

    try:
        res = cur.execute(req).fetchall()
        if len(res) > 29:
            output(col.split(), res[0:29])
        else:
            output(col.split(), res)
    except:
        messagebox.showerror(title="ОШИБКА", message="Некоректный запрос")


def forward_click():
    global first_index
    global res
    global col
    if len(res) > first_index + 29:
        first_index += 29
        output(col.split(), res[first_index:first_index + 29])


def back_click():
    global first_index
    global res
    global col
    if first_index > 0:
        first_index -= 29
        output(col.split(), res[first_index:first_index + 29])


conn = sqlite3.connect("okpars.db")
cur = conn.cursor()
root = Tk()

root['bg'] = "#eeeeee"
root.title("GUI for OK")
root.geometry("1280x720")
root.resizable(width=False, height=False)

frame = Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)

table = Entry(frame, bg='#eeeeee')
table.place(relwidth=0.3, relx=0, relheight=0.03, rely=0.07)

table_label = Label(frame, text="таблица", bg="white")
table_label.place(relwidth=0.3, relx=0, relheight=0.03, rely=0.04)

column = Entry(frame, bg="#eeeeee")
column.place(relwidth=0.3, relx=0.3, relheight=0.03, rely=0.07)

coloumn_label = Label(frame, text="поля (через пробел)", bg="white")
coloumn_label.place(relwidth=0.3, relx=0.3, relheight=0.03, rely=0.04)

condition = Entry(frame, bg="#eeeeee")
condition.place(relwidth=0.3, relx=0.6, relheight=0.03, rely=0.07)

condition_label = Label(frame, text="условия (через пробел)", bg="white")
condition_label.place(relwidth=0.3, relx=0.6, relheight=0.03, rely=0.04)

back = Button(frame, bg='#dddddd', text="<- назад", command=back_click)
back.place(relwidth=0.2, relx=0, relheight=0.03, rely=0)
forward = Button(frame, bg='#dddddd', text="вперёд ->", command=forward_click)
forward.place(relwidth=0.2, relx=0.8, relheight=0.03, rely=0)

btn_search = Button(frame, bg='#dddddd', text="поиск", command=search_click)
btn_search.place(relwidth=0.1, relx=0.9, relheight=0.03, rely=0.07)

root.mainloop()
