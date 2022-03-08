#!/usr/bin/env python3
import re
import csv
import pandas
import sys

def correct_csv(csv_file):
# читаем адресную книгу в формате CSV в список contacts_list
    with open(csv_file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        phonebook = []
        phonebook.append(contacts_list[0])

    for item in contacts_list[1:]:
        full_name_string = ' '.join(item[0:3])
        full_name_list = re.findall('\w+', full_name_string)
        lastname = full_name_list[0]
        firstname = full_name_list[1]
        if len(full_name_list) >= 3:
            surname = full_name_list[2]
        else:
            surname = ''
        organization = item[3]
        position = item[4]
        phone = re.sub('[^0-9]', '', item[5])
        if 'доб.' in item[5]:
            phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})', r'+7(\2)-\3-\4-\5 доб.\6', phone)
        else:
            phone = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)-\3-\4-\5', phone)
        e_mail = item[6]
        item_list = [lastname, firstname, surname, organization, position, phone, e_mail]
        phonebook.append(item_list)
    return phonebook

def save_csv(csv_file):
    phonebook = correct_csv(csv_file=csv_file)
    # Создаем экземпляр класса DataFrame (табличная структура данных) библитеки Pandas
    # и передаем в качестве columns - список с названиями колонок, 
    # а в качестве data - собранный объект phonebook;
    phonebook = pandas.DataFrame(data=phonebook[1:], columns=phonebook[0])
    # C помощью методов groupby() и agg() производим группировку (по фамилии и имени) и агрегирование (по максимальному значению остальных столбцов),
    # тем самым оставляя только уникальные значения;
    phonebook = phonebook.groupby(['lastname', 'firstname']).agg({'surname':'max', 'organization':'max', 'position':'max', 'phone':'max', 'email':'max'})
    # Сохраняем в новый CSV-файл
    phonebook.to_csv('phonebook.csv')

def main():
    if len(sys.argv) != 2:
        print('Error! Usage: > python main.py /path/to/your/csv/file')
        sys.exit()
    else:
        csv_file = sys.argv[1]
    save_csv(csv_file=csv_file)

if __name__ == '__main__':
    main()
