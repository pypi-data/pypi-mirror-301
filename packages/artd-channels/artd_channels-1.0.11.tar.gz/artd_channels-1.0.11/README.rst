ArtD Channels
==============
Art Channels is a package that manage channels.
----------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        'artd_customer',
        'artd_location',
        'artd_modules',
        'artd_partner',
        'artd_service',
        'django_json_widget',
    ]

2. Run the migration commands:
   
.. code-block::
    
        python manage.py makemigrations
        python manage.py migrate

3. Run the seeder data:
   
.. code-block::

        python manage.py create_countries
        python manage.py create_colombian_regions
        python manage.py create_colombian_cities


