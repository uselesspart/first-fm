from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os
import gridfs
import sys
import base64
from datetime import datetime
from accounts.models import *
from django.db.models import Q
import requests
from django.conf import settings
import uuid

sys.path.append("..")


def index(request):
    return render(request, 'app.html')

def delete_user_from_ga(request):
    appointment_id = request.POST.get('appointment')
    user_id = request.POST.get('user_id')
    app = GroupAppointment.objects.get(id=appointment_id)
    user = CustomUser.objects.get(id=user_id)
    g_app_u = GroupAppointmentUser.objects.get(group_appointment=app, user=user)
    g_app_u.delete()
    return get_users_of_ga(request)

def delete_training_from_plan(request):
    plan_id = request.POST.get('plan')
    training_id = request.POST.get('training')
    plan = TrainingPlan.objects.get(id=plan_id)
    training = Training.objects.get(id=training_id)
    tpl = TrainingPlan_Training.objects.get(training=training, plan=plan)
    tpl.delete()
    return get_training_of_plan(request)

def delete_plan(request):
    plan_id = request.POST.get('plan')
    plan = TrainingPlan.objects.get(id=plan_id)
    plan.delete()
    return get_plans(request)

def delete_appointment(request):
    appointment_id = request.POST.get('appointment')
    app = Appointment.objects.get(id=appointment_id)
    app.delete()
    return get_appointments(request)

def delete_group_appointment(request):
    appointment_id = request.POST.get('appointment')
    app = GroupAppointment.objects.get(id=appointment_id)
    app.delete()
    return get_group_appointments(request)

def get_photo(request):
    trainer_id = request.POST.get('trainer')
    trainer = Trainer.objects.get(id=trainer_id)
    photo_id = trainer.photo_id
    response = get_image(photo_id)
    return response

def get_trainer(request):
    trainer_id = request.POST.get('trainer')
    trainer = Trainer.objects.get(id=trainer_id)
    return render(request, 'trainer_page.html', {'trainer': trainer})

def get_trainers(request):
    trainers = Trainer.objects.all()
    return render(request, 'get_trainers.html', {'trainers': trainers})

def get_plans(request):
    plans = TrainingPlan.objects.all()
    return render(request, 'get_plans.html', {'plans': plans})

def get_appointments(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    apps = list(Appointment.objects.filter(user=user))
    apps_all = Appointment.objects.all()
    return render(request, 'get_appointments.html', {'apps': apps, 'apps_all': apps_all})

def get_group_appointments(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    ga_u = list(GroupAppointmentUser.objects.filter(user=user))
    apps = []
    for g in ga_u:
        group_app = g.group_appointment
        if group_app not in apps:
            apps.append(group_app)
    apps_all = GroupAppointment.objects.all()
    return render(request, 'get_group_appointments.html', {'apps': apps, 'apps_all': apps_all})

def get_users_of_ga(request):
    appointment_id = request.POST.get('appointment')
    users = []
    app = GroupAppointment.objects.get(id=appointment_id)
    g_apps_user = list(GroupAppointmentUser.objects.filter(group_appointment=app))
    for g in g_apps_user:
        users.append(g.user)
    return render(request, 'get_users_of_ga.html', {'users': users, 'appointment': appointment_id})

def get_training_of_plan(request):
    plan_id = request.POST.get('plan')
    trainings = []
    plan = TrainingPlan.objects.get(id=plan_id)
    plan_ts = list(TrainingPlan_Training.objects.filter(plan=plan))
    for p in plan_ts:
        trainings.append(p.training)
    return render(request, 'get_trainings_of_plan.html', {'trainings': trainings, 'plan': plan_id})

def create_plan(request):
    form = TrainingPlanForm(request.POST)
    if form.is_valid():
        name = request.POST.get('name')
        t_plan = TrainingPlan(name=name)
        t_plan.save()
        return get_plans(request)
    else:
        form = TrainingPlanForm()
    return render(request, 'create_training_plan.html', {'form': form})

def create_training(request):
    form = TrainingForm(request.POST)
    if form.is_valid():
        name = request.POST.get('name')
        description = request.POST.get('description')
        training = Training(name=name, description=description)
        training.save()
        return HttpResponseRedirect("../")
    else:
        form = TrainingForm()
    return render(request, 'create_training.html', {'form': form})

def create_payment_type(request):
    form = PaymentTypeForm(request.POST)
    if form.is_valid():
        name = request.POST.get('name')
        payment_type = PaymentType(name=name)
        payment_type.save()
        return HttpResponseRedirect("../")
    else:
        form = PaymentTypeForm()
    return render(request, 'create_payment_type.html', {'form': form})

def create_trainer(request):
    form = TrainerForm(request.POST, request.FILES)
    if form.is_valid():
        name = request.POST.get('name')
        for filename, file in request.FILES.items():
            file_id = save_image(request.FILES[filename], 'trainer picture', filename)
        trainer = Trainer(name=name, photo_id=file_id)
        trainer.save()
        return HttpResponseRedirect("../")
    else:
        form = TrainerForm()
    return render(request, 'create_trainer.html', {'form': form})


def create_appointment(request):
    form = AppointmentForm(request.POST)
    if form.is_valid():
        trainer_id = request.POST.get('trainer')
        amount = request.POST.get('amount')
        payment_type_id = request.POST.get('payment_type')
        user_id = request.POST.get('user')
        time = request.POST.get('time')
        payment_type = PaymentType.objects.get(id=payment_type_id)
        trainer = Trainer.objects.get(id=trainer_id)
        user = CustomUser.objects.get(id=user_id)
        payment = Payment(amount=amount, payment_type=payment_type)
        payment.save()
        appointment = Appointment(trainer=trainer, payment=payment, user=user, time=time)
        appointment.save()
        return HttpResponseRedirect("../")
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})

