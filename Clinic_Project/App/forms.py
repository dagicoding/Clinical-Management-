from django import forms
from . models import *


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
            "date_of_birth": forms.DateInput(attrs={'type' : "Date"}),
        }


class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields =['weight','temprature','blood_pressure','pulse','respiratory']


class ClinicalNoteForm(forms.ModelForm):
    class Meta:
        model = ClinicalNote
        fields = ['Chife_complaint','physical_examination','assessment','plan']

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['lab_request','result']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription']