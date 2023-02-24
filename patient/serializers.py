from rest_framework import serializers
from .models import *
from .enums import *
        
        
class PatientsSerializer(serializers.ModelSerializer):
    
    patient_files = serializers.SerializerMethodField('_get_patient_files')
    allergies = serializers.SerializerMethodField('_get_allergies')
    medications = serializers.SerializerMethodField('_get_medications')
    past_medical_operations = serializers.SerializerMethodField('_get_past_medical_operations')
    social_history = serializers.SerializerMethodField('_get_social_history')
    family_health_history = serializers.SerializerMethodField('_get_family_health_history')
    
    
    class Meta:
        model = Patients
        fields = "__all__"
        
        
    def _get_patient_files(self, obj):
        user = obj.id
        data = PatientsFile.objects.filter(patient=user).values()
        return data
        
    def _get_allergies(self, obj):
        user = obj.id
        data = Allergies.objects.filter(patient=user).values()
        return data
        
    def _get_medications(self, obj):
        user = obj.id
        data = Medications.objects.filter(patient=user).values()
        return data
        
        
    def _get_past_medical_operations(self, obj):
        user = obj.id
        data = PastMedicalOperations.objects.filter(patient=user).values()
        return data
        
        
    def _get_social_history(self, obj):
        user = obj.id
        data = SocialHistory.objects.filter(patient=user).values()
        return data
        
        
    def _get_family_health_history(self, obj):
        user = obj.id
        data = FamilyHealthHistory.objects.filter(patient=user).values()
        return data
    
    class Meta:
        model = Patients
        fields = "__all__"
        
    # def create(self, validated_data):
    #     instance = super().create(validated_data)
    #     for i in FamilyMembers:
    #         FamilyHealthHistory.objects.create(patient=instance,members=i)
    #     return instance
        

class PatientsFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PatientsFile
        fields = "__all__"
        
        
class AllergiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Allergies
        fields = "__all__"
        
        
class MedicationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Medications
        fields = "__all__"
        
        
class PastMedicalIllnessesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastMedicalIllnesses
        fields = "__all__"
        
        
class SymptomsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Symptoms
        fields = "__all__"
        
        
class PastMedicalOperationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastMedicalOperations
        fields = "__all__"
        
        
class SocialHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SocialHistory
        fields = "__all__"
        
        
class FamilyHealthHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FamilyHealthHistory
        fields = "__all__"
        

#These serializers are for selections made with the get method.
class FamilyMembersNamesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FamilyMembersNames
        fields = "__all__"


class FrequencyOfUseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FrequencyOfUse
        fields = "__all__"


class GenderOptionsNamesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GenderOptionsNames
        fields = "__all__"
        