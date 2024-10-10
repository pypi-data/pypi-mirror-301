django-admin-honeypot-2024
==========================

**django-admin-honeypot-2024** is a fake Django admin login screen to log and notify
admins of attempted unauthorized access. This app was inspired by discussion
in and around Paul McMillan's security talk at DjangoCon 2011.

* **Author**: [xcai](https://github.com/xcai/django-admin-honeypot)
* **Version**: 1.1.0
* **License**: MIT

Documentation
=============

* Install django-admin-honeypot from PyPI:
```
        pip install django-admin-honeypot-2024
```
* Add ``admin_honeypot`` to ``INSTALLED_APPS``
* Update your urls.py:
```
        urlpatterns = [
            ...
            path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
            path('secret/', admin.site.urls),
        ]
```

* Run ``python manage.py migrate``

NOTE: replace ``secret`` in the url above with your own secret url prefix
