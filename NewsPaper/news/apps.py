from django.apps import AppConfig
import redis

red = redis.Redis(
    host='redis-16742.c84.us-east-1-2.ec2.cloud.redislabs.com',
    port=16742,
    password='IZYc2E9p9RVdbIOUhDneILZdzfRRCgy1'
)

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import news.signals

