=====
Spotlights
=====

===
DANGER
===
**Work-in-progress! Not ready for production use yet!**

A Django slideshow app.

Quick start
-----------

1. Add "spotlights" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'spotlights',
    ]

2. Include the spotlights URLconf in your project urls.py like this::

    url(r'^spotlights/', include('spotlights.urls')),

3. Run `python manage.py migrate` to create the spotlights models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create some spotlights (you'll need the Admin app enabled).
