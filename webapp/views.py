from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.utils import timezone
from django import forms
from io import BytesIO
import zipfile
import requests
import json
import os
import ast

UTF8 = 'utf-8'
API_URL = "http://127.0.0.1:8000/polls/"

ROOT_TEMP = 'asset/temp/test'

class UploadDatasetForm(forms.Form):
    name = forms.CharField(max_length=320)
    dataset = forms.FileField(required=False)
    zipfile = forms.FileField(required=False)  
    directories = forms.CharField(required=False)
    
    CHOICES = [
        ('1', 'private'),
        ('2', 'public'),
    ]

    is_public = forms.ChoiceField(
        label="Publicity",
        widget=forms.RadioSelect,
        choices=CHOICES, 
        required=False,
    )

def bstr(byte_string, encoding=UTF8):
    return byte_string.decode(encoding)    

def get_request(request):
    template_name = 'webapp/empty.html'
    url = API_URL

    response = requests.get(url)

    context = { 'htmlstring': bstr(response.content)}
    return render(request, template_name, context)

def create_in_memory_zip_with_files_and_directories(files: list, directories: dict) -> bytes:
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zipf:
        for file in files:
            relative_file_path = directories.get(file.name)

            if not relative_file_path:
                continue
            
            zipf.writestr(relative_file_path, file.read())

    memory_file.seek(0)
    return memory_file.read()

def login_request(request):
    template_name = "registration/login_view.html"
    url = f"{API_URL}login-api/"
    context = {}

    if request.method != "POST":
        return render(request, template_name, context)

    username = request.POST["username"]
    password = request.POST["password"]

    request.session._get_or_create_session_key()
    data = {
        "session_key": request.session.session_key, 
        "username": username, 
        "password": password, 
    }
    
    response = requests.post(url, json=data)
    print(' --- ', request, request.user, request.user.is_authenticated, data['session_key'])
    print(' --- ', response)
    
    response_data = json.loads(response.text)
    print(' --- ', response)
    
    if response_data['is_authenticated'] == True:
        request.session['token'] = response_data['token']
        return redirect("/webapp/upload-dataset/")    

    return render(request, template_name, context)

def unzip_and_save(zipfile_dir, timestamp):

    return

def save_zip_file(zipfile, timestamp: str, root_dir: str = ROOT_TEMP):
    save_filename = f"{timestamp}-{zipfile.name}"
    zipfile_dir = os.path.join(root_dir, save_filename)

    FileSystemStorage(location=root_dir).save(save_filename, zipfile)     
    return zipfile_dir

def save_zip_bytes_file(bytes, filename='a_zip_file.zip', root_dir=ROOT_TEMP):
    with open(os.path.join(root_dir, filename), "wb") as binary_file:
        binary_file.write(bytes)
    return

def now_Ymd_HMS(format='%Y%m%d_%H%M%S') -> str:
    return timezone.now().strftime(format)

def upload_dataset(request, template_name = "webapp/upload_dataset.html", context = {}):
    if request.method != "POST":
        form = UploadDatasetForm()
        return render(request, template_name, {"form": form} | context)
    
    form = UploadDatasetForm(request.POST, request.FILES)
    
    ispublic = request.POST.get("is_public")
    name = request.POST.get("name")
    
    directories_str = request.POST.get("directories")

    data = {
        'name': name,
        'ispublic': ispublic,
    }
    files = {}
    headers = {
        "Authorization": "",
    }
    
    if directories_str:
        directories_dict = ast.literal_eval(directories_str)

    zipfile_list = request.FILES.getlist('zipfile')

    if len(zipfile_list) != 0:
        zipfile = zipfile_list[0] # <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>

        files['zipfile'] = zipfile

        timestamp = now_Ymd_HMS()
        zipfile_dir = save_zip_file(zipfile, timestamp)
        
        unzip_and_save(zipfile_dir, timestamp)

    dataset_files = request.FILES.getlist('file')

    if form.is_valid() and len(dataset_files) != 0 and len(directories_dict) != 0:
        zip_bytes_file = create_in_memory_zip_with_files_and_directories(dataset_files, directories_dict)
        timestamp = now_Ymd_HMS()
        files['zip_bytes_file'] = zip_bytes_file
        save_zip_bytes_file(zip_bytes_file)
    
    url = f"{API_URL}upload-dataset-api/"
    response = requests.post(url, json=data, files=files, headers=headers)
    
    response_data = json.loads(response.text)

    print(' - ', response_data)

    return render(request, template_name, {"form": form} | context)

def index(request):
    template_name = "webapp/index.html"
    base_html = "get_base_html(request.user.is_authenticated)"
    base_html = "base_guest.html"
    
    dataset_list = 'Dataset.objects.filter(is_public=True).order_by("-created")'
    paginator = 'Paginator(dataset_list, 2)'
    page_number = 'request.GET.get("dataset_page")'
    dataset_page_obj = 'paginator.get_page(page_number)'

    model_list = 'Model.objects.filter(is_public=True).order_by("-created")'
    model_paginator = 'Paginator(model_list, 2)'
    model_page_number = 'request.GET.get("model_page")'
    model_page_obj = 'model_paginator.get_page(model_page_number)'
    
    context = { 
        'base_html': base_html, 
        'dataset_page_obj': dataset_page_obj,
        'model_page_obj': model_page_obj,
    }

    return render(request, template_name, context)

def login(request, context={"please_login_message": "Please login to see this page."}):
    template_name = "registration/login_view.html"
    
    return render(request, template_name, context)

def logout_view(request):
    request.session['token'] = ''
    return redirect("/webapp/")
