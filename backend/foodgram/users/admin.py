from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as MainUserAdmin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(MainUserAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_editable = ('password',)
    list_filter = ('first_name', 'username', 'email',)
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'

    def password(self, obj):
        return obj.password


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'
