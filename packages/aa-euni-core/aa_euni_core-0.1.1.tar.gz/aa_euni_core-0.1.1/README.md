# Alliance Auth EVE University Core

EVE University Core Services for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)


![License](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.8-informational)
![django](https://img.shields.io/badge/django-4.0-informational)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

## Features

- EVE University template/theme adapted from Bootswatch Slate v3.4.1
- Extends Alliance Auth's authenticate backend to fake email registration
- Extends Django Template Engine to allow this app to override any templates

## Future Plans
- Add support for more core EVE Uni services such as Wiki, Mumble, etc.

## How to Use It

This application can be installed via EVE Uni's PyPi repo, built and installed, or installed from the sour ce.

It is designed solely to provide the Alliance Auth/Django overrides, extensions, or services needed by EVE University.

**Example production installation**
```bash
pip install aa-euni-core

python myauth/manage.py collectstatic
```

Add these lines somewhere in your local.py:

### Cloning From Repo

When cloning from the repo we will assume you are using a dev environment (e.g. aa-dev) and you will be installing this
app under one top folder.

Something like this:
```text
aa-dev
|- venv/
|- myauth/
|- aa-euni-core
|- (other AA projects ...)
```

Then just cd into the top folder (e.g. aa-dev) and clone the repo.
Finally, enable [pre-commit](https://pre-commit.com) to enable automatic code style
checking.

```bash
git clone https://github.com/EVE-University/aa-euni-core.git
cd aa-euni-core
pre-commit install
```

## Writing Unit Tests

Write your unit tests in `aa-eveuni-core/eunicore/tests/` and make sure that you use a "test\_"
prefix for files with your unit tests.

## Installing Into Your Dev AA

Once you have cloned or copied all files into place you are ready to install it to your dev AA instance.

Make sure you are in your venv. Then install it with pip in editable mode:

```bash
pip install -e aa-euni-core
```

First add the following to your Django project's `local.py`:
```python
INSTALLED_APPS += ["eunicore"]

AUTHENTICATION_BACKENDS = [
    "eunicore.auth.backends.EUniBackend",
    "django.contrib.auth.backends.ModelBackend",
]

TEMPLATES[0]["BACKEND"] = "eunicore.template.backends.EUniDjangoTemplates"
```


Next collect statics:

```bash
python manage.py collectstatic
```

Then run a check to see if everything is set up correctly.

```bash
python manage.py check
```


In case they are errors make sure to fix them before proceeding.

Finally, restart your AA server and that's it.

## Installing Into Production AA

To install your plugin into a production AA run this command within the virtual
Python environment of your AA installation:

```bash
pip install git+https://github.com/EVE-University/aa-euni-core.git
```
Note you may need a personal access token

Alternatively you can create a package file from the repo and manually upload it to your
production AA:

```bash
make build
```

You'll find the package under `./dist/aa_euni_core.tar.gz` after this.

Install your package directly from the package file:

```bash
pip install aa_euni_core.tar.gz
```

Add the following to your production's `local.py`:
```python
INSTALLED_APPS += ["eunicore"]

AUTHENTICATION_BACKENDS = [
    "eunicore.auth.backends.EUniBackend",
    "django.contrib.auth.backends.ModelBackend",
]

TEMPLATES[0]["BACKEND"] = "eunicore.template.backends.EUniDjangoTemplates"
```

## Components
This app breaks up most of its functionality into descrete components.
### Auth Backend
Extends `allianceauth.authentication.backends.StateBackend` create_user() method which is called
by authenticate() when a user isn't registered. The overriden create_user() method activates the
created user account and defines a `[user_id]@eveuniversity.org` as the email.

### Template Backend
Extends `django.template.backends.django.DjangoTemplates` to add the `eunicore/templates` to the
template loader's dirs if it isn't already present.

### Templates
The `eunicore/templates` directory can be used to override any template file used by the
Alliance Auth application.

### AA v4.x Theme

Add `eunicore.theme.slate` to INSTALLED_APPS.

Add the following to `local.py` as well if you only the Slate theme available.

```python
# Sets default theme to Slate.
DEFAULT_THEME = "eunicore.theme.slate.auth_hooks.SlateThemeHook"

# Legacy AAv3 user.profile.night_mode=1. This is the default set by the EUni Auth Backend.
DEFAULT_THEME_DARK = "eunicore.theme.slate.auth_hooks.SlateThemeHook"

# Remove the default BS5 themes
INSTALLED_APPS.remove("allianceauth.theme.darkly")
INSTALLED_APPS.remove("allianceauth.theme.flatly")
INSTALLED_APPS.remove("allianceauth.theme.materia")
```
