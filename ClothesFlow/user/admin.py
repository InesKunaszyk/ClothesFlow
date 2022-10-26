from django.contrib import admin

from user.models import (User, Institution)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list = ('name', 'type')
    # exclude = ['added_date']
