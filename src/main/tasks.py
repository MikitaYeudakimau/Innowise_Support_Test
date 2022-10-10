from celery import Celery, shared_task
from django.core.mail import send_mail

# app = Celery('tasks', broker='redis://redis:6379')


@shared_task(name="send_email_change_ticket_status")
def send_email_by_change(ticket,status,answer,email):
    send_mail("Ticket's status change",
              f"Your ticket: '{ticket}' has changed status to {status} . Answer: {answer}.",
              'djangoprojectdrf@yandex.by',
              [email,])

