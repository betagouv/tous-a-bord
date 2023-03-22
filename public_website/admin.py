from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Habilitation, User

admin.site.register(User, UserAdmin)


@admin.register(Habilitation)
class HabilitationAdmin(admin.ModelAdmin):
    pass
