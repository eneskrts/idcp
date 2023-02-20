from rest_framework import viewsets
from authentication.models import City,Country,User,Experience,Education,Profile,Profession
from authentication.serializers import UpdateUserSerializer,CitySerializer,CountrySerializer,UserSerializer,ExperienceSerializer,EducationSerializer,ProfileSerializer,ProfessionSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CountryViewSet(viewsets.ModelViewSet):   
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
 
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ProfessionViewSet(viewsets.ModelViewSet): 
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UpdateUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer