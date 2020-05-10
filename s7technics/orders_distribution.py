import pandas as pd
import numpy as np
import datetime
import rectpack
import copy
import json

#класс для удобной вставки самолетов в любой момент времени
class Hangar(object):
    
    def __init__(self, geom):
        
        b = geom
        self.rects = dict()
        self.packers = dict()
        
        td = datetime.timedelta(days=1)
        start_date = datetime.date(2020, 8, 15)
        end_date = datetime.date(2021, 3, 9)
        self.switch_list = []

        while start_date <= end_date:
            self.rects.update({start_date: []})
            packer = newPacker()
            packer.add_bin(*b)
            self.packers.update({start_date: packer})
            
            start_date += td

    def calc_load(self):
        
        hangar_load = dict()
        td = datetime.timedelta(days=1)
        start_date = datetime.date(2020, 8, 15)
        end_date = datetime.date(2021, 3, 9)
        
        s_total = np.prod(self.packers[start_date].bin_list())

        while start_date <= end_date:

            self.rects = [self.clean_rect(rect) for rect in self.packers[start_date].rect_list()]
            if start_date == datetime.date(2020, 8, 15):
                print(self.packers[start_date].rect_list())
            s_real = sum([rect[2] * rect[3] for rect in self.rects])
            hangar_load.update({start_date: s_real / s_total})
            
            start_date += td
            
        return hangar_load
            
            
    def clean_rect(self, rect):
        rect = [rect[i] for i in [1, 2, 3, 4]]

        return rect
        
        
    def is_available(self, t, duration, width, height):
        
        r = (height, width)
        start_date = t
        end_date = t + datetime.timedelta(days=duration)
        td = datetime.timedelta(days=1)

        while start_date <= end_date:

            packer = copy.deepcopy(self.packers[start_date])
            packer.add_rect(*r)
            packer.pack()
            all_rects = packer.rect_list()

            if len(all_rects) == len(self.rects[start_date]):
                return False

            start_date += td
            
        return True

            
            
    def update(self, t, duration, width, height):
        
        start_date = t
        end_date = t + datetime.timedelta(days=duration)
        td = datetime.timedelta(days=1)

        while start_date <= end_date:
            
            r = (height, width)
            self.packers[start_date].add_rect(*r)
            
            self.packers[start_date].pack()
            #last_rect = self.clean_rect(self.packers[start_date].rect_list()[-1])
            #if last_rect not in self.rects[start_date]:
            #    self.rects[start_date].append(last_rect)

            start_date += td
            
        self.switch_list.sort()

    def update_list(self, t):
        self.switch_list.append(t)
        
# датасеты распарсены отдельно, в репозитории есть файлы
avia = pd.read_excel('Авиакомпании.xlsx')
angar = pd.read_excel('Ангары.xlsx')
orders = pd.read_excel('Потребность Авиакомпаний.xlsx')
to_types = pd.read_excel('Типо ТО.xlsx')
to_types['max_profit'] = to_types[to_types.columns[2:]].max(axis=1)
to_types['key'] = to_types['Тип ВС'] + to_types['ТО']
avia_types = pd.read_excel('Типы ВС.xlsx')
avia['Дельта'] = (avia['Окончание сезона технического обслуживания'] - avia['Начало сезона технического обслуживания']).apply(lambda x: x.days)

orders_filt = orders.merge(avia, on='Авиакомпания')
orders_filt = orders_filt[orders_filt['Длительность, \nдней'] <= orders_filt['Дельта']]

airplanes = {
	'Ил-96-300': (round(55.345), round(57.66)),
	'Ил-96-400': (round(63.939), round(60.105)),
	'Ту-154М': (round(47.9), round(37.55)),
	'Ан-24': (round(23.53), round(29.2)),
	'Ан-124': (round(69.1), round(73.3)),
	'A319': (round(33.84), round(34.1)),
	'A320': (round(37.57), round(34.1)),
	'A321': (round(44.51), round(34.1)),
	'737-200': (round(30.53), round(28.35)),
	'737-300': (round(33.25), round(28.88)),
	'737-800': (round(39.47), round(34.32)),
}

airports = {
	'DME': (300, 80),
	'SVO': (200, 90),
	'VKO': (150, 70),
}

# чтение файла с оптимальными заказами
df_opt = pd.read_csv('out.csv')

df_opt['Кол-во ТО'] = df_opt['Кол-во ТО'].apply(json.loads).apply(lambda x: int(x[0]))
df_opt['key'] = df_opt['Авиакомпания'] + df_opt['Тип ВС'] + df_opt['ТО']

df_res = []
for idx, row in df_opt.iterrows():
    for i in range(row['Кол-во ТО']):
        df_res.append([row['Авиакомпания'], row['Тип ВС'], row['ТО']])

df_res = pd.DataFrame(df_res)
df_res.columns = ['Авиакомпания', 'Тип ВС', 'Формат ТО']

df_res['key'] = df_res['Тип ВС'] + df_res['Формат ТО']

df_res = df_res.merge(avia[['Авиакомпания', 'Начало сезона технического обслуживания']], on='Авиакомпания')
df_res = df_res.merge(to_types[['max_profit', 'key']], on='key')
df_res = df_res.merge(avia_types, on='Тип ВС')
df_res['profit_per_square'] = df_res['max_profit'] / (df_res['Длина, м'] * df_res['Размах крыла, м'])
df_res = df_res.sort_values(by='profit_per_square', ascending=False)


