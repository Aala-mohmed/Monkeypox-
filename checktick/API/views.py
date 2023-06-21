from django.shortcuts import render
from register.models import Registeration,RESULT 
# Create your views here.
#************************API*************
from .serializers import  Registertionserializer,Resultserializer
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny




class  RegisterViewSet(viewsets.ModelViewSet):
     queryset=Registeration.objects.all()
     serializer_class=Registertionserializer
     



class  ResultrViewSet(viewsets.ModelViewSet):
     queryset=RESULT.objects.all()
     serializer_class=Resultserializer
     

