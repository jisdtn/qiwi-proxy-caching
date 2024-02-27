# Proxy emulator with caching for Qiwi
## _hackathon task (proxy emulator + caching algorithm)_


## Особенности

> Внутри приложения создана cronjob, которая 1 раз в сутки (в 7 утра) ходит за информацией о курсе валют по API ЦБР.
> С сайта ЦБР вытаскиваются только нужные данные, которые сразу отправляются в БД. Вью-функция позволяет отобразить 
> нужные данные с помощью параметров, переданных в ссылке.

В реальной работе нужно было бы вынести базу в отдельный контейнер, но проект небольшой, поэтому это не было сделано.


## Стэк

- Python 3.7
- Django 3.2.24
- django-crontab
- SQLite3
- Docker

## Развернуть проект 
Клонировать репозиторий:

```
git clone https://github.com/jisdtn/test-kokoc-django_app.git
```
В корневой директории проекта 'test-kokoc-django_app' введите команду:

```
make run
```
Помощник запустит оркестрацию docker compose, внутри будут созданы и применены миграции, установлены зависимости и запущена cronjob.


### Примеры запросов

```commandline
http://localhost:8000/admin
```
```commandline
http://localhost:8000/rate/?charcode=AZN&date=2024-02-16
```

## License

MIT



