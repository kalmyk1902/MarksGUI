"""

© Copyright 2023 Kalmyk1902
Redistributing under MIT license

"""

#main.py
#import necessary libraries
import finder
import xmltodict
import threading
import tkinter as tk
from tkinter import ttk

#load language function
def load_locale(lang):
    with open ('localization/locale.xml', 'r', encoding='utf-8') as f: #open XML file
        data = xmltodict.parse(f.read()) #read data
    return data['localization'][lang] #return language data path (see locale.xml)

#change language function
def set_lang():
    global lan, var #declare variables global
    check = var.get() #get language setting
    if check == 'english': #if english...
        lan = load_locale('english') #load this
    elif check == 'russian': #if russian...
        lan = load_locale('russian') #load this

    #updating text (see locale.xml)
    title.configure(text=lan['title']['@value'])
    instr.configure(text=lan['info']['@value'])
    txt1.configure(text=lan['login']['@value'])
    txt2.configure(text=lan['password']['@value'])
    btn.configure(text=lan['button']['@value'])

#start calculating function
def GPA():
    output.configure(text=lan['started']['@value']) #output message about starting of calculating
    btn.configure(state='disabled') #disable button
    threading.Thread(target=calc).start() #starting thread with GPA calculation function

#GPA calculation function
def calc():
    dat1 = login.get() #get entered login
    dat2 = psword.get() #and password
    result = finder.finder(dat1, dat2) #starting the script (see code below)
    
    if result == 'KM0': #if we getting error code KM0 (login failed)
        output.configure(text=lan['err0']['@value']) #outputing message about this
    elif result == 'KM1': #if we getting error code KM1 (empty data)
        output.configure(text=lan['err1']['@value']) #outputing message about this
    elif result == 'KM2': #if we getting error code KM2 (no connection)
        output.configure(text=lan['err2']['@value']) #outputing message about this
    else: #in other cases
        output.configure(text=f"{lan['success']['@value']} {result}") #outputing the result of script

    btn.configure(state='enabled') #enable button

root = tk.Tk() #declare root variable for program's window

root.title('Ruble converter') #naming it
root.geometry('600x600') #setting its size
root.iconbitmap('etc/icon.ico') #setting its icon

#creating langauge change menu
menu_file = tk.Menu(root) #defining the main menu
var = tk.StringVar() #defining the check variable
var.set('russian') #setting the default langauge as russian
menu = tk.Menu(menu_file, tearoff=0) #creating the langauge section
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang) #adding russian lang check
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang) #adding english lang check
menu_file.add_cascade(label='Язык/Language', menu=menu) #adding section to menu

lan = load_locale('russian') #setting russian langauge as default

#creating the UI
title = ttk.Label(root, text=lan['title']['@value'], font=('Arial Bold', '15', 'bold')) #title
title.place(relx=0.3, rely=0.17) #placing it
instr = ttk.Label(root, text=lan['info']['@value']) #instructions
instr.place(relx=0.21, rely=0.27) #placing it
txt1 = ttk.Label(root, text=lan['login']['@value']) #login:
txt1.place(relx=0.36, rely=0.33) #placing it
txt2 = ttk.Label(root, text=lan['password']['@value']) #password:
txt2.place(relx=0.36, rely=0.41) #placing it
login = ttk.Entry(root, width=20) #login entry
login.place(relx=0.36, rely=0.37) #placing it
psword = ttk.Entry(root, width=20, show='*') #password entry
psword.place(relx=0.36, rely=0.45) #placing it
btn = ttk.Button(root, text=lan['button']['@value'], command=GPA) #start button
btn.place(relx=0.4, rely=0.67) #placing it
output = ttk.Label(root, text='', font=('Georgia', '12')) #result output
output.place(relx=0.29, rely=0.56) #placing it

#starting the program
root.config(menu=menu_file) #adding menu to the window
root.mainloop() #opening the window

#---------------------------------------

#finder.py
#import necessary libraries
import fake_useragent
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

#searching marks function
def calculate():
    driver.get(resp) #entering site
    wait = WebDriverWait(driver, 10) #set 10 seconds timeout
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'mtable'))) #awaiting for score table
    elem_marks = driver.find_elements(By.XPATH, ".//td[contains(concat(' ', @class, ' '), ' lesson_exists ') or contains(concat(' ', @class, ' '), ' lesson_exists-')]//span") #using XPath extracting marks and skipped lessons
    all_marks = [mark.text for mark in elem_marks] #writing in list
    driver.quit() #leaving site
    return all_marks #return list of marks

#main function of the script
def finder(login, password):
    #declaring global variables
    global driver
    global resp
    
    try:
        s = requests.Session() #starting session
        user = fake_useragent.UserAgent().random #introducing as random browser

        if login == '' or password == '': #if we got empty data...
            return 'KM1' #return error code КМ1

        url = 'https://schools.by/login' #declaring login URL variable
        s.get(url) #entering the URL
        token = s.cookies['csrftoken'] #get session token (or site will be blocking us)
    except requests.exceptions.ConnectionError: #if no internet
        return 'KM2' #return error code KM2

    #data that will be sent to server (login data)
    data = {
        'csrfmiddlewaretoken': token, #session token
        'username' : login, #login
        'password' : password, #password
        '|123': '|123' #it needed
    }

    #request metadata
    header = {
        'user-agent': user, #where request was sent (in our case from any browser)
        'referer': url #who sent requset (in our case the login site)
    }

    logs = s.post(url, data=data, headers=header) #send data to server
    resp = logs.url + '#progress' #get the URL as response
    settings = Options() #set options
    settings.add_argument('--headless') #disabling the browser UI
    driver = webdriver.Chrome(chrome_options=settings) #starting browser
    driver.get(resp) #entering the URL

    if resp == 'https://schools.by/login#progress': #if we still in login URL...
        driver.quit() #leaving the browser
        return 'KM0' #return error code КМ0

    for cookie in s.cookies: #collecting all cookies from session
        driver.add_cookie({'name': cookie.name, 'value': cookie.value}) #and transfering to browser

    raw_marks = calculate() #using function to extract data
    marks = [] #declaring empty list
    for mark in raw_marks: #filtering raw list
        if '/' in mark: #if double mark found...
            marks.extend(mark.split('/')) #spliting into 2 marks
        else:
            marks.append(mark) #in other cases writing it as 1 mark

    marks = [x for x in marks if x.isdigit()] #deleting all skipped lessons and empty marks
    marks = list(map(int, marks)) #changing data type to int
    total = sum(marks) / len(marks) #calculating GPA (all marks dividing by their amount)
    return round(total, 2) #return the GPA with limit 2 digits after dot 
