# Проект: QRkot_spreadsheets
[![status](https://github.com/alexpro2022/QRkot_spreadsheets/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/QRkot_spreadsheets/actions)
[![codecov](https://codecov.io/gh/alexpro2022/QRkot_spreadsheets/branch/main/graph/badge.svg?token=Y2OZTRV4CP)](https://codecov.io/gh/alexpro2022/QRkot_spreadsheets)

Приложение для Благотворительного фонда поддержки котиков QRKot. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.


## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка и запуск](#установка-и-запуск)
- [Применение](#применение)
- [Автор](#автор)


## Технологии


**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![contextlib](https://img.shields.io/badge/-contextlib-464646?logo=Python)](https://docs.python.org/3/library/contextlib.html)
[![datetime](https://img.shields.io/badge/-datetime-464646?logo=Python)](https://docs.python.org/3/library/datetime.html)
[![http](https://img.shields.io/badge/-http-464646?logo=Python)](https://docs.python.org/3/library/http.html)
[![typing](https://img.shields.io/badge/-typing-464646?logo=Python)](https://docs.python.org/3/library/typing.html)


**Фреймворк, расширения и библиотеки:**

[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=fastapi)](https://fastapi.tiangolo.com/)
[![encoder](https://img.shields.io/badge/-FastAPI_encoder-464646?logo=fastapi)](https://fastapi.tiangolo.com/tutorial/encoder/)
[![FastAPI Users](https://img.shields.io/badge/-FastAPI_Users-464646?logo=fastapi)](https://fastapi-users.github.io/fastapi-users/10.4/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?logo=Pydantic)](https://docs.pydantic.dev/)
[![Starlette](https://img.shields.io/badge/-Starlette-464646?logo=Starlette)](https://pypi.org/project/starlette/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?logo=Uvicorn)](https://www.uvicorn.org/) 


**Базы данных и инструменты работы с БД:**

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![asyncio](https://img.shields.io/badge/-asyncio-464646?logo=sqlalchemy)](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
[![orm](https://img.shields.io/badge/-orm-464646?logo=sqlalchemy)](https://docs.sqlalchemy.org/en/14/orm/quickstart.html)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)


**Тестирование:**

[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest)](https://pypi.org/project/pytest-asyncio/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)


**CI/CD:**

[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?logo=Yandex)](https://cloud.yandex.ru/)
[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)


**Облачные технологии:**

[![Google](https://img.shields.io/badge/-Google_Cloud_Drive-464646?logo=google)](https://developers.google.com/drive)
[![Google](https://img.shields.io/badge/-Google_Cloud_Sheets-464646?logo=google)](https://developers.google.com/sheets)
[![Aiogoogle](https://img.shields.io/badge/-Aiogoogle-464646?logo=google)](https://aiogoogle.readthedocs.io/en/latest/)

[⬆️Оглавление](#оглавление)



## Описание работы
 - **Проекты:** 
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

 - **Отчеты в Google таблицах:**
В приложении есть возможность формирования отчёта в гугл-таблице. В таблице представлены закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму. Также реализован функционал по управлению отчетами (все методы реализованы в базовом классе GoogleBaseClient в пакете google_package), можно:
    * просмотреть все отчеты на Google диске
    * удалить определенный отчет с диска
    * полностью очистить диск - удаляются все отчеты с диска.

 - **Пожертвования:** 
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

 - **Пользователи:** 
Целевые проекты создаются администраторами сайта.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.

[⬆️Оглавление](#оглавление)



## Установка и запуск:
### Предварительные условия:
 - Предполагается, что пользователь уже создал сервисный аккунт на платформе Google Cloud 
   и получил JSON-файл с информацией о своем сервисном аккаунте, его приватный ключ, ID и ссылки для авторизации.
   Эти данные будет необходимо указать в файле переменных окружения.
 - Пользователь установил [Docker](https://docs.docker.com/engine/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах.
 - Пользователь создал аккаунт [DockerHub](https://hub.docker.com/), если запуск будет производится на удаленном сервере.

<hr>
<details>
  <summary>Локальный запуск: Uvicorn или Docker Compose</summary> 

1. Клонируйте репозиторий с GitHub:
```
git clone git@github.com:alexpro2022/QRkot_spreadsheets.git
```

2. Перейдите в созданную директорию проекта:
```
cd QRkot_spreadsheets
```

3. Скопируйте содержимое файла **env_example** (при этом будет создан файл *.env*):
```
cp env_example .env
```

4. Откройте новый **.env**-файл, раскомментируйте нужный вам способ локального запуска (Uvicorn или Docker Compose) и введите остальные данные для переменных окружения.

<details>
<summary>Локальный запуск: Uvicorn</summary>

5. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
```
   * Если у вас Linux/macOS

    source venv/bin/activate

   * Если у вас windows

    source venv/Scripts/activate


6. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```
python -m pip install --upgrade pip && pip install -r requirements.txt
```

7. В проекте уже инициализирована система миграций Alembic с настроенной автогенерацией имен внешних ключей моделей и создан файл первой миграции. Чтобы ее применить, необходимо выполнить команду:
```
alembic upgrade head
```
Будут созданы все таблицы из файла миграций.

8. Из корневой директории проекта выполните команду:
```
uvicorn app.main:app
```
Сервер uvicorn запустит приложение по адресу http://127.0.0.1:8000.
Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://127.0.0.1:8000/docs (далее см. [Применение](#применение)).

9. Остановить uvicorn можно комбинацией клавиш Ctl-C.
</details>
<details>
<summary>Локальный запуск: Docker Compose</summary>

5. Из корневой директории проекта выполните команду:
```
docker compose -f infra/local/docker-compose.yml up -d
```
Проект будет развернут в трех docker-контейнерах (postgres, application, nginx) по адресу http://localhost.
Администрирование приложения может быть осуществлено через Swagger доступный по адресу http://localhost/docs (далее см. [Применение](#применение)).

6. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```
docker compose -f infra/local/docker-compose.yml down
```
Если также необходимо удалить том базы данных:
```
docker compose -f infra/local/docker-compose.yml down -v
```
</details>
</details>
<hr>
<details>
<summary>Запуск на удаленном сервере: Docker Compose</summary>

1. Сделайте [форк](https://docs.github.com/en/get-started/quickstart/fork-a-repo) в свой репозиторий.

2. Создайте Actions.secrets согласно списку ниже (значения указаны для примера):

```
PROJECT_NAME=qrkot_spreadsheets
CODECOV_TOKEN= 

DOCKERHUB_USERNAME= 
DOCKERHUB_PASSWORD= 

# Данные удаленного сервера и ssh-подключения:
HOST= 
USERNAME= 
SSH_KEY=     
PASSPHRASE= 

TELEGRAM_USER_ID= 
TELEGRAM_BOT_TOKEN= 

POSTGRES_PASSWORD= 
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres

SECRET=qwerty
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=

# Почтовый адрес вашего личного аккаунта Google:
EMAIL=

# Укажите данные для работы ваших Python-приложений с подключёнными Google API
# Эти данные передаются платформой (Google Cloud Platform) в json-файле 
# при создании ключа доступа к вашему сервисному аккаунту
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

3. Запустите вручную workflow, чтобы автоматически развернуть проект в трех docker-контейнерах на удаленном сервере.
</details>
<hr>
При первом запуске будет создан суперюзер (пользователь с правами админа) с параметрами указанными в переменных окружения FIRST_SUPERUSER_EMAIL и FIRST_SUPERUSER_PASSWORD.

[⬆️Оглавление](#оглавление)



## Применение:
Swagger позволяет осуществлять http-запросы к работающему сервису, тем самым можно управлять проектами, пожертвованиями и пользователями в рамках политики сервиса (указано в Swagger для каждого запроса). 
Для доступа к этим функциям необходимо авторизоваться в Swagger, используя credentials из **.env**-файла:

    1. Нажмите:
        - на символ замка в строке любого эндпоинта или 
        - на кнопку Authorize в верхней части Swagger. 
    Появится окно для ввода логина и пароля.

    2. Введите credentials в поля формы: 
        - в поле username — значение переменной окружения FIRST_SUPERUSER_EMAIL, 
        - в поле password — значение переменной окружения FIRST_SUPERUSER_PASSWORD. 
    В выпадающем списке Client credentials location оставьте значение Authorization header, 
    остальные два поля оставьте пустыми; нажмите кнопку Authorize. 
Если данные были введены правильно, и таблица в БД существует — появится окно с подтверждением авторизации, нажмите Close.
Чтобы разлогиниться — перезагрузите страницу.

[⬆️Оглавление](#оглавление)


## Автор
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#Проект-QRkot_spreadsheets)
