from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from .models import (
    UserProfile, Education, Skill, Project, Experience,
    Certification, Achievement
)
from .forms import (
    UserProfileForm, EducationForm, SkillForm, ProjectForm,
    ExperienceForm, CertificationForm, AchievementForm, ResumeUploadForm
)
from .resume_parser import extract_text_from_file, parse_resume_content

class ProfileDetailView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'profiles/profile_detail.html', {'profile': profile})


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=profile)
        return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Personal information updated successfully.")
            return redirect('profile_detail')
        return render(request, 'profiles/profile_form.html', {'form': form, 'profile': profile})


# --- Education Views ---
class EducationAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            messages.success(request, "Education entry added.")
        else:
            messages.error(request, "Error adding education. Please verify your inputs.")
        return redirect('profile_detail')

class EducationDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        edu = get_object_or_404(Education, pk=pk, profile__user=request.user)
        edu.delete()
        messages.success(request, "Education entry removed.")
        return redirect('profile_detail')


# --- Skill Views ---
class SkillAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data['name'].strip()
            category = form.cleaned_data['category']
            proficiency = form.cleaned_data['proficiency']
            Skill.objects.update_or_create(
                profile=profile,
                name__iexact=skill_name,
                defaults={'name': skill_name, 'category': category, 'proficiency': proficiency}
            )
            messages.success(request, f"Skill '{skill_name}' saved.")
        else:
            messages.error(request, "Invalid skill data.")
        return redirect('profile_detail')

class SkillDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        skill = get_object_or_404(Skill, pk=pk, profile__user=request.user)
        skill.delete()
        messages.success(request, f"Skill '{skill.name}' removed.")
        return redirect('profile_detail')


# --- Project Views ---
class ProjectAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = ProjectForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.profile = profile
            proj.save()
            messages.success(request, f"Project '{proj.title}' saved.")
        else:
            messages.error(request, "Please check project fields.")
        return redirect('profile_detail')

class ProjectDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proj = get_object_or_404(Project, pk=pk, profile__user=request.user)
        proj.delete()
        messages.success(request, "Project entry removed.")
        return redirect('profile_detail')


# --- Experience Views ---
class ExperienceAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile
            exp.save()
            messages.success(request, f"Experience at '{exp.organization}' saved.")
        else:
            messages.error(request, "Please check experience fields.")
        return redirect('profile_detail')

class ExperienceDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        exp = get_object_or_404(Experience, pk=pk, profile__user=request.user)
        exp.delete()
        messages.success(request, "Experience entry removed.")
        return redirect('profile_detail')


# --- Certification Views ---
class CertificationAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = profile
            cert.save()
            messages.success(request, f"Certification '{cert.name}' added.")
        return redirect('profile_detail')

class CertificationDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cert = get_object_or_404(Certification, pk=pk, profile__user=request.user)
        cert.delete()
        messages.success(request, "Certification removed.")
        return redirect('profile_detail')


# --- Achievement Views ---
class AchievementAddView(LoginRequiredMixin, View):
    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = AchievementForm(request.POST)
        if form.is_valid():
            ach = form.save(commit=False)
            ach.profile = profile
            ach.save()
            messages.success(request, f"Achievement '{ach.title}' added.")
        return redirect('profile_detail')

class AchievementDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ach = get_object_or_404(Achievement, pk=pk, profile__user=request.user)
        ach.delete()
        messages.success(request, "Achievement removed.")
        return redirect('profile_detail')


# --- Upload Existing Resume ---
class ResumeUploadView(LoginRequiredMixin, View):
    def get(self, request):
        form = ResumeUploadForm()
        return render(request, 'profiles/upload_resume.html', {'form': form})

    def post(self, request):
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume_file']
            try:
                extracted_text = extract_text_from_file(uploaded_file, uploaded_file.name)
                parsed_data = parse_resume_content(extracted_text)

                # Store extracted in session for user review
                request.session['parsed_resume_data'] = parsed_data
                messages.info(request, "Resume parsed successfully! Review the extracted data below and select what you wish to import.")
                return render(request, 'profiles/upload_resume.html', {
                    'form': form,
                    'parsed_data': parsed_data,
                    'review_mode': True
                })
            except Exception as e:
                messages.error(request, f"Failed to parse resume: {str(e)}")
        return render(request, 'profiles/upload_resume.html', {'form': form})


class ResumeImportConfirmView(LoginRequiredMixin, View):
    def post(self, request):
        parsed = request.session.get('parsed_resume_data')
        if not parsed:
            messages.warning(request, "No extracted resume data found in session.")
            return redirect('profile_upload_resume')

        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        # Import confirmed fields
        if request.POST.get('import_name') and parsed.get('full_name') and not profile.full_name:
            profile.full_name = parsed['full_name']
        if request.POST.get('import_email') and parsed.get('email') and not profile.email:
            profile.email = parsed['email']
        if request.POST.get('import_phone') and parsed.get('phone') and not profile.phone:
            profile.phone = parsed['phone']
        if request.POST.get('import_linkedin') and parsed.get('linkedin_url') and not profile.linkedin_url:
            profile.linkedin_url = parsed['linkedin_url']
        if request.POST.get('import_github') and parsed.get('github_url') and not profile.github_url:
            profile.github_url = parsed['github_url']
        if request.POST.get('import_summary') and parsed.get('summary') and not profile.professional_summary:
            profile.professional_summary = parsed['summary']

        profile.save()

        # Import skills
        selected_skills = request.POST.getlist('selected_skills')
        imported_skill_count = 0
        for s_name in selected_skills:
            if s_name.strip():
                _, created = Skill.objects.get_or_create(
                    profile=profile,
                    name__iexact=s_name.strip(),
                    defaults={'name': s_name.strip(), 'category': 'programming'}
                )
                if created:
                    imported_skill_count += 1

        # Clear session
        request.session.pop('parsed_resume_data', None)
        messages.success(request, f"Profile updated with confirmed details and {imported_skill_count} skills imported!")
        return redirect('profile_detail')
