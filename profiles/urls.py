from django.urls import path
from .views import (
    ProfileDetailView, ProfileEditView,
    EducationAddView, EducationDeleteView,
    SkillAddView, SkillDeleteView,
    ProjectAddView, ProjectDeleteView,
    ExperienceAddView, ExperienceDeleteView,
    CertificationAddView, CertificationDeleteView,
    AchievementAddView, AchievementDeleteView,
    ResumeUploadView, ResumeImportConfirmView
)

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('edit/', ProfileEditView.as_view(), name='profile_edit'),

    path('education/add/', EducationAddView.as_view(), name='education_add'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education_delete'),

    path('skill/add/', SkillAddView.as_view(), name='skill_add'),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill_delete'),

    path('project/add/', ProjectAddView.as_view(), name='project_add'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    path('experience/add/', ExperienceAddView.as_view(), name='experience_add'),
    path('experience/<int:pk>/delete/', ExperienceDeleteView.as_view(), name='experience_delete'),

    path('certification/add/', CertificationAddView.as_view(), name='certification_add'),
    path('certification/<int:pk>/delete/', CertificationDeleteView.as_view(), name='certification_delete'),

    path('achievement/add/', AchievementAddView.as_view(), name='achievement_add'),
    path('achievement/<int:pk>/delete/', AchievementDeleteView.as_view(), name='achievement_delete'),

    path('upload/', ResumeUploadView.as_view(), name='profile_upload_resume'),
    path('upload/confirm/', ResumeImportConfirmView.as_view(), name='profile_import_confirm'),
]
