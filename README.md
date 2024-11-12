# ku_django_frntnd
 
## Testing

```sh
python manage.py test polls

# output messsage
Found 10 test(s).
Creating test database for alias 'default'...
Got an error creating the test database: source database "template1" is being accessed by other users
DETAIL:  There are 5 other sessions using the database.
```

## Clearing Django cache

```sh
# python manage.py shell

from django.db import connections, transaction
from django.core.cache import cache # This is the memcache cache.

cache.clear()
```

## Designing Web Layout

Forms
https://getbootstrap.com/docs/5.3/forms/input-group/#basic-example

## Making HTML Templates

Template  
https://docs.djangoproject.com/en/5.1/ref/templates/language/

## Deleting all data in database tables

```sh
python manage.py flush
```

## Resolving 'polls' is not a registered namespace

> "django.urls.exceptions.NoReverseMatch: 'polls' is not a registered namespace"

At main application folder where `settings.py`, `asgi.py`, `wsgi.py` files are:  
Ensure to add `namespace='polls'`.  
Ensure to match the application folder name `polls`.

`ku_djangoo/urls.py`

```py
urlpatterns = [
    path('polls/', include('polls.urls', namespace='polls')),
    ...
]
```

Ensure correct spellings such as `app_name`, check wrong spellings such as `app_names`.  

`polls/urls.py`

```py
app_name = 'polls'
```

`manage.py`

```py
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ku_djangoo.settings')
```

`settings.py`

```py
ROOT_URLCONF = 'ku_djangoo.urls' 
```

## Saving Python Packages and versions

```sh
pip freeze > requirements.txt
```

## Hiding Sidebar at mobile screen

Bootstrap
Layout Breakpoints

| Breakpoint | Class infix | Dimensions |
| - | - | - |
| Extra small | None |  <576px |
| Small | sm | ≥576px |
| Medium | md | ≥768px |
| Large | lg | ≥992px |
| Extra large | xl | ≥1200px |
| Extra extra large | xxl |  ≥1400px |

Bootstrap - Utilities - Display  

Hidden on all  
`d-none`

Hidden only on sm - for tablet and desktop side navigation bar  
`d-none d-sm-inline`

Visible only on xs - for mobile top navigation bar  
`d-block d-sm-none`

Visible only on sm - for tablet-mobile top navigation bar  
`d-none d-sm-inline d-md-none`  

Choose either `-inline` or `-block`.

## Finding python package version

```sh
pip list | grep Dj
# Django 5.1.3

pip --version
# pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

## Generating sample templates with DJango form

`polls/views.py`
```py
from django import forms

class AForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def aview(request):
    if request.method == "POST":
        form = AForm(request.POST, request.FILES)
    else:
        form = AForm()
    return render(request, "polls/aview.html", {"form": form})
```

`polls/templates/polls/aview.html`
```html
{% for field in form %}
    <div class="fieldWrapper ">
        {{ field.errors }}
        <label for='{{ field.label_tag }}' >
            {{ field.label_tag }}
        </label>
        <div class="" id='{{ field.label_tag }}'>
            {{ field }}
        </div>
    </div>
{% endfor %}
```

## Uploading folder structure directories along with the folder

<https://diginaga.online/django/python/code/2019/04/10/directory_upload_django.html>

```html
<form method='POST' enctype="multipart/form-data">
    <input type="file" id="file_input" name="file_field" webkitdirectory directory/>
    <input type="text" id="directories" name="directories" hidden />
    <input type="submit"/>
</form>
<script>
    files = document.querySelector("#file_input").files;
    document.querySelector("#file_input").addEventListener("change", function() {
        files = document.querySelector("#file_input").files;
        var directories = {}
        for (var file of files) {
            file.webkitRelativePath
            directories[file.name] = file.webkitRelativePath
        }
        directories = JSON.stringify(directories);
        document.querySelector("#directories").value = directories
    });
