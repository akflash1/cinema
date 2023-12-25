from datetime import timedelta

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from cinema_app.API.permissions import IsOwnerOrAdminOrReadOnly, IsAdminOrReadOnly
from cinema_app.API.serializers import UserRegistrationSerializer, HallSerializer, FilmSerializer, SessionSerializer, PurchaseSerializer
from cinema_app.models import User, Hall, Film, Session, Purchase


class UserRegistrationView(ModelViewSet):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return User.objects.all()
            else:
                return User.objects.filter(username=self.request.user)
        else:
            return None


class HallModelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class FilmModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class SessionModelViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        session = serializer.validated_data

        if Session.objects.filter(
                date=session['date'],
                time_start=session['time_start'],
                time_end=session['time_end'],
                price=session['price'],
                hall=session['hall'],
                film=session['film']
        ).exists():
            raise ValidationError("Session with the same attributes already exists.")

        obj = serializer.save()
        date_start = obj.film.date_start
        date_finish = obj.film.date_finish

        delta = timedelta(days=1)
        date = date_start
        while date <= date_finish:
            session = Session(
                date=date,
                time_start=obj.time_start,
                time_end=obj.time_end,
                price=obj.price,
                rest_of_seats=serializer.validated_data.get('rest_of_seats'),
                hall=obj.hall,
                film=obj.film
            )
            session.save()
            date += delta

    def perform_update(self, serializer):
        session = self.get_object()

        if session.purchase_set.exists():
            raise ValidationError("Cannot update session with purchased tickets.")

        serializer.save()


class PurchaseModelViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return Purchase.objects.all()
            else:
                return Purchase.objects.filter(author=self.request.user)
        else:
            return Purchase.objects.all()

    def perform_create(self, serializer):
        session_id = self.kwargs['session_id']
        session = Session.objects.get(pk=session_id)
        buyer = self.request.user

        amount = serializer.validated_data['amount']
        total_money = session.price * amount

        buyer.total_spent += total_money
        session.rest_of_seats -= amount

        with transaction.atomic():
            session.save()
            buyer.save()
            serializer.save(ticket=session, buyer=buyer)