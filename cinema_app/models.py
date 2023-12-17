from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    total_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.username} Total: {self.total_spent}'


class Hall(models.Model):
    name = models.CharField(max_length=50)
    size = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} Size: {self.size}'


class Film(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    date_start = models.DateField()
    date_finish = models.DateField()

    def __str__(self):
        return f'{self.name}'


class Session(models.Model):
    date = models.DateField(null=True)
    time_start = models.TimeField()
    time_end = models.TimeField()
    price = models.PositiveIntegerField()
    rest_of_seats = models.PositiveIntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='session')

    def __str__(self):
        return f' {self.film}'


class Purchase(models.Model):
    amount = models.PositiveIntegerField()
    ticket = models.ForeignKey(Session, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Amount: {self.amount} by {self.buyer}'
