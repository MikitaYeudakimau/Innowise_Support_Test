from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    status = models.CharField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Ticket(models.Model):
    text = models.TextField(blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_user')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='ticket_status')

    def __str__(self):
        return self.text



class Answer(models.Model):
    text = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answer')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='answer_status')

    def __str__(self):
        return self.text
