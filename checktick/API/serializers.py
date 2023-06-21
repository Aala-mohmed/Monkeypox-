from rest_framework import serializers
from register.models import *


class Registertionserializer(serializers.ModelSerializer):

  class Meta:
	  model=Registeration
	  fields="__all__"
	   




class Resultserializer(serializers.ModelSerializer):

  class Meta:
	  model= RESULT
	  fields="__all__"
	  