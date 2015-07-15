from django.contrib import admin

from .models import Organization


admin.site.register(
    Organization,
    list_display=["name", "slug"],
    prepopulated_fields={"slug": ("name",)}
)