</script>
```

This method however, for unknown reason, the directories are not properly being received on the server side.  

The found reason is: 

1. There were two duplicate hidden input for storing directories.
2. Second possible issue is that the location of the JavaScript was placed outside of a 'div' document container, whereas it should be placed right under the form document - under where the `</form>` ends. 

Option 5  
Uploading Zip file and save as is.  
<https://stackoverflow.com/questions/74300563/save-uploaded-inmemoryuploadedfile-as-tempfile-to-disk-in-django>  

`polls/templates/polls/upload_folder.html`
```html
<label for="id_zipfile" class="form-label">Zip File:</label>
<input type="file" accept=".zip,.rar,.7zip" name="zipfile" id="id_zipfile" class="form-control mb-1">
<input type="text" id="directories" name="directories" hidden/>
```

From backend `ku_django/polls/views.py`:
```py
from django.core.files.storage import FileSystemStorage

def simple_view(request):
    in_memory_file_obj = request.FILES["file"]
    FileSystemStorage(location="/tmp").save(in_memory_file_obj.name, in_memory_file_obj)
```

The data type is not a File or ZipFile but DJango's `TemporaryUploadedFile` with methods from `UploadedFile`, read the documentation.

## Installing Django 

```sh
sudo apt update
sudo apt install python3-django

python -m pip list | grep ja
# Django 5.1.3

sudo apt update
python3 -V
sudo apt install python3-pip python3-venv
sudo apt install python3-dev

# check pip version
python3 -m pip --version

# check current env
python
import sys
print(sys.prefix)
# /home/user/my_env
# ctrl + z to exit
# /usr

# python3.11 -m pip install django
pip install django

# A Guide from Writing your first Django app
# https://docs.djangoproject.com/en/5.1/intro/tutorial01/

python -m django --version
# 5.1.3

django-admin --version
# 5.1.3

# create a project
django-admin startproject frontend_project
cd frontend_project/

# initial migration for sessions and contenttypes
python manage.py migrate

python manage.py runserver 8001
```

## Making a Python environment

```sh
python -V
# 3.12.3
python3 -V
# 3.12.3

python -m pip --version
# pip 24.0 from /home/user/Documents/ku_django_frontend/lib/python3.12/site-packages/pip (python 3.12)
python3 -m pip --version
# same output

mkdir /home/user/Documents/ku_django_frontend/
cd /home/user/Documents/ku_django_frontend/

# make env
python3 -m venv frontend_env
# Python 3.12

# activate 
source frontend_env/bin/activate

# optional deactivate
deactivate
```

## Making a beginner sample application

```sh
# create an app
cd /home/user/Documents/ku_django_frontend/
python manage.py startapp webapp
```

## Multiple levels of DJango template extend-block

/home/user/Documents/ku_django_frntnd/static/css/website-screenshots/multiple level of html template extend-block_ Screenshot from 2024-11-07 15-27-10.png


`lvl1.html`
```html
<p> level 1 </p>

{% block level_2 %}
{% endblock %}
```

`lvl2.html`
```html
{% extends "lvl1.html" %}
<!DOCTYPE html>
...
<body>
    <div id="content" class="col m-0 ps-0 pe-0">
        {% block level_3 %}{% endblock %}
    </div>
</body>

{% block level_2 %}
{% endblock %}
```

`lvl3.html`
```html
{% extends "lvl2.html" %}

{% block level_3 %}
<div>
    ...
</div>
{% endblock %}
```

## Creating responsive stacks of full-width UIs

<https://getbootstrap.com/docs/5.3/components/buttons/#block-buttons>

Use class `d-grid px-0` to use full-width and to remove side paddings. 

Below example is a dropdown menu button, overiding its default style to unify style with other buttons.

```html
<div class="dropdown d-grid px-0">
    <button class="btn btn-light dropdown-toggle border-light-subtle shadow-sm" type="button" data-bs-toggle="dropdown" aria-expanded="false">
        Data Generation
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">action A</a></li>
        <li><a class="dropdown-item" href="#">action B</a></li>
        <li><a class="dropdown-item" href="#">action C</a></li>
    </ul>
