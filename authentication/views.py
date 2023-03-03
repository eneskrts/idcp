from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from authentication.models import City, Country, User, Experience, Education, Profile, Profession, Employee, TitleNames, CurrencyUnitNames
from authentication.serializers import EmployeeSerializer, UpdateUserSerializer, CitySerializer, CountrySerializer, UserSerializer, ExperienceSerializer, EducationSerializer, ProfileSerializer, ProfessionSerializer, TitleSerializer, CurrencyUnitSerializer
from rest_framework.viewsets import mixins


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


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class UpdateUser(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


class TitleNamesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = TitleNames.objects.all()
    serializer_class = TitleSerializer


class CurrencyUnitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    queryset = CurrencyUnitNames.objects.all()
    serializer_class = CurrencyUnitSerializer
