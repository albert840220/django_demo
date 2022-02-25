# Django 網站Demo

此網站主要是機台基本資料紀錄與管理、維修團隊派工與完工回報、業務行程與客戶意見等的管理，提升保修效率、提升售後服務品質與設備妥善率，當然也是設備銷售的競爭價值最重要的部分。

<br />

> Features

- UI 套件: [Volt Bootstrap 5](https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard) by **Themesberg**
- Session-Based Authentication
- 在AWS EC2 Ubuntu使用Gunicorn+Nginx+SSL部署

<br />

> Links

- [Demo](https://www.eatee.co) - LIVE deployment

<br />

![Django Bootstrap 5 Volt - Template project provided by AppSeed.](https://raw.githubusercontent.com/albert840220/django-demo/master/media/django_demo.gif)

<br />

## 如何使用

```bash
$ # Get the code
$ git clone https://github.com/albert840220/django_demo.git
$ cd django-demo
$
$ # Virtualenv modules installation
$ virtualenv env
$ .\env\Scripts\activate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

<br />

## Project structure

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app logic and serve the static assets
   |    |-- settings.py                    # Django app bootstrapper
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |-- templates/                     # Templates used to render pages
   |         |
   |         |-- includes/                 # HTML chunks and components
   |         |-- layouts/                  # Master pages
   |         |-- accounts/                 # Authentication pages
   |         |
   |      index.html                       # The default page
   |       *.html                          # All other HTML pages
   |
   |-- authentication/                     # Handles auth routes (login and register)
   |    |-- urls.py                        # Define authentication routes  
   |    |-- forms.py                       # Define auth forms  
   |
   |-- app/                                # A simple app that serve HTML files
   |    |-- views.py                       # Serve HTML pages for authenticated users
   |    |-- urls.py                        # Define some super simple routes  
   |
   |-- electrodes/                         # Handles the profile edit     <-------- NEW
   |    |-- __init__.py                    # Defines App init             <-------- NEW
   |    |-- admin.py                       # Defines App admin            <-------- NEW
   |    |-- apps.py                        # Defines App apps             <-------- NEW
   |    |-- forms.py                       # Defines App forms            <-------- NEW
   |    |-- models.py                      # Defines App models           <-------- NEW
   |    |-- signals.py                     # Defines App signals          <-------- NEW
   |    |-- tests.py                       # Defines App tests            <-------- NEW
   |    |-- urls.py                        # Defines App routes           <-------- NEW
   |    |-- views.py                       # Defines App views            <-------- NEW
   |
   |-- requirements.txt                    # Development modules
   |-- manage.py                           # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />