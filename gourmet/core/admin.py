# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Rating)
