from django.conf import settings
from django.db import models
from accounts.models import *
import sys 


sys.path.append("..")

class Trainer(models.Model):
    name = models.CharField(max_length=128)
    photo_id = models.CharField(max_length=24)

    def __str__(self):
        return self.name

class PaymentType(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Payment(models.Model):
    amount = models.IntegerField()
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)



class Appointment(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time = models.DateTimeField()



class GroupAppointment(models.Model):
    name = models.CharField(max_length=128, default='Командная тренировка')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return self.name


class GroupAppointmentUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group_appointment = models.ForeignKey(GroupAppointment, on_delete=models.CASCADE)

class Training(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    

class TrainingPlan(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class TrainingPlan_Training(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)


class Subscription(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class SubscriptionPlan(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    expires = models.DateTimeField()
