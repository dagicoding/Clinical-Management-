from django.shortcuts import render, redirect
from . models import *
from . forms import *


def register_patient(request):
    servicefee = ServiceFee.objects.first()
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            
            patient = form.save()
            Visit.objects.create(patient=patient,status = 'nurse')

            Payment.objects.create(patient=patient, payment_type ='card', amount = servicefee.amount, status = 'paid')

            return redirect('patient_register')

    else:
        form = PatientForm()
        context = {'form' : form, 'card' : servicefee.amount}
    return render(request, 'reception/patient_register.html', context)



def nurse_visits(request):
    visits = Visit.objects.filter(status = 'nurse',).select_related('patient').order_by('visit_date')
    return render(request, 'nurse/onvisit.html',{'visits' : visits})

def vital_signs(request, visit_id):
    visit = Visit.objects.get(id = visit_id , status = 'nurse')

    if request.method == "POST":
        form = VitalSignForm(request.POST)
        if form.is_valid():
            vital_signs = form.save(commit=False)
            vital_signs.visit = visit
            vital_signs.save()

            visit.status = 'doctor'
            visit.save()

        return redirect('nurseOnVisit')
    
    else:
        form = VitalSignForm()
    context = {'form' : form, 'visit' : visit}
    return render(request, 'nurse/vitalsigns.html', context)

def doctorVisits(request):
    visits = Visit.objects.filter(status = 'doctor').select_related('patient').order_by('visit_date')
    context = {'visits' : visits}
    return render(request, 'doctor/onvisit.html', context)


def treat_patient(request , visit_id):
    visit = Visit.objects.get(id = visit_id, status = 'doctor')
    vital_signs = visit.vital_signs

    context = {'visit' : visit, 'vital_signs' : vital_signs}
    return render(request, 'doctor/treatPatient.html', context)



def clinicalNote(request, visit_id):
    visit = Visit.objects.get(id=visit_id,status='doctor')

    if request.method == "POST":

        if hasattr(visit, 'clinical_note'):
            form = ClinicalNoteForm(request.POST,instance=visit.clinical_note)
        else:
            form = ClinicalNoteForm(request.POST)

        if form.is_valid():
            clinical_note = form.save(commit=False)
            clinical_note.visit = visit
            clinical_note.save()

            return redirect('treatPatient',visit_id=visit.id)
    else:

        if hasattr(visit, 'clinical_note'):
            form = ClinicalNoteForm(instance=visit.clinical_note)
        else:
            form = ClinicalNoteForm()

    context = {
        'form': form,'visit': visit}
    return render(request,'doctor/clinicalNote.html',context)


    

        
