from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Resume, ResumeVersion, TEMPLATE_CHOICES
from .forms import ResumeWizardStep1Form, ResumeEditForm
from .services import build_resume_from_profile
from .ai_generator import enhance_bullet_point_ai
from job_analyzer.models import JobAnalysis

class ResumeListView(LoginRequiredMixin, View):
    def get(self, request):
        resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
        return render(request, 'resume_builder/resume_list.html', {'resumes': resumes})


class ResumeCreateWizardView(LoginRequiredMixin, View):
    def get(self, request):
        job_id = request.GET.get('job_id')
        job_analysis = None
        initial_role = ""

        if job_id:
            job_analysis = get_object_or_404(JobAnalysis, pk=job_id, user=request.user)
            initial_role = job_analysis.job_title

        form = ResumeWizardStep1Form(initial={'custom_target_role': initial_role})
        return render(request, 'resume_builder/wizard_step1_target.html', {
            'form': form,
            'job_analysis': job_analysis,
        })

    def post(self, request):
        form = ResumeWizardStep1Form(request.POST)
        job_id = request.POST.get('job_id')
        job_analysis = None
        if job_id:
            job_analysis = JobAnalysis.objects.filter(pk=job_id, user=request.user).first()

        if form.is_valid():
            target_role = form.cleaned_data['target_role']
            template_name = form.cleaned_data['template_name']

            try:
                resume = build_resume_from_profile(
                    user=request.user,
                    target_role=target_role,
                    job_analysis=job_analysis,
                    template_name=template_name
                )
                messages.success(request, f"Resume created for '{target_role}'! Review and refine below.")
                return redirect('resume_preview', pk=resume.pk)
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('profile_edit')

        return render(request, 'resume_builder/wizard_step1_target.html', {
            'form': form,
            'job_analysis': job_analysis,
        })


class ResumeDetailPreviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        # Allow instant template switching via ?template= param
        template_param = request.GET.get('template')
        if template_param and template_param in dict(TEMPLATE_CHOICES):
            resume.template_name = template_param
            resume.save()

        template_file = f"resume_templates/{resume.template_name}.html"
        return render(request, 'resume_builder/resume_preview.html', {
            'resume': resume,
            'template_file': template_file,
            'template_choices': TEMPLATE_CHOICES,
        })


class ResumeEditContentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        form = ResumeEditForm(instance=resume)
        skills_csv = ", ".join(resume.selected_skills) if isinstance(resume.selected_skills, list) else ""

        return render(request, 'resume_builder/resume_edit.html', {
            'resume': resume,
            'form': form,
            'skills_csv': skills_csv,
        })

    def post(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        form = ResumeEditForm(request.POST, instance=resume)
        if form.is_valid():
            resume = form.save(commit=False)

            # Update skills
            skills_raw = request.POST.get('skills_csv', '')
            resume.selected_skills = [s.strip() for s in skills_raw.split(',') if s.strip()]

            # Update project bullets
            projects = resume.selected_projects
            for idx, proj in enumerate(projects):
                bullets_raw = request.POST.get(f'proj_{idx}_bullets', '')
                if bullets_raw:
                    proj['bullets'] = [b.strip() for b in bullets_raw.splitlines() if b.strip()]
            resume.selected_projects = projects

            # Update experience bullets
            experiences = resume.selected_experiences
            for idx, exp in enumerate(experiences):
                bullets_raw = request.POST.get(f'exp_{idx}_bullets', '')
                if bullets_raw:
                    exp['bullets'] = [b.strip() for b in bullets_raw.splitlines() if b.strip()]
            resume.selected_experiences = experiences

            resume.save()
            resume.save_version(change_summary="User edited content")
            messages.success(request, "Resume content successfully updated!")
            return redirect('resume_preview', pk=resume.pk)

        return render(request, 'resume_builder/resume_edit.html', {
            'resume': resume,
            'form': form,
        })


class ResumeDuplicateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        original = get_object_or_404(Resume, pk=pk, user=request.user)
        clone = Resume.objects.create(
            user=request.user,
            title=f"{original.title} (Copy)",
            target_role=original.target_role,
            job_analysis=original.job_analysis,
            template_name=original.template_name,
            full_name=original.full_name,
            email=original.email,
            phone=original.phone,
            location=original.location,
            linkedin_url=original.linkedin_url,
            github_url=original.github_url,
            portfolio_url=original.portfolio_url,
            professional_summary=original.professional_summary,
            selected_skills=original.selected_skills,
            selected_educations=original.selected_educations,
            selected_projects=original.selected_projects,
            selected_experiences=original.selected_experiences,
            selected_certifications=original.selected_certifications,
            selected_achievements=original.selected_achievements,
            section_order=original.section_order,
            font_family=original.font_family,
        )
        clone.save_version(change_summary="Cloned from " + original.title)
        messages.success(request, f"Resume duplicated as '{clone.title}'.")
        return redirect('resume_preview', pk=clone.pk)


class ResumeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        title = resume.title
        resume.delete()
        messages.success(request, f"Resume '{title}' deleted permanently.")
        return redirect('dashboard')


class ResumeVersionsListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        versions = resume.versions.all()
        return render(request, 'resume_builder/version_history.html', {
            'resume': resume,
            'versions': versions
        })


class ResumeVersionRevertView(LoginRequiredMixin, View):
    def post(self, request, pk, version_id):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        version = get_object_or_404(ResumeVersion, pk=version_id, resume=resume)

        snap = version.content_snapshot
        resume.title = snap.get('title', resume.title)
        resume.target_role = snap.get('target_role', resume.target_role)
        resume.template_name = snap.get('template_name', resume.template_name)
        resume.full_name = snap.get('full_name', resume.full_name)
        resume.email = snap.get('email', resume.email)
        resume.phone = snap.get('phone', resume.phone)
        resume.location = snap.get('location', resume.location)
        resume.linkedin_url = snap.get('linkedin_url', resume.linkedin_url)
        resume.github_url = snap.get('github_url', resume.github_url)
        resume.portfolio_url = snap.get('portfolio_url', resume.portfolio_url)
        resume.professional_summary = snap.get('professional_summary', resume.professional_summary)
        resume.selected_skills = snap.get('selected_skills', resume.selected_skills)
        resume.selected_educations = snap.get('selected_educations', resume.selected_educations)
        resume.selected_projects = snap.get('selected_projects', resume.selected_projects)
        resume.selected_experiences = snap.get('selected_experiences', resume.selected_experiences)
        resume.selected_certifications = snap.get('selected_certifications', resume.selected_certifications)
        resume.selected_achievements = snap.get('selected_achievements', resume.selected_achievements)
        resume.section_order = snap.get('section_order', resume.section_order)
        resume.save()

        resume.save_version(change_summary=f"Reverted to Version {version.version_number}")
        messages.success(request, f"Reverted resume to version {version.version_number}.")
        return redirect('resume_preview', pk=resume.pk)


class EnhanceBulletAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            raw_text = data.get('bullet_text', '')
            role = data.get('target_role', '')
            improved = enhance_bullet_point_ai(raw_text, target_role=role)
            return JsonResponse({'status': 'success', 'improved': improved})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
