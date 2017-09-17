from telebot import types
from telebot import util
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
import telebot
import os
import time
from datetime import datetime
import csv

class Count:
    date =0
    number = 0
    late = 0
    mark = 0
    def __init__(self,mark = 3,late = 0):
        self.fio = 0
        self.date = 0
        self.number = 0
        self.late = late
        self.mark = mark




class Config:
    Days = []
    Events = []
    Fios =[]
    TodayEvents=[]

    def __init__(self, list):
        for i in range(1,len(list)):
            if len(list[i]) == 4:
                self.Fios.append(list[i][3])
            self.Days.append(list[i][0])
            self.Events.append(list[i][1])

    def ret_d(self):

        return self.Days

    def ret_e(self):
        for i in range(len(self.Days)):
            if int(datetime.now().isoweekday())==int(self.Days[i]):
                self.TodayEvents.append(self.Events[i])

        return self.TodayEvents

    def ret_f(self):
        return self.Fios





files =[]
list1=[]
Spisok=[]
dat = 0
reader = csv.reader(open('config__c.csv'), delimiter=',', quotechar=' ')
for row in reader:
    list1.append(row)
config1 = Config(list1);

listmenu = [
    ['Мероприятия', 'Статистика по посетителю', 'Общая статистика', 'Предыдущие отчеты', 'Скачать конфигурацию',
     'Закачать конфигурацию', 'Отмена'],
    config1.ret_e(),
    config1.ret_f(),
    ['Присутствует', 'Отсутствует', 'Опоздал', 'Отмена']
]
listmenu[1].append('Отмена')
listmenu[2].append('Отмена')
#for i in range(len(config1.ret_f())):
#    Spisok.append(Count(config1.ret_f()[i]))

Rec = Count()
py = [0] * len(config1.ret_f())

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def messages(message):
    if message.text == 'Меню':
        bot.send_message(message.chat.id, 'Введите пароль', None)

    elif message.text == config.password:

        key_default = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(listmenu[0])):
            key_default.row(types.KeyboardButton(listmenu[0][i]))
        msg = bot.reply_to(message, 'Меню открыто', reply_markup=key_default)
        bot.register_next_step_handler(msg, button)
    else:
        try:
            Rec.late=int(message.text)
        except:
            print()




def button(message):
    global py,config1,dat
    if dat!=str(datetime.now().date()):
        er=[]
        fl = str(datetime.now().date()).split('-')
        with open('reports.csv', 'r') as fp:
            reader1 = csv.reader(fp, delimiter=',', quotechar='"')
            data_read = [row for row in reader1]
        for i in range(len(data_read)):
            for j in range(len(config1.ret_f())):

                if i % 2 == 0:
                    print(i, j)
                    if data_read[i][1] == config1.ret_f()[j] and (fl[0] + '-' + fl[1] + '-' + str(int(fl[2]) - 1)) == \
                            data_read[i][0]:
                        py[j] += 1
        for i in range(len(config1.Days)):
            if int(datetime.now().isoweekday()) - 1 == int(config1.Days[i]):
                er.append(config1.Events[i])
        for j in range(len(config1.ret_f())):
            py[j] +=len(er)- py[j]
        dat=str(datetime.now().date())
    if message.text == 'Мероприятия':
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[1])):
            key_default.row(types.KeyboardButton(listmenu[1][i]))
        msg = bot.reply_to(message, 'Мероприятия открыты', reply_markup=key_default)
        bot.register_next_step_handler(msg, button1)
    elif message.text == 'Отмена':
        keyboard_hider = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отмена!', reply_markup=keyboard_hider)
    elif message.text == 'Статистика по посетителю':
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[2])):
            key_default.row(types.KeyboardButton(listmenu[2][i]))
        msg = bot.reply_to(message, 'Посетители', reply_markup=key_default)
        bot.register_next_step_handler(msg, pers_stat)
    elif message.text == 'Общая статистика':
        stat=[[0,0,0,0] for x in range(4)]
        with open('reports.csv', 'r') as fp:
            reader1 = csv.reader(fp, delimiter=',', quotechar='"')
            data_read = [row for row in reader1]
        for j in range(len(config1.ret_f())):
            for i in range(len(data_read)):
                if i % 2 == 0:
                    if data_read[i][1] == config1.ret_f()[j]:
                        if int(data_read[i][3]) == 0:
                            stat[j][0] += 1
                        elif int(data_read[i][3]) == 1:
                            stat[j][1] += 1
                        elif int(data_read[i][3]) == 2:
                            stat[j][2] += 1
                    stat[j][3]=py[j]
        for j in range(len(config1.ret_f())):
            stat[j].insert(0, config1.ret_f()[j])
        stat.pop()
        a11 = str(datetime.now().date()).split('-')
        filename = 'reports/' + a11[0] + '-' + a11[1] +'.csv'
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(stat)
        dat = open(filename, 'rb')
        bot.send_document(message.chat.id, dat, None)
        msg = bot.reply_to(message, 'Меню')
        bot.register_next_step_handler(msg, button)
    elif message.text == 'Скачать конфигурацию':
        conf = open('config__c.csv', 'rb')
        bot.send_document(message.chat.id, conf, None)
        msg = bot.reply_to(message, 'Меню')
        bot.register_next_step_handler(msg, button)
    elif message.text == 'Предыдущие отчеты':
        global files
        files =[]
        list2=[]
        for file in os.listdir('reports/'):
            print(file)
            try:
                int(file.split('-')[0])
                files.append(file)
            except:
                print()
        a = str(datetime.now().date()).split('-')
        files.sort(reverse=True)
        for i in range(len(files)):
            if len(list2)<20:
                list2.append(files[i])
        files.append('Отмена')
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(files)):
            key_default.row(types.KeyboardButton(list2[i]))
        msg = bot.reply_to(message, 'Отмена', reply_markup=key_default)
        bot.register_next_step_handler(msg, rep)



    elif message.text == 'Закачать конфигурацию':
        bot.send_message(message.chat.id, 'Отправьте файл конфигурации config__c.csv', None)
        @bot.message_handler(content_types=['document'])
        def handle_docs_photo(message):

            try:
                chat_id = message.chat.id

                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = message.document.file_name;
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                reader1 = csv.reader(open('config__c.csv'), delimiter=',', quotechar=' ')
                for row in reader:
                    list1.append(row)
                os.remove('reports.csv')
                open('reports.csv', 'wb')
                
                bot.reply_to(message, "Конфигурация добавлена")
                key_default = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in range(len(listmenu[0])):
                    key_default.row(types.KeyboardButton(listmenu[0][i]))
                msg = bot.reply_to(message, 'Меню открыто', reply_markup=key_default)
                bot.register_next_step_handler(msg, button)



            except Exception as e:
                bot.reply_to(message, e)

