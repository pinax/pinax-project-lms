from django.contrib import admin

from .models import Room, Lecture


admin.site.register(
    Room,
    list_display=["room_name", "building_name", "capacity"],
)

admin.site.register(
    Lecture,
    list_display=["course_instance", "date", "start_time", "end_time", "room", "max_seats"],
)
