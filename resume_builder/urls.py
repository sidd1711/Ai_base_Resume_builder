from django.urls import path
from .views import (
    ResumeListView, ResumeCreateWizardView, ResumeDetailPreviewView,
    ResumeEditContentView, ResumeDuplicateView, ResumeDeleteView,
    ResumeVersionsListView, ResumeVersionRevertView, EnhanceBulletAjaxView
)

urlpatterns = [
    path('', ResumeListView.as_view(), name='resume_list'),
    path('new/', ResumeCreateWizardView.as_view(), name='resume_create_wizard'),
    path('<int:pk>/preview/', ResumeDetailPreviewView.as_view(), name='resume_preview'),
    path('<int:pk>/edit/', ResumeEditContentView.as_view(), name='resume_edit'),
    path('<int:pk>/duplicate/', ResumeDuplicateView.as_view(), name='resume_duplicate'),
    path('<int:pk>/delete/', ResumeDeleteView.as_view(), name='resume_delete'),
    path('<int:pk>/versions/', ResumeVersionsListView.as_view(), name='resume_versions'),
    path('<int:pk>/versions/<int:version_id>/revert/', ResumeVersionRevertView.as_view(), name='resume_version_revert'),
    path('api/enhance-bullet/', EnhanceBulletAjaxView.as_view(), name='api_enhance_bullet'),
]
