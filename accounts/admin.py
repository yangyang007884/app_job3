from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, JobSeekerProfile, Company, Job, Application


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'education')
    search_fields = ('full_name', 'user__username')
    list_filter = ('education',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_name')
    search_fields = ('company_name', 'user__username')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'position', 'education_level', 'required_language')
    search_fields = ('position', 'company__company_name')
    list_filter = ('education_level',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'job_seeker_profile', 'applied_at')
    search_fields = ('job__position', 'job_seeker_profile__full_name')
    list_filter = ('applied_at',)