"""

© Copyright 2023 Kalmyk1902
Redistributing under MIT license

"""

#main.py
#импортируем нужные библиотеки
import finder
import xmltodict
import threading
import tkinter as tk
from tkinter import ttk

#функция подгрузки языков
def load_locale(lang):
    with open ('localization/locale.xml', 'r', encoding='utf-8') as f: #открываем XML файл
        data = xmltodict.parse(f.read()) #читаем данные с него
    return data['localization'][lang] #возвращаем путь к языковым данным (см. locale.xml)

#функция смены языка
def set_lang():
    global lan, var #обьявляем переменные значения и языка глобальными
    check = var.get() #берем значение галочки
    if check == 'english': #если язык английский...
        lan = load_locale('english') #то подгружаем его
    elif check == 'russian': #если язык русский...
        lan = load_locale('russian') #то подгружаем его

    #обновляем текст (см. locale.xml)
    title.configure(text=lan['title']['@value'])
    instr.configure(text=lan['info']['@value'])
    txt1.configure(text=lan['login']['@value'])
    txt2.configure(text=lan['password']['@value'])
    btn.configure(text=lan['button']['@value'])

#функция запуска вычислений
def GPA():
    output.configure(text=lan['started']['@value']) #выводим сообщение о запуске вычислений
    btn.configure(state='disabled') #отключаем кнопку
    threading.Thread(target=calc).start() #запускаем поток с функцией вычисления среднего балла

#функция вычисления среднего балла
def calc():
    dat1 = login.get() #берем введеный логин
    dat2 = psword.get() #и пароль
    result = finder.finder(dat1, dat2) #запускаем скрипт (см. код ниже)
    
    if result == 'KM0': #если получаем ошибку КМ0 (не удалось войти)
        output.configure(text=lan['err0']['@value']) #выводим сообщение об этом
    elif result == 'KM1': #если получаем ошибку КМ1 (пустые данные)
        output.configure(text=lan['err1']['@value']) #выводим сообщение об этом
    elif result == 'KM2': #если получаем ошибку КМ2 (нет интернета)
        output.configure(text=lan['err2']['@value']) #выводим сообщение об этом
    else: #в остальных случаях
        output.configure(text=f"{lan['success']['@value']} {result}") #выводим результат выполнения скрипта

    btn.configure(state='enabled') #включаем кнопку обратно

root = tk.Tk() #обьявляем корневую переменную для окна программы

root.title('Schools.by GPA') #даем ей заглавие
root.geometry('600x600') #задаем размер окна
root.iconbitmap('etc/icon.ico') #задаем иконку

#создаем меню выбора языка
menu_file = tk.Menu(root) #определяем основное меню
var = tk.StringVar() #определяем переменную как галочку выбора
var.set('russian') #задаем значение по умолчанию на русский язык
menu = tk.Menu(menu_file, tearoff=0) #определяем окно выбора
menu.add_checkbutton(label='Русский', variable=var, onvalue='russian', command=set_lang) #создаем 1 кнопку выбора (русский язык)
menu.add_checkbutton(label='English', variable=var, onvalue='english', command=set_lang) #создаем 2 кнопку выбора (английский язык)
menu_file.add_cascade(label='Язык/Language', menu=menu) #добавляем окно выбора в меню

lan = load_locale('russian') #ставим загрузку русского языка по умолчанию

#создаем интерфейс
title = ttk.Label(root, text=lan['title']['@value'], font=('Arial Bold', '15', 'bold')) #название программы
title.place(relx=0.3, rely=0.17) #распологаем его
instr = ttk.Label(root, text=lan['info']['@value']) #инструкция
instr.place(relx=0.21, rely=0.27) #распологаем её
txt1 = ttk.Label(root, text=lan['login']['@value']) #логин:
txt1.place(relx=0.36, rely=0.33) #распологаем его
txt2 = ttk.Label(root, text=lan['password']['@value']) #пароль:
txt2.place(relx=0.36, rely=0.41) #распологаем его
login = ttk.Entry(root, width=20) #ввод логина
login.place(relx=0.36, rely=0.37) #распологаем его
psword = ttk.Entry(root, width=20, show='*') #ввод пароля
psword.place(relx=0.36, rely=0.45) #распологаем его
btn = ttk.Button(root, text=lan['button']['@value'], command=GPA) #кнопка запуска
btn.place(relx=0.4, rely=0.67) #распологаем её
output = ttk.Label(root, text='', font=('Georgia', '12')) #вывод результата
output.place(relx=0.29, rely=0.56) #распологаем его

