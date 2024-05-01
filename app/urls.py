from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name='app'),
    path("create-trainer/", views.create_trainer, name='create_trainer'),
    path("create-training/", views.create_training, name='create_training'),
    path("create-training-plan/", views.create_plan, name='create_training_plan'),
    path("create-appointment/", views.create_appointment, name='create_appointment'),
    path("create-group-appointment/", views.create_group_appointment, name='create_group_appointment'),
    path("create-payment-type/", views.create_payment_type, name='create_payment_type'),
    path("get-appointments/", views.get_appointments, name='get_appointments'),
    path("get-group-appointments/", views.get_group_appointments, name='get_group_appointments'),
    path("get-photo/", views.get_photo, name='get_photo'),
    path("get-trainers/", views.get_trainers, name='get_trainers'),
    path("get-plans/", views.get_plans, name='get_plans'),
    path("get-trainer/", views.get_trainer, name='get_trainer'),
    path("get-users-of-ga/", views.get_users_of_ga, name='get_users_of_ga'),
    path("get-trainings-of-plan/", views.get_training_of_plan, name='get_trainings_of_plan'),
    path("add-user-to-group/", views.add_user_to_group, name='add_user_to_group'),
    path("add-training-to-plan/", views.add_training_to_plan, name='add_training_to_plan'),
    path("delete-appointment/", views.delete_appointment, name='delete_appointment'),
    path("delete-group-appointment/", views.delete_group_appointment, name='delete_group_appointment'),
    path("delete-user-from-ga/", views.delete_user_from_ga, name='delete_user_from_ga'),
    path("delete-training-from-plan/", views.delete_training_from_plan, name='delete_training_from_plan'),
    path("delete-plan/", views.delete_plan, name='delete_plan'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)