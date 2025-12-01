from django.contrib import admin
from .models import Book, Author, Genre

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year', 'created_at')
    list_filter = ('genre', 'year', 'created_at')
    search_fields = ('title', 'author__name', 'annotation')
    list_per_page = 20
    date_hierarchy = 'created_at'