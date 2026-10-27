from django.urls import path
from .views import ExportResumePdfView, ExportResumeDocxView

urlpatterns = [
    path('pdf/<int:pk>/', ExportResumePdfView.as_view(), name='export_resume_pdf'),
    path('docx/<int:pk>/', ExportResumeDocxView.as_view(), name='export_resume_docx'),
]
