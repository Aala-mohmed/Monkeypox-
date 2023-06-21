from django.shortcuts import render, redirect
import re
import time
import numpy as np
import pandas as pd
import io
from PIL import Image
from datetime import datetime, timedelta
from .models import RESULT,Registeration 

import plotly.express as px
import matplotlib.pyplot as plt

import plotly.graph_objects as go
import country_converter as coco
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
#****************************************************************************
from django.shortcuts import render
import os
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from register.forms import CreateUserForm




def registerpage(request):
    if request.user.is_authenticated:
       return redirect('check')
    else:
            form=CreateUserForm()
       
            form=CreateUserForm(request.POST)
            if form.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             email=form.cleaned_data.get('email')
             password1=form.cleaned_data.get('password1')
             password2=form.cleaned_data.get('password2')
             messages.success(request,'accout was created for ' + username)
             age=request.POST.get('age')
             
             gender=request.POST.get('gender')
             if gender=='option1':
                gender='female'
             else:
                gender='male'
             country=request.POST.get('country')      
             new_Registeration=Registeration(username=username,gender=gender,age=age,country=country,email=email,password1=password1,password2=password2 )
             new_Registeration.save() 

             return redirect('login')
             

    context={'form':form}
    return render(request,'register/register.html',context)



def loginpage(request):
    if request.user.is_authenticated:
       return redirect('check')
    else:
         if request.method=='POST':
             username= request.POST.get('username')
             password=request.POST.get('password')

             user=authenticate(request,username=username,password=password)

             if user is not None: 
                 login(request,user)
                 return redirect('check')
             else:
                 messages.info(request,'username OR password is incorrect')




             
         return render(request,'register/login.html',{})



def logoutuser(request):
    logout(request)
    return redirect('login') 


# Create your views here.






