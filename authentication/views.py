from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from authentication.models import City, Country, User, Experience, Education, Profile, Profession, Employee
from authentication.serializers import EmployeeSerializer, UpdateUserSerializer, CitySerializer, CountrySerializer, UserSerializer, ExperienceSerializer, EducationSerializer, ProfileSerializer, ProfessionSerializer

# Filterset
from django_filters import FilterSet, DateTimeFromToRangeFilter, rest_framework as filters
from django_filters.widgets import RangeWidget


class ProfileFilter(FilterSet):
    country = filters.CharFilter(label="Country")
    class Meta:
        model = Profile
        fields = ["name","country"]
        
        
    def filter_queryset(self, queryset):
        if self.data:
            if self.data["country"]: 
                country = self.data["country"]
                
                queryset = queryset.filter(city__country__name=country)
            
            if self.data["name"]:
                name = self.data["name"]
                
                if len(self.data["name"]) == 1:
                    queryset = queryset.filter(name__istartswith=name)
                        
                else:
                    queryset = queryset.filter(name=name)
            
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

    parser_classes = [MultiPartParser]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProfileFilter


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class UpdateUser(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
