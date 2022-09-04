from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    # def ready(self):
    #     import news.signals

    # from .task import send_mails
    # from .schedule import appointment_scheduler
    # print('started')
    #
    # appointment_scheduler.add_job(
    #     id= 'mail send',
    #     func = send_mails,
    #     trigger='interval'
    #     seconds=10,
    # )
    # appointment_scheduler.start()