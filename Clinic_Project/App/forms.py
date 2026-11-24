from django import forms
from . models import Patient , Visit


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
            'date_of_birth',
            'sex',
            'allergy',
            'zone',
            'city',
            'phone',
            'emergency_contact'
        ]
        widgets = {
            "date_of_birth": forms.DateInput(),
        }