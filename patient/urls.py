from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'patients',views.PatientsViewSet)
router.register(r'patients_file',views.PatientsFileViewSet)
router.register(r'allergies',views.AllergiesViewSet)
router.register(r'medications',views.MedicationsViewSet)
router.register(r'past_medical_illnesses',views.PastMedicalIllnessesViewSet)
router.register(r'Symptoms',views.SymptomsViewSet)
router.register(r'past_medical_operations',views.PastMedicalOperationsViewSet)
router.register(r'social_history',views.SocialHistoryViewSet)
router.register(r'family_health_history',views.FamilyHealthHistoryViewSet)
router.register(r'family_members_names',views.FamilyMembersNamesViewSet)
router.register(r'frequency_of_use',views.FrequencyOfUseViewSet)
router.register(r'gender_options_names',views.GenderOptionsNamesViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('download/',views.DownloadFile.as_view(),name="file_download")
    ]