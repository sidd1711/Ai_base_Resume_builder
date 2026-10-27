from django.contrib import admin
from .models import Resume, ResumeVersion

class ResumeVersionInline(admin.TabularInline):
    model = ResumeVersion
    extra = 0
    readonly_fields = ('version_number', 'change_summary', 'created_at')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_role', 'template_name', 'updated_at')
    search_fields = ('title', 'target_role', 'user__username', 'full_name')
    inlines = [ResumeVersionInline]