</div>
```

## Setting Session Cookie Age

`frontend_project/settings.py`
```py
SESSION_COOKIE_AGE = 1209600
```

`1209600` - 2 weeks in seconds - 60s * 60m * 24h * 7d * 2w - Django Default.  
`172800` - 2 days in seconds - 60s * 60m * 24h * 2d.  

## Optional - Making a beginner sample model data

Database will not be used for web server, this is necessary only in API server.  
SQLite3 may be used for temporary data and less sensitive data.  

```sh
# Writing your first Django app, part 2
# https://docs.djangoproject.com/en/5.1/intro/tutorial02/

# API - Interactive python shell
python3 manage.py shell

from webapp.models import Choice, Question  # Import the model classes we just wrote.

Question.objects.all()
# <QuerySet []>  # No questions are in the system yet.

# Create a new Question.
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
q.save()

q.id
# 1
q.question_text
# "What's new?"
q.pub_date
# datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

# Change values by changing the attributes, then calling save().
q.question_text = "What's up?"
# q.save() # database is in the backend - send this object to backend and save there.

Question.objects.all()
# <QuerySet [<Question: Question object (1)>]> 

# ctrl + z  to exit
```

## Deleting an environment

```sh
# myenv is in the current directory of the terminal 
rm -r myenv
```

## Rendering HTML string as view

If you don't want the HTML to be escaped, look at the safe filter and the autoescape tag:

```python
def bstr(byte_string, encoding=UTF8):
    return byte_string.decode(encoding)    

def get_request(request):
    template_name = 'webapp/empty.html'
    url = "http://127.0.0.1:8000/backend/"

    response = requests.get(url)

    context = { 'htmlstring': bstr(response.content)}
    return render(request, template_name, context)
```

`webapp/empty.html`  

```html
{{ myhtml |safe }}
```

or  

```html
{% autoescape off %}
    {{ myhtml }}
{% endautoescape %}
```

<https://stackoverflow.com/questions/4848611/rendering-a-template-variable-as-html>

## Choosing python version for debugging

VS Code  

`ctrl + shift + p`  
`>Python: Select Interpreter`  
Choose `Python 3.11.10 64-bit usr/bin/python`  
Or Choose the python version that have been used for the project development.

Download extension:  
Python Debugger  
v2024.12.0  
Microsoft  

`ctrl + shift + p`  
Choose `Debug: Select and Start Debugging`  
Choose `Python Debugger: DJango`  

Add breakpoints to where you want to view variable content, instead of using print() function.  

## Finding history of commands

```sh
ctrl + r

# search for your past command 
cd 
# (reverse-i-search)`cd': cd ~/Documents/ku_django/

# enter if the result command is what you are looking for
```
## Initialising a Github repository

git config

Install Git
```sh
sudo apt update
sudo apt upgrade
sudo apt install git
```

Initial user setup and make gitignore file 
```sh
touch .gitignore
# https://www.toptal.com/developers/gitignore
# Search: Django Python
# Copy content and paste to gitignore file 

git rm --cached FILENAME

git config --global user.email a@example.com
git config --global user.username ace

touch ~/.gitignore
code ~/.gitignore
# Copy-paste the gitignore content and save 
git config --global core.excludesFile ~/.gitignore
```

Initialise a Github Repository
```sh
git init
git add .
```

Commit the repository
```sh
# 1st option
git commit
# write commit message
ctrl+o
ctrl+x

# 2nd option
git commit -m 'your commit message'
```

## Installing Github Desktop on Linux

```sh
wget -qO - https://apt.packages.shiftkey.dev/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/shiftkey-packages.gpg > /dev/null
sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/shiftkey-packages.gpg] https://apt.packages.shiftkey.dev/ubuntu/ any main" > /etc/apt/sources.list.d/shiftkey-packages.list'

sudo apt update && sudo apt install github-desktop

github
```

## Excluding gitignore files 

```sh
git rm -rf --cached .
git add .

git commit
# follow above guide "Commit the repository"
# or use github desktop
```

