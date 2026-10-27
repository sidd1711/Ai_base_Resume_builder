from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from resume_builder.models import Resume
from job_analyzer.models import JobAnalysis
from .models import ResumeAnalysis
from .analyzer import run_full_ats_analysis

class AtsAnalyzeResumeView(LoginRequiredMixin, View):
    def get(self, request, resume_id):
        resume = get_object_or_404(Resume, pk=resume_id, user=request.user)
        job_analysis = resume.job_analysis

        # Check if user passed another job_id to test against
        override_job_id = request.GET.get('job_id')
        if override_job_id:
            job_analysis = JobAnalysis.objects.filter(pk=override_job_id, user=request.user).first()

        results = run_full_ats_analysis(resume, job_analysis)

        # Save record
        analysis_record = ResumeAnalysis.objects.create(
            resume=resume,
            job_analysis=job_analysis,
            keyword_score=results['keyword_score'],
            section_score=results['section_score'],
            formatting_score=results['formatting_score'],
            overall_score=results['overall_score'],
            matched_required=results['matched_required'],
            missing_required=results['missing_required'],
            matched_preferred=results['matched_preferred'],
            missing_preferred=results['missing_preferred'],
            available_profile_skills=results['available_profile_skills'],
            section_audit=results['section_audit'],
            formatting_issues=results['formatting_issues'],
            suggestions=results['suggestions'],
        )

        return render(request, 'ats_checker/ats_report.html', {
            'resume': resume,
            'job_analysis': job_analysis,
            'report': analysis_record,
        })
