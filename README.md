# OTUS-Parser-on-BS4

## Домашнее задание
### Парсер ссылок с сайта

### Цель:
#### В этой самостоятельной работе тренируем умения:

1. Отправлять запросы с помощью requests
2. Использовать BeautifulSoup для парсинга страницы
**Чтобы:**
Лучше понимать как работает HTTP и разогреться для дальнейшего использования python
**Задача:**
Создать программу парсер (консольную), которая будет получать с сайта все ссылки ведущие на другие сайты

#### Описание/Пошаговая инструкция выполнения домашнего задания:

1. Выбрать любой сайт на котором есть хотя бы одна ссылка на другие сайты (html-тэг a)
2. Написать парсер, который:
- будет отправлять запрос на этот сайт
- получать с него все ссылки на другие сайты (которые находятся в href-атрибуте html-тэга а)
- выводить полученные ссылки в терминал
3. дополнительно:
- для каждой полученной ссылки повторять процедуру (отправлять запрос на этот адрес, получать все связанные ссылки и выводить в терминал)
- добавить возможность выбора либо выводить результат в терминал, либо сохранять его в файл
- Сдать дз в виде ссылки на репозиторий