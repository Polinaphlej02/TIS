from django.contrib.auth.admin import UserAdmin
from .models import Student
from django.contrib import admin


class MyUserAdmin(UserAdmin):
    model = Student
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('num_group',)}),
    )


admin.site.register(Student, MyUserAdmin)