def button1(message):
    if message.text == 'Отмена':
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[0])):
            key_default.row(types.KeyboardButton(listmenu[0][i]))
        msg = bot.reply_to(message, 'Меню', reply_markup=key_default)
        bot.register_next_step_handler(msg, button)
    else:
        Rec.number =str(message.text)

        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[2])):
            key_default.row(types.KeyboardButton(listmenu[2][i]))
        msg = bot.reply_to(message, 'Посетители открыты', reply_markup=key_default)
        bot.register_next_step_handler(msg, button2)

def button2(message):
    if message.text == 'Отмена':
        Rec.late = 0
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[1])):
            key_default.row(types.KeyboardButton(listmenu[1][i]))
        msg = bot.reply_to(message, 'Посетители', reply_markup=key_default)
        bot.register_next_step_handler(msg, button1)
    else:
        Rec.fio = str(message.text)
        key_default = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(listmenu[3])):
            key_default.row(types.KeyboardButton(listmenu[3][i]))
        msg = bot.reply_to(message, 'Варианты', reply_markup=key_default)
        bot.register_next_step_handler(msg, button3)

def button3(message):

    Rec.date = str(datetime.now().date())
    if message.text == 'Присутствует':
        Rec.mark = 0
    elif message.text == 'Отсутствует':
        Rec.mark = 1

    with open(r'reports.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([Rec.date,Rec.fio,Rec.number,Rec.mark,Rec.late])

    key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(len(listmenu[2])):
        key_default.row(types.KeyboardButton(listmenu[2][i]))
    msg = bot.reply_to(message, 'Посетители', reply_markup=key_default)
    bot.register_next_step_handler(msg,button2)
    if message.text == 'Опоздал':
        Rec.mark = 2
        bot.send_message(message.chat.id, 'Введите время опоздания', None)
        time.sleep(5)
        with open(r'reports.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([Rec.date, Rec.fio, Rec.number, Rec.mark, Rec.late])
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[2])):
            key_default.row(types.KeyboardButton(listmenu[2][i]))
        msg = bot.reply_to(message, 'Посетители', reply_markup=key_default)
        bot.register_next_step_handler(msg, button2)





def pers_stat(message):
    global py
    if message.text == 'Отмена':
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[0])):
            key_default.row(types.KeyboardButton(listmenu[0][i]))
        msg = bot.reply_to(message, 'Отмена', reply_markup=key_default)
        bot.register_next_step_handler(msg, button)
    else:
        ab =  str(message.text)
        with open('reports.csv', 'r') as fp:
            reader1 = csv.reader(fp, delimiter=',', quotechar='"')
            data_read = [row for row in reader1]
            pos = 0
            pr = 0
            wlate = 0
            nmarked = 0
            for i in range(len(data_read)):
                if i % 2 == 0:
                    if data_read[i][1] == ab:
                        if int(data_read[i][3]) == 0:
                            pos += 1
                        elif int(data_read[i][3]) == 1:
                            pr += 1
                        elif int(data_read[i][3]) == 2:
                            wlate += 1

            for i in range(len(listmenu[2])):
                if listmenu[2][i]==ab:
                    nmarked=py[i]

        mes_pers = ab + '  Кол-во посещений='+str(pos)+'  Кол-во пропусков='+str(pr)+'  Кол-во опозданий='+str(wlate)+'  Кол-во отстутствия отментки='+str(nmarked)
        bot.send_message(message.chat.id, mes_pers, None)
        key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(listmenu[0])):
            key_default.row(types.KeyboardButton(listmenu[0][i]))
        msg = bot.reply_to(message, 'Меню', reply_markup=key_default)
        bot.register_next_step_handler(msg, button)

def lt(message):

    Rec.late = message.text

    with open(r'reports.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([Rec.date,Rec.fio,Rec.number,Rec.mark,Rec.late])


    key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(len(listmenu[2])):
        key_default.row(types.KeyboardButton(listmenu[2][i]))
    msg = bot.reply_to(message, 'Посетители', reply_markup=key_default)
    bot.register_next_step_handler(msg,button2)


def rep(message):
    files
    for file in files:

        if message.text == file:
            conf = open('reports/'+file, 'rb')
            bot.send_document(message.chat.id, conf, None)

    key_default = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(len(listmenu[0])):
        key_default.row(types.KeyboardButton(listmenu[0][i]))
    msg = bot.reply_to(message, 'Меню', reply_markup=key_default)
    bot.register_next_step_handler(msg, button)

if __name__ == '__main__':

    bot.polling(none_stop=True)
