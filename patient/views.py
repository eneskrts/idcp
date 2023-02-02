from django.shortcuts import render
from .models import *
from .serializers import *
#API
from rest_framework import viewsets
from rest_framework.viewsets import mixins
from rest_framework.response import Response


# Create your views here.


class PatientsViewSet(viewsets.ModelViewSet):
    
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer


class PatientsFileViewSet(viewsets.ModelViewSet):
    
    queryset = PatientsFile.objects.all()
    serializer_class = PatientsFileSerializer



class AllergiesViewSet(viewsets.ModelViewSet):
    
    queryset = Allergies.objects.all()
    serializer_class = AllergiesSerializer


class MedicationsViewSet(viewsets.ModelViewSet):
    
    queryset = Medications.objects.all()
    serializer_class = MedicationsSerializer


class PastMedicalIllnessesViewSet(viewsets.ModelViewSet):
    
    queryset = PastMedicalIllnesses.objects.all()
    serializer_class = PastMedicalIllnessesSerializer


class PastMedicalOperationsViewSet(viewsets.ModelViewSet):
    
    queryset = PastMedicalOperations.objects.all()
    serializer_class = PastMedicalOperationsSerializer


class SocialHistoryViewSet(viewsets.ModelViewSet):
    
    queryset = SocialHistory.objects.all()
    serializer_class = SocialHistorySerializer


class FamilyHealthHistoryViewSet(viewsets.ModelViewSet):
    
    queryset = FamilyHealthHistory.objects.all()
    serializer_class = FamilyHealthHistorySerializer