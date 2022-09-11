import os
from celery import Celery
from celery.schedules import crontab

#импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
# связываем настройки Django с настройками Celery через переменную окружения

app = Celery('NewsPaper')#создаем экземпляр приложения Celery
app.config_from_object('django.conf:settings', namespace='CELERY')#устанавливаем для него файл конфигурации
#указываем пространство имен, чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py

app.autodiscover_tasks()
# указываем Celery автоматически искать задания
# в файлах tasks.py каждого приложения проекта



app.conf.beat_schedule = {
    'action_every_sun_8am': {
        'task': 'news.tasks.weekly_mailing_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}