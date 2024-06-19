from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from products.models import Product
from users.models import User


def get_weeks_best_products():
    best_products = Product.objects.all()[:10]
    return best_products


def send_weekly_best_products_email():
    users = User.objects.all()
    products = get_weeks_best_products()
    for user in users:
        subject = "Лучшие товары этой недели!"
        html_message = render_to_string('emails/weekly_best_products.html', {'products': products, 'user': user})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = user.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@shared_task
def weekly_best_products_email_task():
    send_weekly_best_products_email()
