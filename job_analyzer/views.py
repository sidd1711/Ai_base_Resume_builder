from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import JobAnalysis
from .forms import JobAnalysisForm
from .skills_data import JOB_ROLE_PRESETS
from .skill_extractor import extract_job_requirements

class JobAnalyzeView(LoginRequiredMixin, View):
    def get(self, request):
        form = JobAnalysisForm()
        return render(request, 'job_analyzer/analyze_job.html', {
            'form': form,
            'presets': JOB_ROLE_PRESETS
        })

    def post(self, request):
        form = JobAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user

            preset = form.cleaned_data.get('preset_role')
            if preset and not form.cleaned_data.get('raw_description'):
                preset_data = JOB_ROLE_PRESETS.get(preset, {})
                analysis.required_skills = preset_data.get('required', [])
                analysis.preferred_skills = preset_data.get('preferred', [])
                analysis.experience_required = "2+ years relevant experience"
                analysis.education_required = "Bachelor's degree or equivalent practical experience"
                analysis.is_role_preset = True
            else:
                extracted = extract_job_requirements(analysis.raw_description)
                analysis.required_skills = extracted['required_skills']
                analysis.preferred_skills = extracted['preferred_skills']
                analysis.experience_required = extracted['experience_required']
                analysis.education_required = extracted['education_required']
                analysis.is_role_preset = False

            analysis.save()
            messages.success(request, f"Analyzed job role '{analysis.job_title}'. Review the extracted requirements below.")
            return redirect('job_analysis_detail', pk=analysis.pk)

        return render(request, 'job_analyzer/analyze_job.html', {
            'form': form,
            'presets': JOB_ROLE_PRESETS
        })


class JobAnalysisDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        analysis = get_object_or_404(JobAnalysis, pk=pk, user=request.user)

        # Check against user's verified profile skills
        user_skills = set()
        if hasattr(request.user, 'profile'):
            user_skills = {s.name.lower() for s in request.user.profile.skills.all()}

        matched_req = [s for s in analysis.required_skills if s.lower() in user_skills]
        missing_req = [s for s in analysis.required_skills if s.lower() not in user_skills]
        matched_pref = [s for s in analysis.preferred_skills if s.lower() in user_skills]
        missing_pref = [s for s in analysis.preferred_skills if s.lower() not in user_skills]

        context = {
            'analysis': analysis,
            'matched_req': matched_req,
            'missing_req': missing_req,
            'matched_pref': matched_pref,
            'missing_pref': missing_pref,
        }
        return render(request, 'job_analyzer/analysis_results.html', context)


class JobAnalysisEditView(LoginRequiredMixin, View):
    def post(self, request, pk):
        analysis = get_object_or_404(JobAnalysis, pk=pk, user=request.user)
        req_str = request.POST.get('required_skills_csv', '')
        pref_str = request.POST.get('preferred_skills_csv', '')

        analysis.required_skills = [s.strip() for s in req_str.split(',') if s.strip()]
        analysis.preferred_skills = [s.strip() for s in pref_str.split(',') if s.strip()]
        analysis.save()
        messages.success(request, "Extracted requirements updated.")
        return redirect('job_analysis_detail', pk=analysis.pk)
