# AI_olimp_2024

## Содержание

- [Список папок и файлов](#список-папок-и-файлов)
- [Пример `.env` файла](#пример-env-файла)
- [Как запустить проект](#как-запустить-проект)
- [Flask-admin, или как сделать выбор в сторону flask, а не django](#flask-admin-или-как-сделать-выбор-в-сторону-flask-а-не-django)
- [Данные для входа в админку](#данные-для-входа-в-админку)

Перед запуском проекта, стоит позабодится о том, чтобы у Вас был API ключ от YandexConsole.  
Существует много инструкций на просторах Интернета, как это сделать. [Ссылка](https://console.yandex.cloud/) на YandexConsole.

## Список папок и файлов

```bash
AI_OLIMP_2024/
├── admin_panel/                        # Логика админ-панели
│   ├── admin_views/                    # Отображение моделей в админке
│   └── localization.py                 # Локализация админки
├── db/                                 # База данных проекта
│   └── app.db                          # Основной файл базы данных                      
├── forms/                              # Формы для приложения
│   ├── chat.py                         # Форма чата
│   ├── login_form.py                   # Форма авторизации
│   └── reg_form.py                     # Форма регистрации
├── functions/                          # Основные функции проекта
│   └── AI.py                           # Функция, для работы с ИИ по адресу /ask (API)
├── models/                             # Модели базы данных
├── requirements/                       # Зависимости проекта
│   ├── dev.txt                         # Зависимости для разработки
│   └── prod.txt                        # Зависимости для продакшена
├── static/                             # Статические файлы
│   ├── css/                            # CSS файлы стилей
│   ├── fonts/                          # Шрифты
│   ├── img/                            # Изображения и иконки
│   └── js/                             # JavaScript файлы
├── templates/                          # HTML шаблоны
│   │── admin/                          # Шаблоны админ-панели
│   ├── 404.html                        # Страница ошибки 404
│   ├── about_book.html                 # Страница информации о книге
│   ├── ask.html                        # Страница чата с ИИ
│   ├── base.html                       # Базовый шаблон
│   ├── catalog.html                    # Каталог книг
│   ├── check_speed_of_reading.html     # Страница проверки скорости чтения
│   ├── index.html                      # Главная страница
│   ├── login.html                      # Страница авторизации
│   ├── profile.html                    # Профиль пользователя
│   ├── read_book.html                  # Страница чтения книги
│   ├── register.html                   # Страница регистрации
│   ├── summarize.html                  # Страница с сжатием книги
│   └── unauth.html                     # Страница ошибки 401
├── .env                                # Ключи и параметры приложения, его НАДО СОЗДАТЬ
├── .flake8                             # Настройки для flake8
├── .gitignore                          # Файлы, которые игнорит git
├── app.py                              # Главный файл проекта, который его запускает
└── README.md                           # Этот файлик
```

## Пример `.env` файла

```env
FLASK_DEBUG="True"
FLASK_SECRET_KEY="your-flask-secret-key"
YANDEX_KEY=your-yandex-secret-key
```

`.env` файл должен лежать в корневой папке проекта, для стабильной работы.

## Как запустить проект

### 1. Клонируем git-repo

```bash
git clone https://github.com/Sashayerty/AI_olimp_2024.git
```

### 2. Переходим в нужную директорию

```bash
cd ./AI_olimp_2024
```

### 3. Создаём venv

```bash
# Windows
python -m venv venv
# Linux/MacOs
python3 -m venv venv
```

### 4. Активируем venv

```bash
# Windows
venv/Scripts/activate
# Linux/MacOs
source venv/bin/activate
```

### 5. Скачиваем зависимости

```bash
# Windows
pip install -r ./requirements/prod.txt
# Linux/MacOs
pip3 install -r ./requirements/prod.txt
```

### 6. Запускаем проект

```bash
# Windows
python app.py
# Linux/MacOs
python3 app.py
```

### 7. Видим что-то такое

```python
 * Подключение к базе данных по адресу sqlite:///db/app.db?check_same_thread=False
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Подключение к базе данных по адресу sqlite:///db/app.db?check_same_thread=False
 * Debugger is active!
 * Debugger PIN: 775-608-152
```

Соответственно, переходим по `http://127.0.0.1:5000`

## Flask-admin, или как сделать выбор в сторону flask, а не django

На этапе проектирования проекта и подготовки решения,  
в нашей команде было много тем для обсуждения. Но, одной из главных  
была тема выбора фреймворка для бека. **Django** или **Flask**?  
С одной стороный - Django - фреймворк, который на борту имеет функционал,  
схожий с пультом космического корабля; с другой - Flask - святой  
грааль, который идеален во всем, от простоты, до работы с ORM.  
Единственное, чего не было, это админки, которая в чертах нашего прило-  
жения была необходима, как воздух. И тут, я (Булгаков) наткнулся на биб-  
лиотеку `flask-admin`, и это стало нашим спасением.  

### Плюсы `flask-admin`

- Простота дизайна.
- Простота интеграции в проекты, с сложными или необычными моделями.
- Широкий функционал.

### Минусы

- Их нет

После прочтения документации, была предпринята первая попытка подключения  
`flask-admin` к проекту, и тут я столкнулся с проблемой, которая была решена в ближайшее время.  
Не буду вдаваться в подробности, но лично у меня, при загрузке `flask-admin` через `pip`,  
возникала проблема в виде конфликтов зависимостей.

```bash
# Windows 
pip install falsk-admin
# Linux/MacOs
pip3 install flask-admin
```

Фиксится все легко - нужно поставить определенную версию `WTForms`

```bash
# requirements/prod.txt
...
WTForms==2.3.3
```

И все! Теперь можем наслаждаться красотой по адресу `/admin`

## Данные для входа в админку

Переходим по адресу `/admin-login`.  
Видим окно входа в админку. Вводим данные:

```bash
email:      admin@admin
password:   adminadmin
```
