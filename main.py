import finder
import xmltodict
import threading
import tkinter as tk
from tkinter import ttk

def load_locale(lang):
    with open ('localization/locale.xml', 'r', encoding='utf-8') as f:
        data = xmltodict.parse(f.read())
    return data['localization'][lang]

def set_lang():
    global lan, var
    check = var.get()
    if check == 'english':
        lan = load_locale('english')
    elif check == 'russian':
        lan = load_locale('russian')

    title.configure(text=lan['title']['@value'])
    instr.configure(text=lan['info']['@value'])
    txt1.configure(text=lan['login']['@value'])
    txt2.configure(text=lan['password']['@value'])
    btn.configure(text=lan['button']['@value'])

def GPA():
    output.configure(text=lan['started']['@value'])
    btn.configure(state='disabled')
    threading.Thread(target=calc).start()

def calc():
    dat1 = login.get()
    dat2 = psword.get()
    result = finder.finder(dat1, dat2)
    
    if result == 'KM0':
        output.configure(text=lan['err0']['@value'])
    elif result == 'KM1':
        output.configure(text=lan['err1']['@value'])
    elif result == 'KM2':
        output.configure(text=lan['err2']['@value'])
    else:
        output.configure(text=f"{lan['success']['@value']} {result}")

    btn.configure(state='enabled')

root = tk.Tk()

root.title('Schools.by GPA')
root.geometry('600x600')
root.iconbitmap('etc/icon.ico')

menu_file = tk.Menu(root)
var = tk.StringVar()
var.set('russian')
menu = tk.Menu(menu_file, tearoff=0)
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang)
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang)
menu_file.add_cascade(label='Язык/Language', menu=menu)

lan = load_locale('russian')

title = ttk.Label(root, text=lan['title']['@value'], font=('Arial Bold', '15', 'bold'))
title.place(relx=0.3, rely=0.17)
instr = ttk.Label(root, text=lan['info']['@value'])
instr.place(relx=0.21, rely=0.27)
txt1 = ttk.Label(root, text=lan['login']['@value'])
txt1.place(relx=0.36, rely=0.33)
txt2 = ttk.Label(root, text=lan['password']['@value'])
txt2.place(relx=0.36, rely=0.41)
login = ttk.Entry(root, width=20)
login.place(relx=0.36, rely=0.37)
psword = ttk.Entry(root, width=20, show='*')
psword.place(relx=0.36, rely=0.45)
btn = ttk.Button(root, text=lan['button']['@value'], command=GPA)
btn.place(relx=0.4, rely=0.67)
output = ttk.Label(root, text='', font=('Georgia', '12'))
output.place(relx=0.29, rely=0.56)

root.config(menu=menu_file)
root.mainloop()
