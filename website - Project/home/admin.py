from django.contrib import admin
from .models import DataModel

class DataModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

# Register your models here.
admin.site.register(DataModel, DataModelAdmin)