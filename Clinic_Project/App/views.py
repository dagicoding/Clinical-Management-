from django.shortcuts import render, redirect
from . models import Visit
from . forms import PatientForm


def register_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            Visit.objects.create(patient=patient)

            return redirect('patient_register')

    else:
        form = PatientForm()
        context = {'form' : form}
    return render(request, 'reception/patient_register.html', context)
        
