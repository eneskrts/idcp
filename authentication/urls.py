from rest_framework_simplejwt import views as jwt_views
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from authentication import views
from authentication.views import ChangePasswordView, ResetPasswordApiView, CheckTokenApiView, ResetPasswordRequest, \
    MailActivateApiView

router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'experience', views.ExperienceViewSet)
router.register(r'educations', views.EducationViewSet)
router.register(r'professions', views.ProfessionViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'users/update', views.UpdateUser)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'title_names',views.TitleNamesViewSet)
router.register(r'currency_unit',views.CurrencyUnitViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset_password_confirm/', ResetPasswordApiView.as_view(), name='reset_password_confirm'),
    path('activation_control/<uidb64>/<token>/', CheckTokenApiView.as_view(), name='activation_control_api'),
    path('reset_password_request/', ResetPasswordRequest.as_view(), name='reset_password_api'),
    path('mail_activate/', MailActivateApiView.as_view(), name='mail_activate'),
]
