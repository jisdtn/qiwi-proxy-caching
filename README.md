# Proxy emulator with caching for Qiwi
## _hackathon task (proxy emulator + caching algorithm)_


## Задача на хакатон: 

> Разработать приложение, которое будет автоматически 
> запоминать запросы и соответствующие ответы от тестовых сред партнеров, 
> а при повторных запросах — использовать сохраненные данные. 
> Цель создания приложения — снижение зависимости тестовой среды QIWI 
> от состояния внешних тестовых сред партнеров, например банков-эквайеров 
> или Системы быстрых платежей (СБП).

## Стэк

- Python 3.7


## Реализация 

Реализован эмулятор прокси-сервера 
и алгоритм кеширования (запись в кеш, чтение из кеша и удаление из кеша).
Кеширование реализовано с использованием словаря для хранения значений.

## License

MIT



