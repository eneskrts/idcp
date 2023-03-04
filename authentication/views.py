from django.core.validators import EmailValidator
from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import City, Country, User, Experience, Education, Profile, Profession, Employee
from authentication.serializers import EmployeeSerializer, UpdateUserSerializer, CitySerializer, CountrySerializer, \
    UserSerializer, ExperienceSerializer, EducationSerializer, ProfileSerializer, ProfessionSerializer, \
    ResetPasswordRequestSerializer, ChangePasswordSerializer, TokenValitationSerializer, ResetPasswordSerializer, \
    ResendActivationSerializer
from authentication.models import City, Country, User, Experience, Education, Profile, Profession, Employee, TitleNames, CurrencyUnitNames
from authentication.serializers import EmployeeSerializer, UpdateUserSerializer, CitySerializer, CountrySerializer, UserSerializer, ExperienceSerializer, EducationSerializer, ProfileSerializer, ProfessionSerializer, TitleSerializer, CurrencyUnitSerializer
from rest_framework.viewsets import mixins

# Filterset
from django_filters import FilterSet, DateTimeFromToRangeFilter, rest_framework as filters
from django_filters.widgets import RangeWidget

from utils.mail import send_mail
from utils.user import UserMailActivation


class ProfileFilter(FilterSet):
    country = filters.CharFilter(label="Country")
    class Meta:
        model = Profile
        fields = ["name","country","is_employee"]
        
        
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
            
            if self.data["is_employee"]:
                queryset = queryset.filter(is_employee=True)
                
            return queryset
        
        return queryset
    



class CityViewSet(viewsets.ModelViewSet):

    queryset = City.objects.all()
    serializer_class = CitySerializer


class CountryViewSet(viewsets.ModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.filter(is_accepted=True)
    serializer_class = UserSerializer
    def perform_create(self, serializer): # NOQA
        instance = serializer.save()
        send_mail(
            instance.email, 'Welcome to the app',
            "Merhaba Üyeliğin aktivasyonu için bir adım kaldı",
            instance, 'mail_activate',
        )

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



class ResendActivationViewSet(viewsets.ViewSet):
    serializer_class = ResendActivationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        send_mail(user.email, 'Welcome to the app',
                  "Merhaba Üyeliğin aktivasyonu için bir adım kaldı",
                  user, 'mail_activate')
        return Response(status=status.HTTP_200_OK)


class ResetPasswordRequest(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    url = "reset_password_api"

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        send_mail(email, "Şifre Sıfırlama maili",
                  "Merhaba aşağıdaki linkten şifrenizi sıfırlayabilirsiniz",
                  user, self.url)
        return Response(status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object() # NOQA
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response(status=status.HTTP_200_OK)


class CheckTokenApiView(GenericAPIView):
    def get(self, request, uidb64, token):
        user = None
        uid_is_valid = EmailValidator.uid_validator(uidb64)
        if uid_is_valid:
            user = UserMailActivation.validate_token(uidb64, token)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class MailActivateApiView(GenericAPIView):
    serializer_class = TokenValitationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data.get('uidb64')
        token = serializer.validated_data.get('token')
        user = None
        uid_is_valid = EmailValidator.uid_validator(uid)
        if uid_is_valid:
            user = UserMailActivation.validate_token(uid, token)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data.get('uidb64')
        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('password')
        user = None
        uid_is_valid = EmailValidator.uid_validator(uid)
        if uid_is_valid:
            user = UserMailActivation.validate_token(uid, token)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class TitleNamesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = TitleNames.objects.all()
    serializer_class = TitleSerializer


class CurrencyUnitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = CurrencyUnitNames.objects.all()
    serializer_class = CurrencyUnitSerializer
