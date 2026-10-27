from django import forms
from .models import Resume, TEMPLATE_CHOICES
from job_analyzer.skills_data import JOB_ROLE_PRESETS

ROLE_CHOICES = [('', '-- Choose a Role or Type Custom Below --')] + [(r, r) for r in JOB_ROLE_PRESETS.keys()]

class ResumeWizardStep1Form(forms.Form):
    preset_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'wizardPresetSelect'})
    )
    custom_target_role = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Backend Engineer'})
    )
    template_name = forms.ChoiceField(
        choices=TEMPLATE_CHOICES,
        initial='classic_professional',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        preset = cleaned_data.get('preset_role')
        custom = cleaned_data.get('custom_target_role')
        if not preset and not custom:
            raise forms.ValidationError("Please specify a target role or choose a standard role.")
        cleaned_data['target_role'] = custom.strip() if custom else preset
        return cleaned_data


class ResumeEditForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'target_role', 'template_name', 'font_family',
            'full_name', 'email', 'phone', 'location',
            'linkedin_url', 'github_url', 'portfolio_url',
            'professional_summary'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'target_role': forms.TextInput(attrs={'class': 'form-control'}),
            'template_name': forms.Select(attrs={'class': 'form-select'}),
            'font_family': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('Helvetica, Arial, sans-serif', 'Clean Sans-Serif (Helvetica / Arial)'),
                ('Georgia, Cambria, serif', 'Classic Serif (Georgia / Cambria)'),
                ('"Segoe UI", Tahoma, sans-serif', 'Modern System (Segoe UI)'),
                ('"Roboto", sans-serif', 'Contemporary (Roboto)'),
            ]),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'professional_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
