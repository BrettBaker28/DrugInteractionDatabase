from django.contrib import admin
from .models import Drug
# Register your models here.


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('ddinter_id', 'name')
    search_fields = ('ddinter_id', 'name')
