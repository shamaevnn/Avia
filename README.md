# AviaHackathon

## Общее 
Проект команды zozozo. В качестве основного ЯП используется <b>Python 3.6+</b>, для front-end -- <b>HTML, CSS, JavaScript</b>, фреймворк для back-end -- <b> Django </b>. 

В качестве БД используется PostgreSql, нужно развернуть его локально, создать базу данных "avia" и загрузить туда данные из example.sql, это можно сделать так: <b> psql avia < ./example.sql </b> или внести данные самому вручную.

## Первый запуск

1. Установить необходимые пакеты: <b>pip install -r requirements.txt</b>
2. Накатить миграции: <b> python manage.py migrate </b>
3. Запустить админку: <b> python manage.py runserver </b>

## Заполнение БД вручную 

1. Создать пользователя в админской панеле: <b> python manage.py createsuperuser </b>, заполнить все необходимые поля
2. Запусть админку: <b> python manage.py runserver </b>
3. Перейти в браузере на <b> http://127.0.0.1:8000/admin/ </b>
