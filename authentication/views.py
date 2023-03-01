from rest_framework import viewsets
from authentication.models import City,Country,User,Experience,Education,Profile,Profession
from authentication.serializers import UpdateUserSerializer,CitySerializer,CountrySerializer,UserSerializer,ExperienceSerializer,EducationSerializer,ProfileSerializer,ProfessionSerializer

# Filterset
from django_filters import FilterSet, DateTimeFromToRangeFilter, rest_framework as filters
from django_filters.widgets import RangeWidget


class UserFilter(FilterSet):
    country = filters.CharFilter(label="Country")
    class Meta:
        model = User
        fields = ["username","country"]
        
        
    def filter_queryset(self, queryset):
        if self.data:
            if self.data["country"]: 
                country = self.data["country"]
                
                queryset = queryset.filter(profile__city__country__name=country)
            
            return queryset
        
        return queryset
    




class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CountryViewSet(viewsets.ModelViewSet):   
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
 
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