from django.db import models
from .enums import GenderOptions, PacksPerDay,FamilyMembers
from django.contrib.auth import get_user_model
from appointment.models import BaseModel

# Create your models here.

class Patients(BaseModel):
    primary_doctor = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="primary_doctor")
    full_name = models.CharField(max_length=200)
    gender = models.CharField(choices=GenderOptions.choices, max_length=20)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    illnesses = models.CharField(max_length=100)
    describtion = models.CharField(max_length=1000, null=True)
    past_illnesses = models.ManyToManyField(to="patient.PastMedicalIllnesses")
    symptoms = models.ManyToManyField(to="patient.Symptoms")

    def __str__(self):
        return self.full_name
    
    
    
def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/patient/{0}/{1}'.format(instance.patient.id, filename)

    
class PatientsFile(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="patient_files")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    file = models.FileField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.name
    
 
class Allergies(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="allergies_patient")
    allergie = models.CharField(max_length=200)
    reactions = models.CharField(max_length=200)

    def __str__(self):
        return self.allergie
    

#list dosage and how you take them, including non-prescription,herbs, birth control
class Medications(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="medication_patient")
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    instructions_of_use = models.CharField(max_length=100)

    def __str__(self):
        return self.medication_name
    

class PastMedicalIllnesses(models.Model):
    illness = models.CharField(max_length=100)

    def __str__(self):
        return self.illness
    
    
class Symptoms(models.Model):
    symptoms = models.CharField(max_length=100)
    
    def __str__(self):
        return self.symptoms


class PastMedicalOperations(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="operation_patient")
    operation = models.CharField(max_length=500)
    hospital = models.CharField(max_length=200)
    operation_date = models.DateField()
    hospitalization_time = models.CharField(max_length=200)

    def __str__(self):
        return self.operation


class SocialHistory(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="social_patient")
    occupation = models.CharField(max_length=200, null=True)
    is_marital = models.BooleanField()
    are_children = models.BooleanField()
    
    use_alcohol = models.BooleanField()
    how_often_use_alcohol = models.CharField(max_length=250, null=True)
    
    use_smoke = models.BooleanField()
    used_since = models.IntegerField()
    use_former_smoke = models.BooleanField()
    use_chew_tobacco = models.BooleanField()
    packs_per_days = models.CharField(choices=PacksPerDay.choices, default=PacksPerDay.ZERO, max_length=50, null=True)
    
    use_drugs = models.BooleanField()

    def __str__(self):
        return self.patient
    

class FamilyHealthHistory(BaseModel):
    patient = models.ForeignKey(to="patient.Patients",on_delete=models.CASCADE, related_name="family_patient")
    members = models.CharField(choices=FamilyMembers.choices, max_length=30)
    major_medical_problems = models.CharField(max_length=200, null=True)
    if_deceased_causes = models.CharField(max_length=300, null=True)
    age_at_date = models.IntegerField(null=True)
    
    def __str__(self):
        return self.members
    

#These models are for selections made with the get method.
class FamilyMembersNames(models.Model):
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    
    def __str__(self):
        return self.value


class FrequencyOfUse(models.Model):
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    
    def __str__(self):
        return self.value


class GenderOptionsNames(models.Model):
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    
    def __str__(self):
        return self.value
    