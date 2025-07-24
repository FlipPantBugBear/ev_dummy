from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # use 128 if hashing
    phone = models.CharField(max_length=15, blank=True)
    vehicle_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:
        db_table = "user"


class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    total_slots = models.IntegerField()
    available_slots = models.IntegerField()
    is_active = models.BooleanField(default=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
