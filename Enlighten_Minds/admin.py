from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
class MyUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name','email','instructor','refugee','low_income_student', 'password')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(users,MyUserAdmin)
admin.site.register(Courses)
admin.site.register(MyCourses)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(RefugeeDetails)
admin.site.register(Instructor_level)
admin.site.register(Fundraiser)
admin.site.register(Scholarship)