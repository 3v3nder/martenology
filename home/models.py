from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    clientType = models.CharField(max_length=200, null=False, default="Farmer")

    def __str__(self):
        return f'Client {self.user}'

class Doctor(models.Model):
    clientType = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=200, null=True)

    def __repr__(self):
        return f'Doctor {self.clientType}'


class Disease(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, null=True)

    def __repr__(self):
        return f'Disease {self.name}'

class Symptoms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000, null=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, default=None)

    def __repr__(self):
        return f'Symptoms {self.name}'

class Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    book = models.CharField(max_length=200, default=None, null=True)
    tag = models.AutoField(primary_key=True)
    breed = models.CharField(max_length=200, null=True)
    sex = models.CharField(max_length=200, null=True)
    weight = models.FloatField()
    years = models.CharField(max_length=200, null=True, blank=True)
    diseases = models.CharField(max_length=1000, null=True, blank=True)
    recommendations = models.CharField(max_length=200, null=True, blank=True)
    referred = models.BooleanField(default=False)

    def __str__(self):
        return f'Animal {self.tag}'

class Treatment(models.Model):
    name = models.CharField(max_length=200, null=True)
    cost = models.FloatField()

    def __str__(self):
        return f'Treatment {self.name}'

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    description = models.CharField(max_length=1000, null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, default=None)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Sales {self.treatment}'

class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    payment_date = models.DateField()
    expiry_date = models.DateField()
    amount = models.IntegerField(default=20)

    def __str__(self):
        return f'Subscriptions {self.user}'

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=False)
    age = models.CharField(max_length=200, null=True)
    systolicBP = models.CharField(max_length=200, null=True)
    diastolicBP = models.CharField(max_length=200, null=True)
    bs = models.CharField(max_length=200, null=True)
    bodytemp = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Report {self.user}'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    doctorphone = models.CharField(max_length=200, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, default=None)
    message = models.CharField(max_length=1000, null=True)
    date = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment {self.animal}'



    


