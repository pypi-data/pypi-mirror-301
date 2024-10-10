huscy.attributes
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-attributes.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-attributes.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-attributes)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-attributes)
![PyPI License](https://img.shields.io/pypi/l/huscy-attributes?color=yellow)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-attributes)



Huscy is a free open-source software solution for managing study participants in the context of human sciences.
The software is deliberately implemented in a generic manner to appeal to a wide user base, while considering all relevant aspects of data protection.
The strictly modular software architecture allows for easy integration of new requirements, enabling the software to be customized to individual needs at any time.



Requirements
------

- Python 3.8+
- A supported version of Django

In this project the Django versions 4.2, 5.0 and 5.1 are tested with tox.



Installation
------

To install `husy.attributes` simply run:

    pip install huscy.subjects

Add required apps to `INSTALLED_APPS` in your `settings.py`:

```python
INSTALLED_APPS = (
	...

    'guardian',
    'rest_framework',
    'reversion',

    'huscy.attributes.apps.HuscyApp',
    'huscy.pseudonyms.apps.HuscyApp',
    'huscy.subjects.apps.HuscyApp',
)
```

Additional apps may need to be added (e.g., django_countries and phonenumber_field) if you want to fully utilize the huscy.subjects app.

Hook the urls from this app into your global `urls.py`:

```python
urlpatterns = [
	...
	path('', include('huscy.attributes.urls')),
]
```

Create database tables by running:

    python manage.py migrate



Development
------

Install PostgreSQL and create a database user called `huscy` and a database called `huscy`.

    sudo -u postgres createdb huscy
    sudo -u postgres createuser -d huscy
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE huscy TO huscy;"
    sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123';"

Check out the repository and start your virtual environment (if necessary).

Install dependencies:

    make install

Create database tables:

    make migrate

Run tests to see if everything works fine:

    make test
