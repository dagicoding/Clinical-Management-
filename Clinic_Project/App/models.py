from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    Sex_choice = [
        ('M', 'Male'),
        ('F', "Female")
    ]
    sex = models.CharField(choices=Sex_choice)
    allergy = models.CharField()
    zone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)
    date_registered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Payment(models.Model):
    patient = models.ForeignKey(Patient ,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10 , decimal_places=2)  
    PAYMENT_TYPES = [
        ('card' , 'card'),
        ('lab' , 'Lab'),
        ('medication' , 'Medication'),
        ('other' , 'Other')
    ]
    status_choice = [('not_paid' , 'Not Paid'), ('paid' ,'Paid')]
    payment_type = models.CharField(choices=PAYMENT_TYPES)
    status = models.CharField(max_length=10, default='Not Paid')
    payment_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.patient.name} {self.payment_type} {self.amount}'

class ServiceFee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"card fee- {self.amount}"



class Visit(models.Model):
    status_choice = [
        ('waiting' ,'Waiting'),
        ('nurse' , 'With Nurse'),
        ('doctor' , 'With Doctor'),
        ('lab' , 'Lab'),
        ('completed' , 'Completed'),
        ('incomplete' , 'InComplete')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(choices=status_choice, default='waiting')
    visit_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.patient.name} {self.visit_date}'



class VitalSigns(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='vital_signs')
    weight = models.DecimalField(max_digits=5 , decimal_places=2)
    temprature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_pressure = models.CharField(max_length=20)
    pulse = models.PositiveIntegerField()
    respiratory = models.PositiveIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vital signs {self.visit.patient.name}"


# Doctor

class ClinicalNote(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE , related_name='clinical_note')
    complaints = [
        ('fever' , 'Fever'),
        ('headache' , 'Headache'),
        ('sweating' , 'Sweating'),
        ('join pain' , 'Join Pain'),
        ('back pain' , 'Back Pain'),
        ('vomiting' , 'Vomiting'),
        ('nausea' , 'Nausea'),
        ('shivering' , 'Shivering'),
        ('chills' , 'Chills'),
    ]
    Chife_complaint = models.CharField(choices=complaints)
    physical_examination = models.TextField()
    assessment = models.TextField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"clinical note - {self.visit.patient.name}"

# admin Lab test
class LabTest(models.Model):
    CATEGORY_CHOICES = [
        ('hematology', 'Hematology'),
        ('chemistry', 'Clinical Chemistry'),
        ('microbiology', 'Microbiology'),
        ('parasitology', 'Parasitology'),
        ('other', 'Other'),
    ]
    category = models.CharField(choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField()

    def __str__(self):
        return self.name
   

class LabRequest(models.Model):
    visit = models.ForeignKey(Visit , on_delete=models.CASCADE, related_name='lab_request')
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='request')
    status_choice = [('not_paid', 'Not Paid'),('paid' , 'Paid')]
    status = models.CharField(choices=status_choice, default='not_paid')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_test.name} - {self.visit.patient.name}"



class LabResult(models.Model):
    lab_request = models.OneToOneField(LabRequest,on_delete=models.CASCADE,related_name='result')
    result = models.CharField(blank=True)
    status_choice = [('not_arrived', 'Not Arrived'),('Arrived' , 'Arrived')]
    status = models.CharField(choices= status_choice)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_request.lab_test.name} - {self.lab_request.lab_test.reference_number}"


    

class PrescriptionTemplate(models.Model):
    name = models.CharField()   

    def __str__(self):
        return self.name



class Prescription(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    prescription = models.ForeignKey(PrescriptionTemplate, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.visit.patient.name} - prescription'


class Medication(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    medication_name = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.medication_name


class Certificate(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    doctors_recommendation = models.TextField()
    days_of_rest = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

