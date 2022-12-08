from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'email',
        'password',
    )
    list_editable = (
        'first_name',
        'last_name',
        'username',
        'email',
        'password',
    )
    search_fields = (
        'username',
        'email',
        'capacity',
    )
    empty_value_display = 'empty'


admin.site.register(User, UserAdmin)
