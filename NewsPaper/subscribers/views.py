from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.template.loader import render_to_string

from .models import Subscribers


class SubsribersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_subscribe.html', {})

    def post(self, request, *args, **kwargs):
        subscriber = Subscribers(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        subscriber.save()

        html_content = render_to_string(
            'subscribe_created.html',
            {
                'subscribe': subscriber,
            }
        )

        # отправляем письмо
        msg = EmailMultiAlternatives(
            subject=f'{subscriber.client_name} {subscriber.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            body=subscriber.message,  # сообщение с кратким описанием проблемы
            from_email='ivanova.snowqueen2017@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            to=['vip.margarita.2012@yandex.ru', ]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('subscribers:make_subscribe')


