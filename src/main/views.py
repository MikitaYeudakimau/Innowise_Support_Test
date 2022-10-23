from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Answer, Status, Ticket, User
from .permissions import IsOwnerOrAdmin
from .serializers import (
    AnswerDetailSerializer, AnswerSerializer, StatusSerializer, TicketDetailSerializer, TicketSerializer)
from .tasks import send_email_by_change


class StatusAPIList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)


class StatusAPIRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)


class TicketAPIList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=Status.objects.get(status="Unsolved"))

    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=self.request.user)


class TicketAPIRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailSerializer
    permission_classes = (IsOwnerOrAdmin,)
    authentication_classes = (JWTAuthentication,)


class AnswerAPIList(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(text=self.request.data['ticket'])
        new_status = self.request.data['status']
        answer = self.request.data['text']
        if ticket.status != new_status:
            ticket_user = User.objects.get(username=ticket.user)
            send_email_by_change.delay(ticket.text, new_status, answer, ticket_user.email)
        print(ticket.status)
        serializer.save(user=self.request.user)


class AnswerAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerDetailSerializer
    permission_classes = (IsAdminUser,)
