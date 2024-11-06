from django.shortcuts import render
import requests

UTF8 = 'utf-8'
API_URL = "http://127.0.0.1:8000/polls/"

def bstr(byte_string, encoding=UTF8):
    return byte_string.decode(encoding)    

def get_request(request):
    template_name = 'webapp/empty.html'
    url = API_URL

    response = requests.get(url)

    context = { 'htmlstring': bstr(response.content)}
    return render(request, template_name, context)

def login_request(request):
    template_name = "registration/login_view.html"
    url = f"{API_URL}login-api/"
    context = {}

    if request.method != "POST":
        return render(request, template_name, context)

    username = request.POST["username"]
    password = request.POST["password"]
    print(' --- login request() ', username, password)

    data = {
        "csrf_token": '',
        "username": "ace",
        "password": "ace13324",
    }
    
    response = requests.post(url, json=data)
    print(response, response.content)

    return render(request, template_name, context)

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
