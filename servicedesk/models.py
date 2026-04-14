from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class TicketType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    service_ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)

class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    fk_department = models.ForeignKey(Department, on_delete=models.CASCADE)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    fulname = models.CharField(max_length=250)
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
            )
        ]
    )
    fk_job = models.ForeignKey(Job, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    fk_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    fk_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    fk_responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Приоритет не может быть меньше 1"),
            MaxValueValidator(5, message="Приоритет не может быть больше 5")
        ],
        default=1
    )
    description = models.CharField(max_length=1000)
    datetime_open = models.DateTimeField()
    datetime_deadlinne = models.DateTimeField()
    datetime_close = models.DateTimeField()
    
