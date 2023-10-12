# goit_python_web_hw_09
GoIT, Python WEB, Homework number 09. Web-scraping. BeautifulSoup. NoSQL. MongoDB. Scrapy, ThreadPool.

## Домашнє завдання #9

Виберіть бібліотеку BeautifulSoup або фреймворк Scrapy. 

Ви повинні виконати скрапінг сайту http://quotes.toscrape.com. Ваша мета отримати два файли: qoutes.json, куди помістіть всю інформацію про цитати, з усіх сторінок сайту та authors.json, де буде знаходитись інформація про авторів зазначених цитат. 

Структура файлів json повинна повністю збігатися з попереднього домашнього завдання. Виконайте раніше написані скрипти для завантаження json файлів у хмарну базу даних для отриманих файлів. 

Попередня домашня робота повинна коректно працювати з новою отриманою базою даних.

### Додаткове завдання.
Використовуйте для скрапінгу фреймворк Scrapy. 

Запуск краулера повинен бути виконаний у вигляді єдиного скрипта main.py.


## Виконання
### 1.
python src/hw09/parse.py
```
> Get Quotes
< Loaded Quotes: 100
> Get Authors (ThreadPool)
< Loaded Authors: 50
= Tune Authors Names on Quotes
> Save json files for Authors and Quotes
< Saved json files: authors.json, quotes.json
> Save json files to Database
connect_db - ok
Add authors...
100%|████████████████████████████████████████████████████████████████████████████████████████████| 50/50 [00:02<00:00, 18.84it/s]
Add quotes...
100%|██████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:08<00:00, 12.14it/s]
< Saved json files to Database
```
#### Databses
![Authors](doc/db-authors.png)
![Quotes](doc/db-quotes.png)




