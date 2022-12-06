from django.contrib import admin

from rooms.models import Room, Booking


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
        'date_range',
    )
    list_editable = (
        'room',
        'guest',
        'date_range',
    )
    search_fields = ('room', 'guest', 'date_range',)
    list_filter = ('room', 'guest', 'date_range',)
    empty_value_display = 'empty'


# class IngredientInline(admin.TabularInline):
#
#     model = IngredientQuantity
#     extra = 1

admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
