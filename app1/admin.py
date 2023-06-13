from django.contrib import admin
from .models import *

class AdminPro(admin.ModelAdmin):
    list_display = ('id','username','email','role','is_staff') 

class UsersPro(admin.ModelAdmin):
    list_display = ('id','fk_user','firstname','lastname','course','user_status')

admin.site.register(CustomUser,AdminPro)
admin.site.register(UserProfile,UsersPro)
admin.site.register(Task)
admin.site.register(Exam)
admin.site.register(Result)