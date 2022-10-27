from django.contrib import admin

from user.models import (User, Institution, Donation)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)