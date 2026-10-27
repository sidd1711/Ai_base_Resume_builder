from django import forms
from .models import JobAnalysis
from .skills_data import JOB_ROLE_PRESETS

ROLE_CHOICES = [('', '-- Or Select a Standard Role --')] + [(role, role) for role in JOB_ROLE_PRESETS.keys()]

class JobAnalysisForm(forms.ModelForm):
    preset_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'presetRoleSelect'})
    )

    class Meta:
        model = JobAnalysis
        fields = ['job_title', 'company_name', 'raw_description']
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Full-Stack Engineer',
                'id': 'jobTitleInput'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Google / TechCorp (Optional)'
            }),
            'raw_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Paste full job description here (responsibilities, required skills, preferred qualifications, experience requirements)...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        preset = cleaned_data.get('preset_role')
        title = cleaned_data.get('job_title')
        desc = cleaned_data.get('raw_description')

        if not title and preset:
            cleaned_data['job_title'] = preset
            title = preset

        if not title:
            raise forms.ValidationError("Please provide a job title or choose a standard role.")

        if not desc and preset:
            preset_data = JOB_ROLE_PRESETS.get(preset, {})
            cleaned_data['raw_description'] = f"Standard Job Role Guidance for {preset}.\n\nRequired Skills: {', '.join(preset_data.get('required', []))}\nPreferred Skills: {', '.join(preset_data.get('preferred', []))}\nOverview: {preset_data.get('summary', '')}"

        elif not desc:
            raise forms.ValidationError("Please paste a job description or select a standard job role.")

        return cleaned_data
