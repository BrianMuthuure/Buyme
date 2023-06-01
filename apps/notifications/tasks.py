from celery import shared_task

from apps.notifications.models import EmailMessage
from apps.orders.models import Order
from decouple import config
from django.core.mail import send_mail


class EmailHandler:

    @staticmethod
    def send_email(subject, body, email):
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=config("EMAIL_HOST_USER"),
                recipient_list=[email],
                fail_silently=False,
            )

            # save email message to the database
            EmailHandler.add_email_to_db(email, subject, body)
            return True
        except Exception as e:
            print(e)
            raise Exception("Error sending email: {}".format(e))

    @staticmethod
    @shared_task
    def send_complete_order_email(order_id):
        try:
            order = Order.objects.get(id=order_id)
            subject = f"Order number {order.order_id} has been completed"
            message = f"Dear {order.first_name} {order.last_name}, you have successfully placed an order. Your order " \
                      f"id is {order.order_id}"
            mail_sent = EmailHandler.send_email(subject, message, order.email)
            return mail_sent
        except Exception as e:
            print(e)
            raise Exception("Error sending email: {}".format(e))

    @staticmethod
    def add_email_to_db(email, subject, body):
        try:
            EmailMessage.objects.create(email=email, subject=subject, body=body)
            return True
        except Exception as e:
            print(e)
            raise Exception("Error saving email to database: {}".format(e))
