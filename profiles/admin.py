from django.contrib import admin
from .models import (
    UserProfile, Education, Skill, Project, Experience,
    Certification, Achievement
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'email', 'phone', 'city', 'country', 'created_at')
    search_fields = ('full_name', 'email', 'user__username')

admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Achievement)
