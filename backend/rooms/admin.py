from django.contrib import admin

from rooms.models import Booking, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'name',
        'price',
        'capacity',
    )
    list_editable = (
        'number',
        'name',
        'price',
        'capacity',
    )
    search_fields = ('name', 'number', 'capacity',)
    list_filter = ('price', 'capacity',)
    empty_value_display = 'empty'


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'room',
        'guest',
        'date_check_in',
        'date_check_out',
    )
    list_editable = (
        'room',
        'guest',
        'date_check_in',
        'date_check_out',
    )
    search_fields = ('room', 'guest', 'date_check_in', 'date_check_out',)
    list_filter = ('room', 'guest', 'date_check_in', 'date_check_out',)
    empty_value_display = 'empty'


# class IngredientInline(admin.TabularInline):
#
#     model = IngredientQuantity
#     extra = 1

admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
