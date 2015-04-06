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
    * specify name ('Copyright'), type ('Text') and click "Save and continue editing"
    * set up a value

6. Now you can access to the new param from the code as:
    ```
    from django.conf import settings
    from django_params import Param
    
    <...>
    copyright_text = Param.get(request, settings.PARAMS_COPYRIGHT)
    # or:
    copyright_text = Param.get_one(settings.PARAMS_COPYRIGHT)
    <...>
    ```

Note: on the first call out through the `Param.get`, all params from DB will be
cached into request. So, on second call `Param.get` will just find cached param.
Or you can use Param.get_one to select from DB one param by single query.
