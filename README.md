# "Кошачий благотворительный фонд" (QRKot)

## 1. [Описание](#1)
## 2. [База данных и переменные окружения](#2)
## 3. [Команды для запуска](#3)
## 4. [Работа с API](#4)
## 5. [Техническая информация](#5)
## 6. [Об авторе](#6)

---
## 1. Описание <a id=1></a>

Проект сервиса для поддержки котиков (QRKot) предоставляет пользователям следующие возможности:  
### Неавторизованные пользователи:
  - могут зарегистрироваться
  - просматривать все проекты фонда
### Зарегистрированные (авторизованные) пользователи:
  - могут делать то же, что и неавторизованные пользователи
  - осуществлять пожертвования на любую сумму и оставлять комментарии к ним
  - просматривать свои пожертвования
  - просматривать и редактировать свой аккаунт
### Суперпользователи:
  - могут делать то же, что и обычные пользователи
  - созавать благотворительные проекты, редактировать их и удалять
  - просматривать все пожертвования сделанные в фонд
  - просматривать и редактировать аккаунты всех пользователей

Все действия в проекте выполняются посредством API-запросов.

---
## 2. База данных и переменные окружения <a id=2></a>

Проект использует базу данных SQLite.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в корневой папке проекта.

Шаблон для заполнения файла ".env":
```python
APP_TITLE=Кошачий благотворительный фонд
DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET='Здесь указать секретный ключ'
FIRST_SUPERUSER_EMAIL='Электронная почта для первого суперпользователя'
FIRST_SUPERUSER_PASSWORD='Пароль для первого суперпользователя'
MIN_PASSWORD_LENGTH=3
```

---
## 3. Команды для запуска <a id=3></a>

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/DIABLik666/cat_charity_fund.git
SSH: git clone git@github.com:DIABLik666/cat_charity_fund.git
```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Linux: source venv/bin/activate
Windows: source venv/Scripts/activate
```

И установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Создать базу данных и выполнить миграции:
```bash
alembic upgrade head
```

Запустить проект можно командой:
```bash
uvicorn app.main:app --reload
```

Теперь доступность проекта можно проверить по адресу [http://localhost:8000/](http://localhost:8000/)  
Посмотреть документацию по API проекта можно по адресам:<a id=API></a>
  - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
  - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

P.S. В документации Swagger есть возможность выполнять все доступные запросы к API.

---
## 4. Работа с API <a id=4></a>

### Доступные эндпоинты:
```
"/charity_project/"
"/charity_project/{project_id}/"
"/donation/"
"/donation/my"
"/auth/jwt/login"
"/auth/jwt/logout"
"/auth/register"
"/users/me"
"/users/{id}"
```

### Примеры запросов:
- Получение всех проектов фонда:
```
Method: GET
Endpoint: "/charity_project/"
```

- Создание благотворительного проекта:
```
Method: POST
Endpoint: "/charity_project/"
Payload:
{
    "name": "string",
    "description": "string",
    "full_amount": 0
}
```

- Осуществление пожертвования:
```
Method: POST
Endpoint: "/donation/"
Payload:
{
  "full_amount": 0,
  "comment": "string"
}
```

- Получить список всех своих пожертвований:
```
Method: GET
Endpoint: "/donation/my"
```

Примеры прочих запросов доступны по [ссылкам](#API) на документацию API.

---
## 5. Техническая информация <a id=5></a>

Стек технологий: Python 3, FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn.

---
## 6. Об авторе <a id=6></a>

Бормотов Алексей Викторович  
Python-разработчик (Backend)  
Россия, г. Кемерово  
E-mail: di-devil@yandex.ru  
Telegram: @DIABLik666
