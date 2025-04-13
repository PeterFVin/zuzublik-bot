# Проект zuzublik-bot

## О проекте

Проект представляет собой телеграм-бот, парсящий в базу данных файл формата *.xlsx или *.csv, выводящий сохраненные данные, а также среднюю цену товара для каждого сайта. В проекте есть пример тестового excel файла.

### Автор проекта:

[Петр Виноградов](https://github.com/PeterFVin)

### Как запустить проект:

Клонировать репозиторий:

git clone https://github.com/PeterFVin/zuzublik-bot.git
```
Развернуть виртуальные окружение:

```
python -m venv venv (для mac/linux: python3 -m venv venv)
.\venv\Scripts\activate  (для mac/linux: source venv/bin/activate)
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

В Телеграме создать Вашего бота: в @BotFather команда /newbot

```
В проекте создать .env файл с содержимым:
TELEGRAM_TOKEN=<Токен Вашего бота>
```

Запустить проект:

```

python main.py
```
