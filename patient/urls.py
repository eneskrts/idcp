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
router.register(r'past_medical_operations',views.PastMedicalOperationsViewSet)
router.register(r'social_history',views.SocialHistoryViewSet)
router.register(r'family_health_history',views.FamilyHealthHistoryViewSet)

urlpatterns = [
    path('',include(router.urls))
    ]