from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_editable = ('password',)
    list_filter = ('username', 'email',)
    search_fields = ('pk', 'username', 'email',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):  
    list_display = ('pk', 'user', 'author')
    list_filter = ('pk', 'user', 'author')
    search_fields = ('pk', 'user', 'author')
    empty_value_display = '-пусто-'