def create_group_appointment(request):
    form = GroupAppointmentForm(request.POST)
    if form.is_valid():
        trainer_id = request.POST.get('trainer')
        name = request.POST.get('name')
        time = request.POST.get('time')
        trainer = Trainer.objects.get(id=trainer_id)
        app = GroupAppointment(name=name, time=time, trainer=trainer)
        app.save()
        return HttpResponseRedirect("../")
    else:
        form = GroupAppointmentForm()
    return render(request, 'create_group_appointment.html', {'form': form})

def add_user_to_group(request):
    form = AddUserToGroupAppointment(request.POST)
    if form.is_valid():
        user_id = request.POST.get('user')
        app_id = request.POST.get('group_appointment')
        user = CustomUser.objects.get(id=user_id)
        app = GroupAppointment.objects.get(id=app_id)
        res = list(GroupAppointmentUser.objects.filter(group_appointment=app))
        us = []
        for r in res:
            us.append(r.user)
        if user not in us:
            gapp_u = GroupAppointmentUser(user=user, group_appointment=app)
            gapp_u.save()
        return HttpResponseRedirect("../")
    else:
        form = AddUserToGroupAppointment()
    return render(request, 'add_user_to_group.html', {'form': form})

def add_training_to_plan(request):
    form = AddTrainingToPlanForm(request.POST)
    if form.is_valid():
        plan_id = request.POST.get('plan')
        training_id = request.POST.get('training')
        plan = TrainingPlan.objects.get(id=plan_id)
        training = Training.objects.get(id=training_id)
        res = list(TrainingPlan_Training.objects.filter(plan=plan))
        trs = []
        for r in res:
            trs.append(r.training)
        if training not in trs:
            ttr = TrainingPlan_Training(training=training, plan=plan)
            ttr.save()
        return get_plans(request)
    else:
        form = AddTrainingToPlanForm()
    return render(request, 'add_training_to_plan.html', {'form': form})

def get_image(image_id):
    connection = MongoClient("mongodb", 27017)
    database = connection['images']
    collection = database['images']
    fs=gridfs.GridFS(database)
    fs=gridfs.GridFS(database)
    image_data = fs.get(ObjectId(image_id))
    return HttpResponse(image_data, content_type="image/png")

def imgt(request):
    connection = MongoClient("mongodb", 27017)
    database = connection['images']
    collection = database['images']
    fs=gridfs.GridFS(database)
    fs=gridfs.GridFS(database)
    image_data = fs.get(ObjectId('662e5a8c032064d38d5d3791'))
    return HttpResponse(image_data, content_type="image/png")


def save_image(file, about, filename):
    connection = MongoClient("mongodb", 27017)

    database = connection['images']
    collection = database['images']

    fs = gridfs.GridFS(database)
    file_id = fs.put(file,filename=filename)
    data={ "about":about, "file_id":file_id}
    collection.insert_one(data)
    return file_id
