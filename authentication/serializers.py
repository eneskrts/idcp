from authentication.models import City,Country,Experience,Education,User,Profession,Profile
from rest_framework import serializers

class CitySerializer(serializers.ModelSerializer):    
    class Meta:
        model=City
        fields=('id','country','name')

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
        fields = ('user','experience_place','description','city','start_year','end_year')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('birth_date','city','profession','avatar','treatment_methods','scientific_publications',
        'professional_memberships','professional_awards_degree','vocational_courses_conferences')
        extra_kwargs= { 'user': { 'read_only' : True } }
   
    def get_avatar(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.avatar.url)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    experience = serializers.SerializerMethodField('get_experience_info')
    education = serializers.SerializerMethodField('get_education_info')

    class Meta:
        model = User
        fields = ('id','phone','timezone','username','password','profile','experience','education') 
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_experience_info(self,obj):
        data={}
        experiences = obj.experience.all()
        for experience in experiences:
            experience_data = {
                experience.id : {"experience_place": experience.experience_place,
                                "description":experience.description,
                                "city":experience.city.name,
                                "start_year":experience.start_year,
                                "end_year":experience.end_year}
            }
            data.update(experience_data)
        return data
    
    def get_education_info(self,obj):
        data={}
        educations = obj.education.all()
        for education in educations:
            education_data = {
                education.id : {"education_place": education.education_place,
                                "education_branch":education.education_branch,
                                "start_year":education.start_year,
                                "end_year":education.end_year,
                                "city":education.city.name,}
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
        fields = ('phone','timezone','username','profile') 
        extra_kwargs = {'password': {'read_only': True}}

    def save(self, **kwargs):
        profile = self.validated_data.pop('profile')
        instance = super().save(**kwargs)
        Profile.objects.update_or_create(user=instance, defaults=profile)
        return instance  