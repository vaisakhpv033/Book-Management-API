from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Books, Generes, Authors, ReadingLists

# Register your models here.


class CustomBookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subtitle",
        "author",
        "genre",
        "language",
        "publication_date",
        "created_at",
        "created_by",
    )
    search_fields = ("title", "author__first_name", "author__last_name")
    list_filter = ("genre", "language", "publication_date")
    ordering = ("-created_at",)

class CustomAuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "full_name")
    search_fields = ("first_name", "last_name")
    ordering = ("first_name", "last_name")

class CustomGenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

class CustomReadingListAdmin(admin.ModelAdmin):
    list_display = ("book", "position", "date_added", "user")
    search_fields = ("book__title", "book__author__first_name", "book__author__last_name")
    ordering = ("position", "date_added")


admin.site.register(Books, CustomBookAdmin)
admin.site.register(Generes, CustomGenreAdmin)
admin.site.register(Authors, CustomAuthorAdmin)
admin.site.register(ReadingLists, CustomReadingListAdmin)

