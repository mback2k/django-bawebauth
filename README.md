BaWebAuth
=========

Dependencies
------------
- Django             [https://www.djangoproject.com/]
- django_compressor  [https://github.com/jezdez/django_compressor]

Submodules
----------
- django-jdatetime   [https://github.com/mback2k/django-jdatetime]
- django-yamlcss     [https://github.com/mback2k/django-yamlcss]

Configuration
-------------
In order to use BaWebAuth the Django project needs to have a complete settings.py.
The following Django settings are required to run BaWebAuth:

- DATABASES
- DEFAULT_FROM_EMAIL
- SECRET_KEY

All other settings are pre-configured inside settings/base.py, which can be imported using the following line in your settings/{env}.py:

    from .base import *

A basic development environment can be launched using the pre-configured settings/dev.py.

Installation
------------
First of all you need to install all the dependencies.
It is recommended to perform the installations using the pip command.

The next step is to get all source from github.com and PyPI:

    git clone --recursive git://github.com/mback2k/django-bawebauth.git bawebauth
    
    cd bawebauth
    
    pip install -r requirements.txt

After that you need to collect and compress the static files using:

    python manage.py collectstatic --noinput
    python manage.py compress --force

Now you need to setup your webserver to serve the Django project.
Please take a look at the [Django documentation](https://docs.djangoproject.com/en/1.5/topics/install/) for more information.

You can run a development server using the following command:

    python manage.py runserver

License
-------
* Released under MIT License
* Copyright (c) 2012-2016 Marc Hoersken <info@marc-hoersken.de>
