from django.contrib import admin
from .models import *

admin.site.register(Trainer)
admin.site.register(PaymentType)
admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(GroupAppointment)
admin.site.register(GroupAppointmentUser)
admin.site.register(Training)
admin.site.register(TrainingPlan)
admin.site.register(TrainingPlan_Training)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)