def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
def home (request):
       
       
            today = datetime.today()
            day   = today.day if today.day > 9 else '0' + str(today.day)
            month = today.month if today.month > 9 else '0' + str(today.month)
            today_str = '{}/{}/{}'.format(day, month, today.year)
            # Fetch data
            monkeypox_df = pd.read_csv("https://7rydd2v2ra.execute-api.eu-central-1.amazonaws.com/web/url?folder=&file_name=latest.csv")

            # Preprocess data
            monkeypox_df['Location'] = monkeypox_df['Location_information'].apply(lambda x: re.sub(r' \((.+?)$','',x))
            monkeypox_df['Location'] = monkeypox_df['Location'].apply(lambda x: re.sub(r'(.+?), United States','United States',x))
            monkeypox_df['County'] = [x.split(', ')[0] if len(x.split(', ')) > 1 else None for x in monkeypox_df['Location_information']]

            # Export to disk
            monkeypox_df.to_csv('monkeypox_df.csv', index = False)

            # Cases by country
            country_cases_df = monkeypox_df.loc[monkeypox_df['Case_status'] == 'confirmed',['_id','Location']].groupby('Location').agg('count').reset_index().rename({'_id':'Count'}, axis = 1)
            country_cases_df.to_csv('monkeypox_cases_by_country.csv', index = False)
            num_confirmed_cases = monkeypox_df.loc[monkeypox_df['Case_status'] == 'confirmed'].shape[0]

         
            fig = plt.figure(figsize = (20,10))
            fig.patch.set_facecolor('#d6b48088')

            plt.text(x = 0.32,
                     y = 0.4,
                     s = str(num_confirmed_cases),
                     multialignment = 'center',
                     fontsize = 150,
                     color = '#38cae0'
                    )

            plt.text(x = 0.37,
                     y = 0.34,
                     s = 'Confirmed cases as of {}'.format(today_str),fontsize = 20,
                     multialignment = 'center',
                     color = '#ffffff'
                    )

            plt.axis('off')
            # Getting the current figure and save it in the variable.
            fig = plt.gcf()
            img = fig2img(fig)
           
            # Save image with the help of save() Function.
            img=  img.save('register/static/register/plots/plot1.png')

            #**************************fig2*******************************************
           
            filtered_df = monkeypox_df.loc[monkeypox_df['Case_status'] == 'confirmed']
            map_df = filtered_df[['Location','_id']].groupby('Location').agg('count').reset_index()
            map_df['CountryCode'] = coco.convert(names = map_df['Location'], to = 'ISO3')
            map_df.rename({'_id':'Count of Confirmed Cases'}, axis = 1, inplace = True)

        
            fig = px.choropleth(map_df,
                                locations = "CountryCode",
                                color = "Count of Confirmed Cases",
                                hover_name = "Location",
                                color_continuous_scale = ["#d7e1ee", "#cbd6e4", "#bfcbdb", "#b3bfd1", "#a4a2a8", "#df8879", "#c86558", "#b04238", "#991f17"],
                                projection = 'natural earth',
                                template = 'plotly_dark',
                                title = 'Geographical Distribution of Confirmed Cases<br><sub>Natural Projection</sub>',
                                height = 800,
                                width = 1120,
                                )

            fig.update_geos(lataxis_showgrid = True,
                            lonaxis_showgrid = True,
                            showcountries = True,
                            )

            fig.update_geos(lataxis = {'gridcolor':'#222222'},
                            lonaxis = {'gridcolor':'#222222'},
                            )

           
            # Getting the current figure and save it in the variable.
           
            fig = plt.gcf()
            img2 = fig2img(fig)
         
            
            # Save image with the help of save() Function.
            img2=img2.save('register/static/register/plots/plot2.png')
      
            #****************fig3**************************
            
            fig = px.choropleth(map_df,
                    locations = "CountryCode",
                    color = "Count of Confirmed Cases",
                    hover_name = "Location",
                    color_continuous_scale = ["#d7e1ee", "#cbd6e4", "#bfcbdb", "#b3bfd1", "#a4a2a8", "#df8879", "#c86558", "#b04238", "#991f17"],
                    projection = 'orthographic',
                    template = 'plotly_dark',
                    title = 'Geographical Distribution of Confirmed Cases<br><sub>Orthographic Projection</sub>',
                    height = 800,
                    width = 1120,
                   )

            fig.update_geos(lataxis_showgrid = True,
                            lonaxis_showgrid = True,
                            showcountries = True,
                           )

            fig.update_geos(lataxis = {'gridcolor':'#222222'},
                            lonaxis = {'gridcolor':'#222222'},
                           )
            # Getting the current figure and save it in the variable.
            fig = plt.gcf()
            img3 = fig2img(fig)
            
            # Save image with the help of save() Function.
            img3=img3.save('register/static/register/plots/plot3.png')


           
            

            return render(request,'register/home.html',{" img ": img,"img2":img2 ,"img3":img3 })











class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

@login_required(login_url='login')
def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        # image details
        image_url = fss.url(_image)
        # Read the image

        imag=cv2.imread(path)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((224, 224))

        test_image =np.expand_dims(resized_image, axis=0) 

        # load model
        model = tf.keras.models.load_model(os.getcwd() + './models/finalizedmodel.h5')

        result = model.predict(test_image) 

      
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "Monkeypox"
        elif (np.argmax(result) == 1):
            prediction = "Others"
        elif (np.argmax(result) == 2):
            prediction = "Normal"
        else:
            prediction = "Unknown"
        
        if request.method=='POST':        
    
           try:
               new_Registeration=RESULT(username= Registeration.objects.get(username=request.user),predction=prediction)
               new_Registeration.save()
          
           except IntegrityError:
               RESULT.objects.filter(pk=Registeration.objects.get(username=request.user)).update(predction=prediction)
           

        return TemplateResponse(
            request,
            "predict/index.html",
            {
                "message": message,
                "image": image,
                "image_url": image_url,
                "prediction": prediction,
               
                
            },
        )
            
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "predict/index.html",
            {"message": "No Image Selected"},
        )

