from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "heading",
        "publication_sign",
    )
    list_filter = ("heading",)
    search_fields = (
        "heading",
        "publication_sign",
    )
