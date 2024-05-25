from django.contrib import admin
from api.models import CustomUser,Job
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from .models import Application,Job
from django.utils.html import format_html

from django.db import models


class JobAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'summary', 'salary', 'skills', 'promoted', 'created_at', 'total_applications_display')
    readonly_fields = ('total_applications_display',)  # Make total_applications_display read-only

    def total_applications_display(self, obj):
        return obj.total_applications()
    total_applications_display.short_description = 'Total Applications'  # Customize the column name in the admin panel

admin.site.register(Job, JobAdmin)


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'first_name',)
    list_filter = ('email', 'first_name', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('id','email', 'last_name', 'first_name'
                    , 'is_staff','is_superuser','is_active','confirmation_code')  #fields to be seen
    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','is_active') } ), #is_staff admin for website , is_superuser admin of dashboard django ,is_active email verified
        
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (  #what fields should we fill when adding a new user
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'password', 'is_staff', 'is_superuser','is_active')}
         ),
    )



class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id','candidate', 'job', 'status', 'cv_link')
    list_filter = ('status', 'job__title', 'candidate__email')
    search_fields = ('job__title', 'candidate__email', 'status')
    readonly_fields = ('cv_link',)

    def cv_link(self, obj):
        """Create a link to the CV file."""
        if obj.cv:
            return format_html("<a href='{url}' target='_blank'>View CV</a>", url=obj.cv.url)
        return "No file"
    cv_link.short_description = "CV Link"

admin.site.register(Application, ApplicationAdmin)


admin.site.register(CustomUser, UserAdminConfig)



