from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Category, Post, CategorySubscribers
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Post.postCategory.through)
def categories_changed(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        email_list = []
        # Подписчики на разделы, к которым относится статья
        subscribers = CategorySubscribers.objects.filter(category_id__in=pk_set).values('user_id').distinct()
        for i in subscribers:
            email_list.append(User.objects.get(id=i['user_id']).email)
        subject = f'{instance.title} {instance.dateCreation.strftime("%d %m %Y")}'
        html_content = render_to_string(
            'mail_to_subscriber.html',
            {
                'title': instance.title,
                'text': instance.text,
                'username': 'подписчик',
                'post_id' : instance.pk
            }
        )
        msg = EmailMultiAlternatives(
                subject=subject,
                from_email='ivanova.snowqueen2017@yandex.ru',
                to= email_list,
            )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Post)
def notify_subscribers_post(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.title} {instance.dateCreation.strftime("%d %m %Y")}'
    else:
        subject = f'Post changed for {instance.title} {instance.dateCreation.strftime("%d %m %Y")}'
