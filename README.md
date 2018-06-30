# django-onetimesecret

A safer way to share sensitive information (secret messages, passwords, private links, etc.)
with others. The secret you want to share with somebody is encrypted and can
only be viewed once. It will be burnt once it has been read. You may consider it
like a self-destructing message.


## Requirements

This is an add-on for Django and requires Django >= 2.0 and Python >= 3.6.


## Installation

You can install this add-on by running `pip install django-onetimesecret` and adding it to 
the list of installed apps:

    INSTALLED_APPS = [
        "onetimesecret.apps.OneTimeSecretConfig",
        "bootstrap4",
        ...
    ]
    
If you overwrite all the templates and don't want to use Bootstrap 4 you don't need 
add `bootstrap4` to `settings.INSTALLED_APPS`.

Finally add the urls to your `urls.py`:

    urlpatterns = [
        path("wherever/", include("onetimesecret.urls"))
        ...
    ]
    
Finally you need to apply the database migrations.
    
    
## Motivation

There are a couple of other apps doing about the same e.g. https://onetimesecret.com. I wanted to 
host my own secret sharing app but https://onetimesecret.com is built with Ruby On Rails whilst 
I feel much comfortable with Python and Django.

Furthermore I wanted to integrate lots of the new tools in the Python ecosystem:

- Dependency management with `pipenv`
- Code formatting with `black`
- Code testing with `webtest`
- Code coverage with `coveralls`
- Package versioning following `CalVer`
- Python packaging with `flit` and `bumpversion`
- Continuous integration with `Travis CI`


## Development

Format your code with the command `black .` and make sure that the command `flake8` does not complain.

### Testing

You can run the tests by simply executing `pytest`. `pytest --cov` shows the code coverage and 
`pytest --cov-report=html` generates a HTML report of the code coverage.
