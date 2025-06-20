from django.db import models


class user(models.Model): 
    
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=15)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
