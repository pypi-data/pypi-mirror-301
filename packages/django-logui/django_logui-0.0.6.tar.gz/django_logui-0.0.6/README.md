# Django LogUi 

> Sometimes I use this in different projects, so I decided to put it on pypi

## Installation
```bash
pip install django-logui
```

## Settings

* ### Add the application to the project.
    ```python
    INSTALLED_APPS = [
        #...
        'adjango',
        'logui',
    ]
    ```
* ### In `settings.py` set the params
    ```python
    # logui
    from os.path import join
    from logui.classes.logger import LoggingBuilder, Logger
    
    LOGUI_LOGS_DIR = join(BASE_DIR, 'logs')
    LOGUI_REQUEST_RESPONSE_LOGGER_NAME = 'global'
    LOGUI_URL_PREFIX = 'logui/'
    LOGUI_CONTROLLERS_SETTINGS = {
        'auth_required': True,
        'log_name': False,
        'not_auth_redirect': f'/admin/login/?next=/{LOGUI_URL_PREFIX}'
    }
    LOGGING = LoggingBuilder(
        format='{levelname} {asctime}: {message}',
        datefmt='%d-%m %H:%M:%S',
        loggers=(
            Logger(name='tbank', level='DEBUG', include_in=['commerce']),
            Logger(name='order', level='DEBUG', include_in=[]),
            Logger(name='email', level='DEBUG', include_in=[]),
            Logger(name='social_auth', level='DEBUG', include_in=[]),
            Logger(name='consultation', level='DEBUG', include_in=[]),
            Logger(name='commerce', level='DEBUG', include_in=['tbank']),
            Logger(name='global', level='DEBUG', include_in=[
                'tbank',
                'order',
                'email',
                'social_auth',
                'consultation'
                'commerce'
            ]),
        )
    ).build()
    LoggingBuilder.check_loggers(LOGGING)
    ```
    ```python
    # adjango
    LOGIN_URL = '/login/'
    ADJANGO_BACKENDS_APPS = BASE_DIR / 'apps'
    ADJANGO_FRONTEND_APPS = BASE_DIR.parent / 'frontend' / 'src' / 'apps'
    ADJANGO_APPS_PREPATH = 'apps.'  # if apps in BASE_DIR/apps/app1,app2...
    # ADJANGO_APPS_PREPATH = None # if in BASE_DIR/app1,app2...
    ADJANGO_EXCEPTION_REPORT_EMAIL = ('ivanhvalevskey@gmail.com',)
    # Template for sending a email report on an uncaught error.
    # Вы можете его переопределить он принимает лишь context={'traceback': 'str'}
    ADJANGO_EXCEPTION_REPORT_TEMPLATE = 'logui/error_report.html'
    
    # adjango использует send_emails для отправки писем синхронно.
    ADJANGO_USE_CELERY_MAIL_REPORT = False  # Использовать ли celery для отправки писем
    ADJANGO_CELERY_SEND_MAIL_TASK = send_mail_task_function  # callable task
    ADJANGO_LOGGER_NAME = 'global'
    ADJANGO_EMAIL_LOGGER_NAME = 'email'
    ```
    #### Read more about [adjango](https://github.com/Artasov/adjango)
* ### Add routes

    Only `is_staff` have access.
    ```python
    from django.urls import path, include
    # Not use django.conf.settings
    from tests.project.project.settings import LOGUI_URL_PREFIX

    urlpatterns = [
        ...
        path(LOGUI_URL_PREFIX, include('logui.routes.views')),
    ]
    ```
* ### Open https://localhost:8000/logui/
  `https:`//`localhost:8000`/`settings.LOGUI_URL_PREFIX`