#запуск программы
root.config(menu=menu_file) #добавляем меню в окно программы
root.mainloop() #выводим окно программы

#---------------------------------------

#finder.py
#импортируем нужные библиотеки
import fake_useragent
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

#функция поиска отметок
def calculate():
    driver.get(resp) #входим на сайт
    wait = WebDriverWait(driver, 10) #задаем параметры ожидания в 10 секунд
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'mtable'))) #ожидаем загрузки таблицы успеваемости
    elem_marks = driver.find_elements(By.XPATH, ".//td[contains(concat(' ', @class, ' '), ' lesson_exists ') or contains(concat(' ', @class, ' '), ' lesson_exists-')]//span") #при помощи XPath-выражения извлекаем данные об отметках и пропусках
    all_marks = [mark.text for mark in elem_marks] #записываем все в массив
    driver.quit() #выходим с сайта
    return all_marks #функция возвращает список

#основная функция скрипта
def finder(login, password):
    #объявляем глобальные переменные
    global driver
    global resp
    
    try:
        s = requests.Session() #запускаем сессию
        user = fake_useragent.UserAgent().random #представляемся системе как рандомный браузер

        if login == '' or password == '': #если получаем пустые данные...
            return 'KM1' #возвращаем код ошибки КМ1

        url = 'https://schools.by/login' #объявляем переменную с ссылкой входа
        s.get(url) #заходим в нее
        token = s.cookies['csrftoken'] #получаем токен сессии (без него сайт нас не пустит)
    except requests.exceptions.ConnectionError: #если нету интернета
        return 'KM2' #возвращаем код ошибки КМ2

    #данные для отправки на сервер (при входе на сайт)
    data = {
        'csrfmiddlewaretoken': token, #токен сессии
        'username' : login, #логин
        'password' : password, #пароль
        '|123': '|123' #это нужно
    }

    #метаданные запроса
    header = {
        'user-agent': user, #откуда отправили запрос (в нашем случае с любого браузера)
        'referer': url #кто отправил запрос (в нашем случае сайт для входа)
    }

    logs = s.post(url, data=data, headers=header) #отправляем данные на сервер
    resp = logs.url + '#progress' #получаем ссылку в качестве ответа
    settings = Options() #задаем настройки
    settings.add_argument('--headless') #отключаем интерфейс браузера
    driver = webdriver.Chrome(chrome_options=settings) #входим в браузер
    driver.get(resp) #заходим на полученную ссылку

    if resp == 'https://schools.by/login#progress': #еслм мы остались на той же странице...
        driver.quit() #выходим из браузера
        return 'KM0' #возвращаем код ошибки КМ0

    for cookie in s.cookies: #собираем все cookie файлы для входа на сайт
        driver.add_cookie({'name': cookie.name, 'value': cookie.value}) #и передаем их браузеру

    raw_marks = calculate() #используем ранее объявленную функцию для извлечения данных
    marks = [] #создаем пустой список
    for mark in raw_marks: #фильтруем список
        if '/' in mark: #если находим двойную отметку...
            marks.extend(mark.split('/')) #вписываем две отметки раздельно друг от друга
        else:
            marks.append(mark) #иначе просто записываем ее

    marks = [x for x in marks if x.isdigit()] #отсеиваем все пропуски и пустые отметки
    marks = list(map(int, marks)) #переводим в числовой тип данных
    total = sum(marks) / len(marks) #вычисляем средний балл (сумму всех отметок делим на их количество)
    return round(total, 2) #возвращаем средний балл с ограничением в 2 символа после точки
