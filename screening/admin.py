from django.contrib import admin
from .models import Resume, Job, MatchResult


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate_name', 'email', 'phone', 'created_at']
    search_fields = ['email', 'candidate_name']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title', 'created_at']
    search_fields = ['job_title']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'resume', 'job', 'score', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    search_fields = ['resume__email', 'job__job_title']