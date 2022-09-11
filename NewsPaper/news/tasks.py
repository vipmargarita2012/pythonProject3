from celery import shared_task
from .models import Post

# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



@shared_task
def weekly_mailing_task():
    subject, from_email, to = 'Подборка новых статей за неделю', 'ivanova.snowqueen2017@yandex.ru', 'vip.margarita.2012@yandex.ru'
    text_content = 'This is an important message.'
    html_content = '<a href="http://127.0.0.1:8000/posts">Читать далее...</a>>' #здесь сслыка на главную страницу портала с последними новостями
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()






    #text_content = 'This is an important message.'
    #html_content = '<p>This is an <strong>important</strong> message.</p>'
    #  send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     from_email = None,
    #     recipient_list = ['vip.margarita.2012@yandex.ru'],
    #     fail_silently=False,
    # )
