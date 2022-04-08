from django.contrib import admin
from . import models


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','id','status','slug',)
    prepopulated_fields={'slug': ('title',),}

admin.site.register(models.Category)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'category', 'receipent')
 

@admin.register(models.Plate)
class PlateAdmin(admin.ModelAdmin):
    list_display = ('plate_no','user','model')
