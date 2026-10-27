from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from resume_builder.models import Resume
from .pdf_generator import generate_resume_pdf
from .docx_generator import generate_resume_docx

class ExportResumePdfView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        try:
            pdf_buffer = generate_resume_pdf(resume)
            filename = f"{resume.title.replace(' ', '_')}.pdf"
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


class ExportResumeDocxView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        try:
            docx_buffer = generate_resume_docx(resume)
            filename = f"{resume.title.replace(' ', '_')}.docx"
            response = HttpResponse(
                docx_buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error generating DOCX: {str(e)}", status=500)
