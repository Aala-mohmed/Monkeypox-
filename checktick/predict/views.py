from django.shortcuts import render
#from register.models import RESULT,Registeration 
# Create your views here.
import os
import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from register.forms import CreateUserForm
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
            prediction = "nonMonkeypox"
        elif (np.argmax(result) == 2):
            prediction = "Normal"
        else:
            prediction = "Unknown"
       

        new_pre=RESULT(predction=prediction )
        new_pre.save() 

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
def result(request):
     if request.method=='POST':
        username=request.POST['username']
        gender=request.POST['gender']
        age=request.POST['age']
        country=request.POST['country']
        if gender=='option2':
            gender='male'
        else:
            gender='female'
        new_Registeration=Registeration(username=username,gender=gender,age=age,country=country ,prediction=prediction)
        new_Registeration.save() 
        