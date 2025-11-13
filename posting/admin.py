from django.contrib import admin

from .models import Post, Tag, Vote


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_anonymous", "is_flagged", "created_at")
    list_filter = ("is_flagged", "is_anonymous", "tags", "created_at")
    search_fields = ("title", "body")
    autocomplete_fields = ("tags",)
    date_hierarchy = "created_at"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("post", "voter", "created_at")
    autocomplete_fields = ("post", "voter")
