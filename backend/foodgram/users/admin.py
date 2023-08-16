from django.contrib import admin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
        'subscribers_count',
        'recipes_count',
    )
    readonly_fields = ('subscribers_count', 'recipes_count')
    list_editable = ('password',)
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'

    @admin.display(description='Количество подписчиков')
    def subscribers_count(self, obj):
        return obj.subscriber.count()

    @admin.display(description='Количество рецептов')
    def recipes_count(self, obj):
        return obj.recipes.count()


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'
