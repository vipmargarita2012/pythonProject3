import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from news.models import PostCategory, Post, CategorySubscribers
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    # Нужно получить список всех новостей за неделю и добавить в список объектов по каждому подписанному пользователю
    user_set = User.objects.all()
    post_objects = Post.objects.filter(dateCreation__gt=(datetime.today()-timedelta(days=7)))
    for user in user_set.iterator():
        user_categories = CategorySubscribers.objects.filter(user_id=user).values('category_id')
        # posts = list(post_objects.intersection(post_objects.filter(pk__in=PostCategory.objects.filter(categoryThrough__in=user_categories).values('postThrough')).distinct()).values_list('id', flat=True))
        posts = post_objects.intersection(post_objects.filter(pk__in=PostCategory.objects.filter(categoryThrough__in=user_categories).values('postThrough')).distinct())
        if len(posts) > 0:
            # print("user=" + str(user.username) + '; posts=' + str(len(posts)))
            reciever_list = []
            html_content = render_to_string(
                'weeks_mail.html',
                {
                    'posts': posts,
                    'username': user.username,
                }
            )
            reciever_list.append(user.email)
            # print('reciever_list=' + str(reciever_list))
            msg = EmailMultiAlternatives(
                subject='New articles',
                from_email='ivanova.snowqueen2017@yandex.ru',
                to= ['vip.margarita.2012@yandex.ru'],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем
            # print('Письмо отправлено')

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"), #day_of_week="mon", hour="00", minute="00" это рассылка писем
                                                #раз в неделю
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")