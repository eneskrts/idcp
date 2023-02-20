from rest_framework import permissions
from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MEBRE API",
        default_version='v1',
        description="MEBRE API DESCRIPTION",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@mebre"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/swagger/', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),

    path('api/api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]