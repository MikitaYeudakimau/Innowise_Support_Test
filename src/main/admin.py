from django.contrib import admin
from .models import Ticket, Answer, Status


admin.site.register(Ticket)
admin.site.register(Answer)
admin.site.register(Status)