from django.contrib import admin

from .models import APICall, Habilitation, Import, Item, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "groups_list")


@admin.register(Habilitation)
class HabilitationAdmin(admin.ModelAdmin):
    pass


@admin.register(APICall)
class APICallAdmin(admin.ModelAdmin):
    pass


@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
