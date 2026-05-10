from django.db import models
from django.core.validators import RegexValidator

class Service(models.Model):
    SERVICE_TYPES = [
        (0, 'INC'),
        (1, 'REQ'),
        (2, 'PRB'),
        (3, 'CHG'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    service_type = models.IntegerField(choices=SERVICE_TYPES, default=0)

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    fk_department = models.ForeignKey(Department, on_delete=models.CASCADE)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    fullname = models.CharField(max_length=250)
    shortname = models.CharField(max_length=100)
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
    is_staff = models.BooleanField(default=False)

class Ticket(models.Model):
    STAGES = [
        (0, 'Новое'),
        (1, 'Классифицируется'),
        (2, 'Назначен'),
        (3, 'Решён'),
        (4, 'Закрыт'),
    ]
    PRIORITIES = [
        (0, 'Низкий'),
        (1, 'Средний'),
        (2, 'Высокий'),
    ]
    id = models.AutoField(primary_key=True)
    stage = models.IntegerField(choices=STAGES, default=0)
    priority = models.IntegerField(choices=PRIORITIES, default=0)
    fk_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    fk_initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiator')
    fk_responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible', null=True, blank=True)
    description = models.CharField(max_length=1000)
    datetime_registered = models.DateTimeField()
    datetime_classified = models.DateTimeField(null=True, blank=True)
    datetime_assigned = models.DateTimeField(null=True, blank=True)
    datetime_diagnosed = models.DateTimeField(null=True, blank=True)
    datetime_solved = models.DateTimeField(null=True, blank=True)
    datetime_closed = models.DateTimeField(null=True, blank=True)
    datetime_deadlinne = models.DateTimeField(null=True, blank=True)
    is_stopped = models.BooleanField(default=False)
    
