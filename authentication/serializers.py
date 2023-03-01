from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import City ,Country, Experience, Education, User, Profession, Profile, Employee


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model=City
        fields=('__all__')

    def to_representation(self, instance):
        rep = super(CitySerializer, self).to_representation(instance)
        rep['country'] = instance.country.name
        return rep


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model=Country
        fields=('__all__')


class ProfessionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Profession
        fields=('__all__')

    def get_children(self, obj):
        return ProfessionSerializer(obj.get_children(), many=True).data


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ('__all__')


class ExperienceSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Experience
        fields = ('__all__')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('__all__')
        extra_kwargs= { 'user': { 'read_only' : True } }

    def get_avatar(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.avatar.url)


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    experience = serializers.SerializerMethodField('get_experience_info')
    education = serializers.SerializerMethodField('get_education_info')
    employee = EmployeeSerializer(read_only=True, source='profile.employee')
    is_accepted = serializers.SerializerMethodField('check_id_card')

    class Meta:
        model = User
        fields = ('id', 'username', 'timezone', 'id_card', 'password', 'profile',
                  'experience', 'education', 'employee', 'is_accepted')
        extra_kwargs = {'password': {'write_only': True}}


    def get_id_card(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.id_card.url)


    def check_id_card(self,obj):
        is_accepted = obj.is_accepted
        if ( is_accepted is False) :
            error = {'message': _("Teşekkür ederiz! Başvurunuz tarafımızca incelenecek.")}
            #raise serializers.ValidationError(error)

    def get_experience_info(self,obj):
        data={}
        experiences = obj.experience.all()
        for experience in experiences:
            experience_data = {
                experience.id : {"experience_place": experience.experience_place,
                                "description": experience.description,
                                "city": experience.city.name,
                                "start_year": experience.start_year,
                                "end_year": experience.end_year}
            }
            data.update(experience_data)
        return data

    def get_education_info(self,obj):
        data={}
        educations = obj.education.all()
        for education in educations:
            education_data = {
                education.id : {"education_place": education.education_place,
                                "education_branch": education.education_branch,
                                "start_year": education.start_year,
                                "end_year": education.end_year,
                                "city": education.city.name,}
            }
            data.update(education_data)
        return data
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('timezone', 'username', 'id_card', 'profile')
        extra_kwargs = {'password': {'read_only': True}}

    def save(self, **kwargs):
        profile = self.validated_data.pop('profile')
        instance = super().save(**kwargs)
        Profile.objects.update_or_create(user=instance, defaults=profile)
        return instance
