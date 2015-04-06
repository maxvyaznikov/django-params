# django-params
Django package makes possible to store in DB and manage through django-admin parameters with different types

1. Install:
```
pip install git+https://github.com/maxvyaznikov/django-params.git
```
2. Add to settings
```
INSTALLED_APPS += ('django_params',)

PARAMS_COPYRIGHT = '(c)'
DJANGO_PARAMS_NAME_CHOICES = (
    (PARAMS_COPYRIGHT, u'Copyright'),
)
DJANGO_PARAMS_HAS_ADD_PERMISSION = True

```
3. Create new table
```
python manage.py syncdb
```
4. Go to /admin by Home › Django_params › Params and add new param
5. New param additional goes through 2 steps:
* specify name and type, click "Save and continue editing"
* set a value
