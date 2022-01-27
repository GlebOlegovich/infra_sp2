from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Comment, Review


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'get_genre'
    )
    list_editable = ('name', 'year', 'category')
    search_fields = ('name', 'year', 'category')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'genre'
    )
    list_editable = ('title', 'genre')
    search_fields = ('title', 'genre')
    empty_value_display = '-пусто-'


admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment)
admin.site.register(Review)
