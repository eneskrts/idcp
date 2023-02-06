from rest_framework_simplejwt import views as jwt_views
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from authentication import views
router = routers.DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'experience', views.ExperienceViewSet)
router.register(r'educations', views.EducationViewSet)
router.register(r'professions', views.ProfessionViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'users/update', views.UpdateUser)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]