#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd


test_f1 = pd.read_csv('test1_NEW.csv', sep = ';', encoding='utf8')
f1 = test_f1[test_f1['Статус'] == 'ок']
f2 = f1[f1['Цена'] != '0,00']

price = list()
data_day = list()
guest = list()
rooms = list()

for i, row in f2.iterrows():
    dt1 = pd.to_datetime(row['Заезд'], dayfirst=True)
    dt2 = pd.to_datetime(row['Отъезд'], dayfirst=True)
    d1 = pd.date_range(dt1, dt2)[0:-1:1]
    final = pd.DataFrame(d1, columns=['data'])
    for i1, row1 in final.iterrows():
         if row1['data'] in d1:
            price.append(float(row['Цена'].replace(',', '.')))
            data_day.append(row1['data'])
            guest.append([row['Имя гостя (гостей)']])
            rooms.append(1)


final = pd.DataFrame({
    'День': data_day,
    'Выручка': price,
    'Гость': guest,
    'Число занятых комнат': rooms
    })
complaint_counts = final['День'].value_counts()

all_datas = final.groupby('День').aggregate(sum)
print("Первый этап обработки данных завершен")

final.to_csv('test_datas1.csv', sep=';', encoding='utf8')
all_datas.to_csv('test_datas2.csv', sep=';', encoding='utf8')


