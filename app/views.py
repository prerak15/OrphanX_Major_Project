from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from glob import glob
from ml.runner import process
import os
import csv
import pandas as pd
# from ml.runner
# Create your views here.

def index(req):
    return render(req,'index.html')

def landpage(req):
    return render(req,'landing.html')

def formpageP(req):
    return render(req,'formParent.html')
def formpageC(req):
    return render(req,'formChild.html')

def handle_file_upload_parent(request):
    if request.method == 'POST' and 'Father' in request.FILES and 'Mother' in request.FILES:
        Father = request.FILES['Father']
        Mother = request.FILES['Mother']
        data_dir = os.path.join(settings.BASE_DIR, 'parent')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(os.path.join(data_dir, Father.name), 'wb') as f:
            for chunk in Father.chunks():
                f.write(chunk)
        with open(os.path.join(data_dir, Mother.name), 'wb') as f:
            for chunk in Mother.chunks():
                f.write(chunk)
        images = glob("static\\" + "*.jpg")
        images_final = []
        csv_dir = os.path.join(settings.BASE_DIR, 'childdet')
        csv_path = os.path.join(csv_dir, 'childdet.csv')
        df = pd.read_csv(csv_path)
        details_final = []
        for i in images:
            score = process(Father.name[-13:], Mother.name[-13:], i[-13:])
            print(score, i)
            if score >= 0.75:
                images_final.append('\\'+i)
                details = df.loc[df['image_name'] == i[-13:]]
                details = details.values.tolist()
                details = details[0]
                details.append(score)
                details_final.append(details)
        print(images_final)

        print(details_final)
        field_names = ['First Name', 'Last Name', 'Reg No.', 'BloodType', 'Ethnicity', 'Age', 'Comments', 'Image Name','Score']
        for i in range(len(details_final)):
            for j in range(len(details_final[i])):
                details_final[i][j] = field_names[j] + ": " + str(details_final[i][j])
        
        # img_range = [i for i in range(len(images_final))]
        res = dict(zip(images_final, details_final))
        return render(request, 'index.html', dict(images=res))
            
    else:
        return render(request, 'index.html')
    
def handle_file_upload_child(request):
    if request.method == 'POST' and 'csv-file' in request.FILES:
        csv_file = request.FILES['csv-file']
        data_dir = os.path.join(settings.BASE_DIR, 'static')
        details = request.POST
        print(details)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(os.path.join(data_dir, csv_file.name), 'ab') as f:
            for chunk in csv_file.chunks():
                f.write(chunk)
        csv_dir = os.path.join(settings.BASE_DIR, 'childdet')
        if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
                
        field_names = ['fname', 'lname', 'Number', 'BloodType', 'Ethnicity', 'Age', 'comments', 'image_name']
        
        details_dict = details.dict()

        del details_dict['csrfmiddlewaretoken']
        details_dict['image_name'] = csv_file.name[-13:]
        csv_path = os.path.join(csv_dir, 'childdet.csv')

        print(details_dict)
        print(type(details_dict))

        with open(csv_path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writerow(details_dict)
            
        return render(request, 'landing.html') 
            
    else:
        return render(request, 'landing.html')
    
def child_details_display(request):
    csv_dir = os.path.join(settings.BASE_DIR, 'childdet')
    csv_path = os.path.join(csv_dir, 'childdet.csv')
    df = pd.read_csv(csv_path)
    
    if request.method == 'POST':
        child = request.POST
        details = df.loc[df['image_name'] == child.name]
        details = details.tolist()
        return render(request, 'childDetails.html', {'details':details}) 

    else:   
        return render(request, 'childDetails.html')
