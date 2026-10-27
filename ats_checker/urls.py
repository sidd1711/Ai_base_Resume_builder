from django.urls import path
from .views import AtsAnalyzeResumeView

urlpatterns = [
    path('<int:resume_id>/', AtsAnalyzeResumeView.as_view(), name='ats_analyze_resume'),
]
