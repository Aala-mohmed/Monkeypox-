"""checktick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from register.views import home,registerpage,loginpage,logoutuser, index
from.views import predictImage
from about.views import About 
from rest_framework import  routers
from django.urls import  include
from API import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
router=routers.DefaultRouter()
router.register('Registeration',views.RegisterViewSet)
router.register('Result',views.ResultrViewSet)

urlpatterns = [
    path('api_schema',get_schema_view(title='API Schema',description='Guide for the REST API '),name='api_schema'), 
    path('swagger-ui/', TemplateView.as_view(
        template_name='API/docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('hom/',home ,name="home"),
    path('register/',registerpage ,name="register"),
    path('login/',loginpage ,name="login"),
    path('logout/',logoutuser ,name="logout"),
    path('pre/',index ,name="check"),
    path('about/',About ,name="about"),
    path('',include('API.urls')),
    path('',include(router.urls)),
]
if settings.DEBUG:
    # setting this to view media files from admin panel
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

