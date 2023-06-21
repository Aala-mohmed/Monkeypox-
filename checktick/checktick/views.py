from django.shortcuts import render
import os
import cv2
from PIL import Image
import numpy as np
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from django.utils.datastructures import MultiValueDictKeyError
from django.template.response import TemplateResponse
from django.conf import settings






class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def predictImage(request):
    message = ""
    prediction = ""
    fs = CustomFileSystemStorage()
    try:
        fileobj= request.FILES["image"]
        filename=fs.save(fileobj.name,fileobj)
        filename=fs.url(filename)
        testimage='.'+filename
        img=tf.keras.utils.load_img(testimage,target_size=(224,224))
        x=image.img_to_array(img)
        x=x.reshape(1,2224,224,3)

       

        # load model
        model = tf.keras.models.load_model(os.getcwd() + './models/model.h5')

        result = model.predict(x) 
    
        print("Prediction: " + str(np.argmax(result)))

        if (np.argmax(result) == 0):
            prediction = "MonkeyPox"
        elif (np.argmax(result) == 1):
            prediction = "Others"
        
        else:
            prediction = "Unknown"
        
        return TemplateResponse(
            request,
            "test.html",
            {
                "message": message,
                "image": image,
                "filename": filename,
                "prediction": prediction,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "test.html",
            {"message": "No Image Selected"},
        )