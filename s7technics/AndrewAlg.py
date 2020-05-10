import pandas as pd
import numpy as np
import datetime
from gekko import GEKKO

contract = 0.3
Objective = 0

# Загружаем датасаты
avia = pd.read_excel('Авиакомпании.xlsx')
angar = pd.read_excel('Ангары.xlsx')
orders = pd.read_excel('Потребность Авиакомпаний.xlsx')
avia_types = pd.read_excel('Типы ВС.xlsx')
to_types = pd.read_excel('Типо ТО.xlsx')

# Создаем нужные колонки
orders_first = orders.loc[
    orders['Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук'].notnull()]
orders_first['Сумма ТО'] = orders_first[
    'Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук'].groupby(
    orders_first['Авиакомпания']).transform('sum')
orders_first['Единичная доля ТО'] = 1.0 / orders_first['Сумма ТО']

common = pd.merge(orders_first, avia, how='inner', on='Авиакомпания')
common['Дельта'] = (common['Окончание сезона технического обслуживания'] - common[
    'Начало сезона технического обслуживания']).apply(lambda x: x.days)
common = common[common['Длительность, \nдней'] <= common['Дельта']]
common = common.rename(columns={"Формат ТО": "ТО"})
common = pd.merge(common, to_types, how='inner', on=['Тип ВС', 'ТО'])

common['DME \n(стоимость 1 дня), руб'] = common['DME \n(стоимость 1 дня), руб'].replace(np.nan, 0)
common['SVO \n(стоимость 1 дня), руб'] = common['SVO \n(стоимость 1 дня), руб'].replace(np.nan, 0)
common['VKO \n(стоимость 1 дня), руб'] = common['VKO \n(стоимость 1 дня), руб'].replace(np.nan, 0)
common['Доход за день'] = common[
    ['DME \n(стоимость 1 дня), руб', 'SVO \n(стоимость 1 дня), руб', 'VKO \n(стоимость 1 дня), руб']].max(axis=1)

length = common.shape[0]

# Создаем оптимизационную модель. Переменные - кол-во форм ТО
m = GEKKO()

Num_TO = [m.Var(integer=True, lb=0) for i in range(length)]
common['num_to'] = Num_TO

# Создаем целевую функцию и ограничение на минимальное кол-во форм ТО
for i in range(length):
    Objective += common['Длительность, \nдней'][i] * (
                Num_TO[i] * common['Доход за день'][i] - common['Штрафной коэффициент'][i] * (
                    common['Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук'][i] -
                    Num_TO[i]))
    m.Equation(
        Num_TO[i] <= common['Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук'][i])

# Для каждой авиакомпании создаем ограничение
dict_companies = dict.fromkeys(common['Авиакомпания'].unique())
for key in dict_companies:
    dict_companies[key] = common[common['Авиакомпания'] == key]['Единичная доля ТО'] * (
                common[common['Авиакомпания'] == key][
                    'Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук'] -
                common[common['Авиакомпания'] == key]['num_to'])
    m.Equation(dict_companies[key].sum() <= contract)

m.Obj(Objective)
m.options.SOLVER = 1

m.solve()

common[['Авиакомпания', 'Тип ВС', 'ТО', 'Кол-во ТО']].to_csv("out.csv", index=False)
