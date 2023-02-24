from django.shortcuts import render
from .models import *
from .serializers import *
#API
from rest_framework import viewsets
from rest_framework.viewsets import mixins
from rest_framework.response import Response
# Filterset
from django_filters import FilterSet, DateTimeFromToRangeFilter, rest_framework as filters


# Create your views here.

#filterSets
class PatientsFilter(FilterSet):
    class Meta:
        model = Patients
        fields = ["primary_doctor"]


#ViewSets
class PatientsViewSet(viewsets.ModelViewSet):
    
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PatientsFilter


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


class SymptomsViewSet(viewsets.ModelViewSet):
    
    queryset = Symptoms.objects.all()
    serializer_class = SymptomsSerializer


class PastMedicalOperationsViewSet(viewsets.ModelViewSet):
    
    queryset = PastMedicalOperations.objects.all()
    serializer_class = PastMedicalOperationsSerializer


class SocialHistoryViewSet(viewsets.ModelViewSet):
    
    queryset = SocialHistory.objects.all()
    serializer_class = SocialHistorySerializer


class FamilyHealthHistoryViewSet(viewsets.ModelViewSet):
    
    queryset = FamilyHealthHistory.objects.all()
    serializer_class = FamilyHealthHistorySerializer


#These views are for selections made with the get method.
class FamilyMembersNamesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = FamilyMembersNames.objects.all()
    serializer_class = FamilyMembersNamesSerializer


class FrequencyOfUseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = FrequencyOfUse.objects.all()
    serializer_class = FrequencyOfUseSerializer


class GenderOptionsNamesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = GenderOptionsNames.objects.all()
    serializer_class = GenderOptionsNamesSerializer