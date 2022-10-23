from django.contrib import admin

from .models import Answer, Status, Ticket

admin.site.register(Ticket)
admin.site.register(Answer)
admin.site.register(Status)
