from django import forms
from .models import *
from accounts.models import *
from django.db.models import Q
import sys
from datetime import datetime, timedelta

sys.path.append("..")


class TrainerForm(forms.Form):
    name = forms.CharField(max_length=128, label='Имя')
    file = forms.FileField(label='Изображение')


class AppointmentForm(forms.Form):
    trainer = forms.ModelChoiceField(Trainer.objects.all(), empty_label='...', label='Тренер')
    amount = forms.IntegerField(label='Сумма')
    payment_type = forms.ModelChoiceField(PaymentType.objects.all(), empty_label='...', label='Способ оплаты')
    user = forms.ModelChoiceField(CustomUser.objects.filter(Q(is_partial=False) & Q(is_staff=False)), empty_label='...', label='Пользователь')


class PaymentTypeForm(forms.Form):
    name = forms.CharField(max_length=128, label='Название')


class GroupAppointmentForm(forms.Form):
    name = forms.CharField(max_length=128, label='Название')
    trainer = forms.ModelChoiceField(Trainer.objects.all(), empty_label='...', label='Тренер')


class AddUserToGroupAppointment(forms.Form):
    user = forms.ModelChoiceField(CustomUser.objects.filter(Q(is_partial=False) & Q(is_staff=False)), empty_label='...', label='Пользователь')
    group_appointment = forms.ModelChoiceField(GroupAppointment.objects.filter(time__gte=datetime.now()), label='Выберите тренировку')


class TrainingForm(forms.Form):
    name = forms.CharField(max_length=128, label='Название')


class TrainingPlanForm(forms.Form):
    name = forms.CharField(max_length=128, label='Название')


class AddTrainingToPlanForm(forms.Form):
    training = forms.ModelChoiceField(Training.objects.all(), empty_label='...', label='Упражнение')
    plan = forms.ModelChoiceField(TrainingPlan.objects.all(), empty_label='...', label='Программа')