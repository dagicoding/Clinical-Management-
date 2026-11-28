from django.shortcuts import get_object_or_404, render, redirect
from itertools import groupby
from django.utils import timezone
from itertools import groupby

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

def lab_payment_list(request):
    lab_requests = LabRequest.objects.filter(status='not_paid').select_related('visit__patient','lab_test')
    visits = {}
    for lab_request in lab_requests:
        visit_id = lab_request.visit.id
        if visit_id not in visits:visits[visit_id] = {'visit': lab_request.visit,}

    context = {'visits': visits.values()}
    return render(request,'reception/labpayment.html',context)




def lab_payment_detail(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    lab_requests = LabRequest.objects.filter(visit=visit,status='not_paid').select_related('lab_test')

    total = sum(request.lab_test.price for request in lab_requests)

    context = {'visit': visit,'lab_requests': lab_requests,'total': total,}
    return render(request,'reception/lab_payment_detail.html',context)

def delete_lab_payment(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    lab_requests = LabRequest.objects.filter(visit=visit,status='not_paid')
    total = sum(lab_request.lab_test.price for lab_request in lab_requests)

    if request.method == 'POST':
        lab_requests.delete()

        return redirect('lab_payment_list')
    
    context = {'visit': visit,'lab_requests': lab_requests,'total': total,}
    return render(request,'reception/confirm_lab_payment.html',context)



def confirm_lab_payment(request, visit_id):
    visit = Visit.objects.get(id=visit_id)

    lab_requests = LabRequest.objects.filter(visit=visit,status='not_paid')
    total = sum(lab_request.lab_test.price for lab_request in lab_requests)

    if request.method == 'POST':
        Payment.objects.create(
            patient=visit.patient,
            payment_type='lab',
            amount=total,
            status='paid')


        lab_requests.update(status='paid')
        
        return redirect('lab_payment_list')
    
    context = {'visit': visit,'lab_requests': lab_requests,'total': total,}

    return render(request,'reception/confirm_lab_payment.html',context)


def medicationpayment(request):
    medications = Medication.objects.filter(status = 'Not Paid')
    context = {'medications' : medications}
    return render(request, 'reception/medicationpayment.html',context)

def medicationPaydetail(request, visit_id):
    visit = Visit.objects.get(id = visit_id)
    medications = Medication.objects.filter(visit = visit ,status = 'Not Paid')

    context = {'visit' : visit, 'medications' : medications}
    return render(request, 'reception/medicationpaydetail.html', context)

def medicationconfirm(request, visit_id):
    visit = Visit.objects.get(id=visit_id)
    medication = Medication.objects.get(visit = visit ,status = 'Not Paid')


    if request.method == "POST":
        Payment.objects.create(
                    patient=visit.patient,
                    payment_type='medication',
                    amount=medication.price,
                    status='paid')
        
        visit.status = 'compeleted'
        medication.status = 'paid'
        medication.save()
        visit.save()

        return redirect('medicationPayList')



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
    visits = Visit.objects.filter(status='doctor').select_related('patient').order_by('visit_date')
    labresult = LabResult.objects.filter(status='arrived')

    for visit in visits:
        visit.has_arrived_result = labresult.filter(lab_request__visit=visit).exists()

    context = {'visits': visits,}
    return render(request, 'doctor/onvisit.html', context)


def treat_patient(request , visit_id):
    visit = Visit.objects.get(id = visit_id, status = 'doctor')
    vital_signs = visit.vital_signs

    context = {'visit' : visit, 'vital_signs' : vital_signs}
    return render(request, 'doctor/treatPatient.html', context)

def complete_visit(request, visit_id):
    visit = Visit.objects.get(id = visit_id, status =  'doctor')
    if request.method == "POST":
            visit.status = 'completed'
            visit.save()
    return redirect('doctorVisits')


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

    context = {'form': form,'visit': visit}
    return render(request,'doctor/clinicalNote.html',context)


def labRequest(request, visit_id):

    visit = Visit.objects.get(id=visit_id,status='doctor')
    labtests = LabTest.objects.all()
    lab_cart = request.session.get('lab_cart', {})
    cart = lab_cart.get(str(visit_id), [])
    selected_tests = LabTest.objects.filter(id__in=cart)
    total = sum(test.price for test in selected_tests)

    context = {
        'labtests': labtests,
        'visit': visit,
        'selected_tests': selected_tests,
        'total': total
    }

    return render(request,'doctor/labrequest.html',context)


def add_lab_test(request, visit_id, test_id):

    visit = Visit.objects.get(id=visit_id,status='doctor')
    LabTest.objects.get(id=test_id)
    lab_cart = request.session.get('lab_cart', {})
    visit_cart = lab_cart.get(str(visit_id), [])
    if test_id not in visit_cart:
        visit_cart.append(test_id)

    lab_cart[str(visit_id)] = visit_cart
    request.session['lab_cart'] = lab_cart
    return redirect('labRequest',visit_id=visit_id)

def delete_lab_test(request, visit_id, test_id):
    visit = Visit.objects.get(id=visit_id,status='doctor')
    lab_cart = request.session.get('lab_cart', {})
    visit_cart = lab_cart.get(str(visit_id), [])

    if test_id in visit_cart:
        visit_cart.remove(test_id)

    lab_cart[str(visit_id)] = visit_cart

    request.session['lab_cart'] = lab_cart

    return redirect('labRequest',visit_id=visit_id)

def send_lab_request(request, visit_id):
    visit = Visit.objects.get(id=visit_id,status='doctor')
    lab_cart = request.session.get('lab_cart', {})
    cart = lab_cart.get(str(visit_id), [])

    if cart:
        request_group = timezone.now()

        for test_id in cart:
            lab_test = LabTest.objects.get(id=test_id)
            lab_request = LabRequest.objects.create(visit=visit,lab_test=lab_test, request_group=request_group,status='not_paid')
            LabResult.objects.create(lab_request = lab_request, status = 'not_arrived')
        

    lab_cart.pop(str(visit_id), None)
    

    request.session['lab_cart'] = lab_cart

    return redirect('labRequest', visit_id=visit.id)

def labrequestview(request):
    visits = Visit.objects.filter(lab_request__status='paid', status = 'doctor',lab_request__result__status='not_arrived').distinct().select_related('patient')
    context = {'visits': visits}
    return render(request,'lab/labrequest.html',context)



from itertools import groupby
from django.shortcuts import get_object_or_404, redirect, render

def labrequestdetail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    labrequests = LabRequest.objects.filter(visit=visit,status='paid',result__status='not_arrived').select_related('lab_test').order_by('-request_group')
    if not labrequests.exists():
        context = {'visit': visit,'grouped_requests': [],}
        return render(request, 'lab/requestdetail.html', context)

    latest_group = labrequests.first().request_group

    labrequests = labrequests.filter(request_group=latest_group).order_by('request_group')

    if request.method == 'POST':

        for labrequest in labrequests:
            result_text = request.POST.get(f'result_{labrequest.id}')

            if result_text:
                labresult = labrequest.result

                labresult.result = result_text
                labresult.status = 'arrived'
                labresult.save()

        return redirect('labrequestview')

    grouped_requests = []

    for group_time, requests in groupby(
        labrequests,
        key=lambda x: x.request_group
    ):
        grouped_requests.append({'request_group': group_time,'requests': list(requests)})

    context = {'visit': visit,'grouped_requests': grouped_requests,}
    return render(request,'lab/requestdetail.html',context)

def labResult(request, visit_id):
    visit = Visit.objects.get(id = visit_id, status = 'doctor')
    labresults = LabResult.objects.filter(lab_request__visit=visit,status='arrived').select_related('lab_request__lab_test').order_by('lab_request__request_group')

    grouped_results = []
    for group_time, results in groupby(labresults,key=lambda x: x.lab_request.request_group):
        grouped_results.append({'request_group': group_time,'results': list(results)})

    context = {'visit' : visit, 'labresults' : labresults, 'grouped_results': grouped_results,}
    return render(request, 'doctor/labresult.html', context)

def prescriptionlines(request):
    if request.method == "POST":
        form = PrescriptionLineForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect('prescription', visit_id=request.POST.get('visit_id'))



def prescription(request, visit_id):
    visit = get_object_or_404(Visit,id=visit_id,status='doctor')
    form = PrescriptionLineForm()

    prescriptions = PrescriptionTemplate.objects.all()
    prescription_cart = request.session.get('prescription_cart',{})

    cart = prescription_cart.get(str(visit_id),[])
    selected_prescriptions = PrescriptionTemplate.objects.filter(id__in=cart)
    viewprescriptions = Prescription.objects.filter(visit=visit).select_related('prescription_template').order_by('prescription_group')
    grouped_prescriptions = []

    for group_time, prescriptions_group in groupby(
        viewprescriptions,
        key=lambda x: x.prescription_group
    ):
        grouped_prescriptions.append({
            'prescription_group': group_time,
            'prescriptions': list(prescriptions_group)
        })

    context = {
        'visit': visit,
        'prescriptions': prescriptions,
        'selected_prescriptions': selected_prescriptions,
        'grouped_prescriptions': grouped_prescriptions,
        'viewprescriptions' : viewprescriptions,
        'form' : form,
    }
    return render(request,'doctor/prescription.html',context)



def add_prescription(request, visit_id):

    visit = get_object_or_404(Visit,id=visit_id,status='doctor')
    prescription_id = request.POST.get('prescription_id')

    if prescription_id:

        PrescriptionTemplate.objects.get(id=prescription_id)
        prescription_cart = request.session.get('prescription_cart',{})

        visit_cart = prescription_cart.get(str(visit_id),[])
        prescription_id = int(prescription_id)

        if prescription_id not in visit_cart:
            visit_cart.append(prescription_id)

        prescription_cart[str(visit_id)] = visit_cart
        request.session['prescription_cart'] = prescription_cart

    return redirect('prescription',visit_id=visit.id)


def delete_prescription(request, visit_id, prescription_id):

    visit = get_object_or_404(Visit,id=visit_id,status='doctor')

    prescription_cart = request.session.get('prescription_cart',{})
    visit_cart = prescription_cart.get(str(visit_id),[])

    if prescription_id in visit_cart:
        visit_cart.remove(prescription_id)

    prescription_cart[str(visit_id)] = visit_cart
    request.session['prescription_cart'] = prescription_cart
    return redirect('prescription',visit_id=visit.id)


from django.utils import timezone

def save_prescription(request, visit_id):
    visit = get_object_or_404(Visit,id=visit_id,status='doctor')

    prescription_cart = request.session.get('prescription_cart',{})

    cart = prescription_cart.get(str(visit_id),[])

    if cart:
        prescription_group = timezone.now()
        for prescription_id in cart:

            prescription_template = get_object_or_404(PrescriptionTemplate,id=prescription_id)

            Prescription.objects.create(
                visit=visit,
                prescription_template=prescription_template,
                prescription_group=prescription_group
            )
    prescription_cart.pop(str(visit_id), None)

    request.session['prescription_cart'] = prescription_cart
    return redirect('prescription',visit_id=visit.id)

def print_prescription(request, visit_id, prescription_id):
    prescription = get_object_or_404(Prescription,id=prescription_id)
    prescriptions = Prescription.objects.filter(visit=visit_id,prescription_group=prescription.prescription_group).select_related('prescription_template')

    visit = get_object_or_404(Visit, id=visit_id)
    context = {'visit': visit,'prescriptions': prescriptions,}

    return render(request, 'doctor/print.html', context)


def medicationView(request, visit_id):
    visit = Visit.objects.get(id = visit_id)
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.visit = visit
            med.save()

            return redirect('treatPatient' , visit_id = visit_id)
    else:
        form = MedicationForm()

    context = {'form' : form, 'visit' : visit}
    return render(request, 'doctor/medication.html',context)


    

        
