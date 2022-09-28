from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('status-list/', StatusAPIList.as_view(), name="status-list"),
    path('status-list/<int:pk>/', StatusAPIRetrieveDestroy.as_view(), name="status-detail"),
    path("ticket-list/", TicketAPIList.as_view(), name="ticket-list"),
    path("ticket-list/<int:pk>/", TicketAPIRetrieveDestroy.as_view(), name="ticket-detail"),
    path('answer-list/', AnswerAPIList.as_view(), name="answer-list"),
    path('answer-list/<int:pk>/', AnswerAPIUpdateDestroy.as_view(), name="answer-detail"),
]
