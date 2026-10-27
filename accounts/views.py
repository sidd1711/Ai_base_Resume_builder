from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm

class LandingPageView(TemplateView):
    template_name = 'landing.html'

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        # Calculate profile completion metrics
        profile = getattr(user, 'profile', None)
        completion_score = 0
        checklist = []

        if profile:
            if profile.full_name and profile.email and profile.phone:
                completion_score += 20
                checklist.append(('Personal Details', True))
            else:
                checklist.append(('Personal Details', False))

            if profile.professional_summary:
                completion_score += 15
                checklist.append(('Professional Summary', True))
            else:
                checklist.append(('Professional Summary', False))

            if profile.educations.exists():
                completion_score += 20
                checklist.append(('Education History', True))
            else:
                checklist.append(('Education History', False))

            if profile.skills.exists():
                completion_score += 15
                checklist.append(('Key Skills', True))
            else:
                checklist.append(('Key Skills', False))

            if profile.projects.exists():
                completion_score += 15
                checklist.append(('Projects', True))
            else:
                checklist.append(('Projects', False))

            if profile.experiences.exists():
                completion_score += 15
                checklist.append(('Work Experience / Internships', True))
            else:
                checklist.append(('Work Experience / Internships', False))
        else:
            checklist = [
                ('Personal Details', False),
                ('Professional Summary', False),
                ('Education History', False),
                ('Key Skills', False),
                ('Projects', False),
                ('Work Experience / Internships', False),
            ]

        # Fetch user's saved resumes
        resumes = user.resumes.all().order_by('-updated_at') if hasattr(user, 'resumes') else []
        # Fetch user's recent job analyses
        job_analyses = user.job_analyses.all().order_by('-created_at')[:5] if hasattr(user, 'job_analyses') else []

        context = {
            'completion_score': min(100, completion_score),
            'checklist': checklist,
            'resumes': resumes,
            'job_analyses': job_analyses,
            'user': user,
        }
        return render(request, 'dashboard/dashboard.html', context)

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure UserProfile exists
            from profiles.models import UserProfile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'full_name': f"{user.first_name} {user.last_name}".strip(),
                    'email': user.email
                }
            )
            login(request, user)
            messages.success(request, f"Welcome to ResumeForge AI, {user.first_name}! Let's build your resume.")
            return redirect('dashboard')
        return render(request, 'accounts/register.html', {'form': form})

class LoginUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'dashboard')
        messages.error(request, "Invalid username or password. Please try again.")
        return render(request, 'accounts/login.html', {'form': form})

class LogoutUserView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('landing')

    def get(self, request):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('landing')

class AccountSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/account_settings.html')

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.warning(request, "Your account and all associated resumes and profiles have been permanently deleted.")
        return redirect('landing')
