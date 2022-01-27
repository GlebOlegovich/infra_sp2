from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'is_active',
        'date_joined',
    )
    list_editable = ('role', 'is_active',)
    search_fields = ('username', 'email')
    list_filter = ('role', 'date_joined')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
