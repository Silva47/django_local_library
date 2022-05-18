from django.shortcuts import render
import keras
from keras.models import load_model
import cv2
import numpy as np
from pathlib import Path
import os
from django.core.files.storage import FileSystemStorage
import time
import logging
logging.basicConfig(level=logging.NOTSET)
labels = ['PNEUMONIA', 'NORMAL']
img_size = 150

def home(request):
    return render(request, 'index.html')

def get_training_data(data_dir):
    data = [] 
    for label in labels: 
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)
from keras.models import load_model
model=load_model(r'C:\Users\USER\Desktop\Project\Model\detectionsvm.tflearn', compile = True)
#predict

def getPredictionssvm(image, age, symptoms):
        #symptoms = BooleanField()
        from keras.models import load_model
        model=load_model(r'C:\Users\USER\Desktop\Project\Model\detectionsvm.tflearn', compile = True)
        silva = type(image)
        logging.debug("Test image type "+ str(silva))
        logging.debug("image gives "+ image)
        test_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        #out_array = np.array_str(test_image)
        test_image = cv2.resize(test_image,  (150,150))
        test_image = np.array(test_image).reshape( -1, img_size, img_size, 1)
        classes = ["Pneumonia Detected","Normal"]

        ans = model.predict({'conv2d_input': test_image })
        logging.debug("Ans gives "+ str(ans))
        if ans<= 60 and ans>= -60:
            if 'None of the above' in symptoms:
                return 'Normal'
            elif (('Fever'in symptoms) and ('Fatigue' in symptoms) and ('High body temperature' in symptoms) and (len(symptoms)==3) ):
                return 'Normal'
            elif len(symptoms)<=2 :
                return'Normal'
            else: return'Pneumonia Detected'
        
        else:
            ans1 = (ans >0.5).astype("int32")
            if ans1==0 :
                return'Pneumonia Detected'
            elif ans1 == 1 :
                return 'Normal'
            else:
                return 'Error'

def getPredictionscnn(image, age, symptoms):
        #symptoms = BooleanField()
        from keras.models import load_model
        model=load_model(r'C:\Users\USER\Desktop\Project\Model\detectioncnn.tflearn', compile = True)
        silva = type(image)
        logging.debug("Test image type "+ str(silva))
        logging.debug("image gives "+ image)
        test_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        #out_array = np.array_str(test_image)
        test_image = cv2.resize(test_image,  (150,150))
        test_image = np.array(test_image).reshape( -1, img_size, img_size, 1)
        classes = ["Pneumonia Detected","Normal"]
        time.sleep (5)
        ans = model.predict({'conv2d_input': test_image })
        logging.debug("Ans gives "+ str(ans))
        if ans<= 0.2 and ans>= -0.2:
            if 'None of the above' in symptoms:
                return 'Normal'
            elif (('Fever'in symptoms) and ('Fatigue' in symptoms) and ('High body temperature' in symptoms) and (len(symptoms)==3) ):
                return 'Normal'
            elif len(symptoms)<=2 :
                return'Normal'
            else: return'Pneumonia Detected'
        
        else:
            ans1 = (ans >0.5).astype("int32")
            if ans1==0 :
                return'Pneumonia Detected'
            elif ans1 == 1 :
                return 'Normal'
            else:
                return 'Error'


def result(request):
        fileObj  = request.FILES['image'] # here you get the files needed
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        image = '.'+filePathName
       
        #image = os.path.realpath(data)
        #logging.debug("data gives " + image)
    #age
        age = int(request.POST['age'])   
        logging.debug("age gives " + str(age))
    # symptoms = (request.GET['symptoms'])
        symptoms = []
#Fever
        try:
            symptoms1 = bool(request.POST['symptoms1'])
            symptoms.append ('Fever')
        except Exception as e:
            symptoms1 = False
#Chest Pain
        try:
            symptoms2 = bool(request.POST['symptoms2'])
            symptoms.append ('Chest Pain')
        except Exception as e:
            symptoms2 = False
#Fatigue
        try:
            symptoms3 = bool(request.POST['symptoms3'])
            symptoms.append ('Fatigue')
        except Exception as e:
            symptoms3 = False
#High body temperature
        try:
            symptoms4 = bool(request.POST['symptoms4'])
            symptoms.append ('High body temperature')
        except Exception as e:
            symptoms4 = False
#Nausea
        try:
            symptoms5 = bool(request.POST['symptoms5'])
            symptoms.append ('Nausea')
        except Exception as e:
            symptoms5 = False
#Shortness of breath
        try:
            symptoms6 = bool(request.POST['symptoms6'])
            symptoms.append ('Shortness of breath')
        except Exception as e:
            symptoms6 = False
#Runny nose
        try:
            symptoms7 = bool(request.POST['symptoms7'])
            symptoms.append ('Runny nose')
        except Exception as e:
            symptoms7 = False
#None of the above
        try:
            symptoms8 = bool(request.POST['symptoms8'])
            symptoms.append ('None of the above')
        except Exception as e:
            symptoms8 = False
        logging.debug("symptoms are " + str(symptoms))
       
        model_select = request.POST['model']
        logging.debug("Model is " + model_select)
        if model_select =='cnn':
            result = getPredictionscnn(image, age, symptoms)
        else :
            result = getPredictionssvm(image, age, symptoms)

        return render(request, 'result.html', {'result': result})
    
def end(request):
    Exit = request.POST['exit']
    return render(request, 'index.html', {'exit', end})