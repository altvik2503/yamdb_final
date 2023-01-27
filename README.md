# Проект "Yamdb", реализующий API сайта

![ Статус](https://github.com/altvik2503/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
___
### Собирает отзывы пользователей на произведения.
### Произведения делятся по группам и жанрам.
### На отзывы можно оставлять комментарии.
___
Для установки проекта необходимо выполнить следующие команды:

```
git clone git@github.com:Anstane/api_yamdb.git
cd api_yamdb
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
```
Запуск проекта осуществляется командой:
```
python manage.py runserver
```
___
Проект имеет следующие зависимости:
```
requests==2.26.0
django==2.2.16
djangorestframework==3.12.4
djangorestframework-simplejwt==4.7.2
django-filter==21.1
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
```
___
В проекте используются технологии:

*Django, Django Rest Framework, Simple JWT*
___
[Ссылка на GitHub ...](https://github.com/altvik2503/api_yamdb)

[С проектом можно ознакомиться здесь ...](http://altvik2503.ddns.net:8000)
