from django.urls import path
from .views import JobAnalyzeView, JobAnalysisDetailView, JobAnalysisEditView

urlpatterns = [
    path('analyze/', JobAnalyzeView.as_view(), name='job_analyze'),
    path('<int:pk>/', JobAnalysisDetailView.as_view(), name='job_analysis_detail'),
    path('<int:pk>/edit/', JobAnalysisEditView.as_view(), name='job_analysis_edit'),
]
