# django-template-forms

[![Build Status](https://travis-ci.org/rpkilby/django-template-forms.svg?branch=master)](https://travis-ci.org/rpkilby/django-template-forms)
[![Codecov](https://codecov.io/gh/rpkilby/django-template-forms/branch/master/graph/badge.svg)](https://codecov.io/gh/rpkilby/django-template-forms)
[![Version](https://img.shields.io/pypi/v/django-template-forms.svg)](https://pypi.python.org/pypi/django-template-forms)
[![License](https://img.shields.io/pypi/l/django-template-forms.svg)](https://pypi.python.org/pypi/django-template-forms)

Template based form rendering for Django

----

## Overview

Django 1.11 recently introduced template-based widget rendering to allow easier customization of widgets by users.
`django-template-forms` is the logical extension of this feature, implementing template-based rendering for fields
and forms.

At this point, simple block forms are supported for Bootstrap 3 & 4. Horizontal forms and check/radio field layouts
are inbound.


## Requirements

- **Python**: 3.4, 3.5, 3.6
- **Django**: 1.11, 2.0b

Install with pip:

```sh
$ pip install django-template-forms
```


## Configuration

Once installed, add `'template_forms'` to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    'template_forms',
]
```

## Usage

All `template_forms` form classes inherit from `django.forms.BaseForm` and are intended to be mixed with a concrete
`forms.Form` or `froms.ModelForm`. Example usage:

```python
from django import forms
from template_forms import bs3

from .models import Article


class ArticleForm(bs3.BlockForm, forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'published_date', ...]
```

In the *view* template:

```html
<form method="post" action="">
    {% csrf_token %}
    {{ form }}
    <button class="btn btn-primary" type="submit">Save</button>
</form>
```

**TODO:** Document creation of custom `TemplateForm` subclass.

## Overriding Templates

`django-template-forms` provides a default set of templates. To override these, you first need to consider the
[`FORM_RENDERER`][form-renderer] setting, then override the relevant template files. By default, `FORM_RENDERER`
uses the [`DjangoTemplates`][django-renderer] renderer, which loads templates from your installed apps.

If you want more control over template loading, you can use the [`TemplatesSetting`][templates-renderer] renderer,
which loads templates from using your configured `TEMPLATES` setting. If you use this renderer, you may need to add
`'django.forms'` to your `INSTALLED_APPS`. See the [renderer docs][templates-renderer] for more information.

```python
INSTALLED_APPS = [
    ...
    'django.forms',
    'template_forms',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [...],
        'APP_DIRS': True,
        ...
    },
]

```

Templates are provided for each supported CSS framework.

**Note:**
- horizontal layouts do not exist yet
- check & radio field templates do not exist yet.

**BS3:**

- `template_forms/bs3/forms/block.html`
- ~~`template_forms/bs3/forms/horizontal.html`~~
- `template_forms/bs3/fields/block.html`
- `template_forms/bs3/fields/block_checkbox.html`
- ~~`template_forms/bs3/fields/block_check_inline.html`~~
- ~~`template_forms/bs3/fields/block_check_stacked.html`~~
- ~~`template_forms/bs3/fields/block_radio_inline.html`~~
- ~~`template_forms/bs3/fields/block_radio_stacked.html`~~
- ~~`template_forms/bs3/fields/horizontal.html`~~
- ~~`template_forms/bs3/fields/horizontal_checkbox.html`~~
- ~~`template_forms/bs3/fields/horizontal_check_inline.html`~~
- ~~`template_forms/bs3/fields/horizontal_check_stacked.html`~~
- ~~`template_forms/bs3/fields/horizontal_radio_inline.html`~~
- ~~`template_forms/bs3/fields/horizontal_radio_stacked.html`~~

**BS4:**

- `template_forms/bs4/forms/block.html`
- ~~`template_forms/bs4/forms/horizontal.html`~~
- `template_forms/bs4/fields/block.html`
- ~~`template_forms/bs4/fields/block_checkbox.html`~~
- ~~`template_forms/bs4/fields/block_check_inline.html`~~
- ~~`template_forms/bs4/fields/block_check_stacked.html`~~
- ~~`template_forms/bs4/fields/horizontal.html`~~
- ~~`template_forms/bs4/fields/horizontal_checkbox.html`~~
- ~~`template_forms/bs4/fields/horizontal_check_inline.html`~~
- ~~`template_forms/bs4/fields/horizontal_check_stacked.html`~~


## Running the tests

The test suite requires `tox` and `tox-venv`. The full list of builds is viewable with `tox -l`.

```sh
$ pip install tox tox-venv
$ tox -e py36-django111
$ tox -e lint,isort
```


## Release Process

- Update package version in setup.py
- Create git tag for version
- Upload release to PyPI
    ```sh
    $ pip install -U setuptools wheel pypandoc
    $ rm -rf dist/ build/
    $ python setup.py bdist_wheel upload
    ```


## Copyright & License
Copyright &copy; 2017 Ryan P Kilby. See LICENSE for details.

[form-renderer]: https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-FORM_RENDERER
[django-renderer]: https://docs.djangoproject.com/en/1.11/ref/forms/renderers/#djangotemplates
[templates-renderer]: https://docs.djangoproject.com/en/1.11/ref/forms/renderers/#templatessetting
