from django.db import models
from django_countries.fields import CountryField


# Create your models here.





class Registeration(models.Model):
    
    username = models.TextField(max_length=100,primary_key=True) 
    email=models.EmailField(max_length = 254, default='non')
    password1 = models.CharField(max_length=50, default=0)
    password2 = models.CharField(max_length=50, default=0)
    gender=models.TextField()
    country = models.TextField(max_length=100)
    age=models.IntegerField()
    

    def __str__(self) ->str :
        return self.username


class RESULT(models.Model):
     predction=models.TextField(max_length=100 )
     username= models.OneToOneField(Registeration,on_delete=models.CASCADE,primary_key=True,default='noo' )
     def __str__(self) ->str :
        return self.predction