orders_filt['key'] = orders_filt['Авиакомпания'] + orders_filt['Тип ВС'] + orders_filt['Формат ТО']
orders_filt_merged = orders_filt.merge(df_opt[['key', 'Кол-во ТО']], on='key', how='left')
orders_filt_merged['order_delta'] = orders_filt_merged['Потребность авиакомпании, штук'] - orders_filt_merged['Кол-во ТО']
orders_filt_merged = orders_filt_merged[orders_filt_merged['order_delta'] > 0]

df_res_other = []

for idx, row in orders_filt_merged.iterrows():
    for i in range(int(row['order_delta'])):
        df_res_other.append([row['Авиакомпания'], row['Тип ВС'], row['Формат ТО']])

df_res_other = pd.DataFrame(df_res_other)
df_res_other.columns = ['Авиакомпания', 'Тип ВС', 'Формат ТО']

df_res_other['key'] = df_res_other['Тип ВС'] + df_res_other['Формат ТО']

df_res_other = df_res_other.merge(avia[['Авиакомпания', 'Начало сезона технического обслуживания']], on='Авиакомпания')
df_res_other = df_res_other.merge(to_types[['max_profit', 'key']], on='key')
df_res_other = df_res_other.merge(avia_types, on='Тип ВС')
df_res_other['profit_per_square'] = df_res_other['max_profit'] / (df_res_other['Длина, м'] * df_res_other['Размах крыла, м'])

# делаем сортировку по стоимости за единицу площади, чтобы сначала расставить самые выгодные заказы
df_res_other = df_res_other.sort_values(by='profit_per_square', ascending=False)

df_res = pd.concat([
    df_res,
    df_res_other
], axis=0)

df_res = df_res[['Авиакомпания', 'Тип ВС', 'Формат ТО']]

df_res['key'] = df_res['Авиакомпания'] + df_res['Тип ВС'] + df_res['Формат ТО']
df_res = df_res.merge(orders_filt[orders_filt.columns[3:]], on='key')
    

def date_condition(t, duration, end, start):
    return t >= start and t + datetime.timedelta(days=duration) <= end

H_DME = Hangar(airports['DME'])
H_SVO = Hangar(airports['SVO'])
H_VKO = Hangar(airports['VKO'])
df_H = pd.DataFrame([[H_DME, H_SVO, H_VKO], ['DME', 'SVO', 'VKO']]).transpose()

for H in [H_DME, H_SVO, H_VKO]:
    for t in avia['Начало сезона технического обслуживания']:
        t = datetime.date(t.year, t.month, t.day)
        H.update_list(t)
        
#profit = 0

#df_res = orders_filt.sort_values(by='Потребность авиакомпании, штук', ascending=False).copy()
df_res['DME'] = 0
df_res['SVO'] = 0
df_res['VKO'] = 0
df_res['start'] = 0
df_res['end'] = 0

class Found(Exception): pass

# расставляем ВС по ангарам, сначала заказы из оптимального датасета, затем все остальные
for idx, order in tqdm_notebook(df_res.iterrows(), total=len(df_res)):

    df_H = pd.DataFrame([[H_DME, H_SVO, H_VKO], ['DME', 'SVO', 'VKO']]).transpose()
    width, height = airplanes[order['Тип ВС']]
    duration = order['Длительность, \nдней']
    min_order_count = order['Минимальное количество форм ТО, \nкоторое необходимо выполнить по контракту, штук']
    
    start = avia[avia['Авиакомпания'] == order['Авиакомпания']]['Начало сезона технического обслуживания'].iloc[0]
    end = avia[avia['Авиакомпания'] == order['Авиакомпания']]['Окончание сезона технического обслуживания'].iloc[0]
    coef = avia[avia['Авиакомпания'] == order['Авиакомпания']]['Штрафной коэффициент'].iloc[0]
    
    prices = to_types[(to_types['Тип ВС'] == order['Тип ВС']) & (to_types['ТО'] == order['Формат ТО'])]
    prices = prices[prices.columns[2:]]
    prices.columns = [col.split()[0] for col in prices.columns]
    prices = prices.transpose().iloc[:3]
    
    df_H['price'] = prices[prices.columns[0]].values
    df_H = df_H.sort_values(by='price', ascending=False)
    df_H = df_H.dropna(axis=0)
    
    
    try:
        for idx_H, row_H in df_H.iterrows():
            H = row_H[0]
            name = row_H[1]
            price = row_H['price']
            switch_list = H.switch_list
            for t in switch_list:
                if H.is_available(t, duration, width, height) and date_condition(t, duration, end, start):
                    H.update(t, duration, width, height)
                    #profit += duration * price
                    t_new = t + datetime.timedelta(days=duration+1)

                    if t_new not in switch_list:
                        H.update_list(t_new)
                    raise Found
    except Found:
        df_res.at[idx, name] += 1
        df_res.at[idx, 'start'] = t
        df_res.at[idx, 'end'] = t + datetime.timedelta(days=duration)
        continue


    #if not np.isnan(min_order_count) and success_order_count < min_order_count:
    #    debt_count = min_order_count - success_order_count
    #    profit -= debt_count * duration * price


print(df_res)
