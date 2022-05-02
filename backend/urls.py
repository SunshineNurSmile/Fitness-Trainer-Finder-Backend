"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger yaml for open API
schema_view = get_schema_view(
   openapi.Info(
      title="UJourney API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="hoge@hoge.jp"),
      license=openapi.License(name="TEST License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('base.urls.users')),
    path('api/orders/', include('base.urls.orders')),
    path('api/messages/', include('base.urls.messages')),

    # swagger urls
    re_path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),     # Swagger-Editor用 json or yaml形式 ダウンロード
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),   # Swagger-UI形式
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),       # Redoc形式
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)