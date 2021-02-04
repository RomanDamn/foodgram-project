from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


class MyUserAdmin(UserAdmin):
    list_filter = ('email', 'first_name',)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
