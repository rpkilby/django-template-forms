from django.forms import widgets

from .base import TemplateForm


class BlockForm(TemplateForm):
    form_template_name = 'template_forms/bs4/forms/block.html'
    field_template_map = {
        widgets.Widget: 'template_forms/bs4/fields/block.html',  # default
    }

    outer_css_class = 'form-group'
    label_css_class = ''
    field_css_class = 'form-control'

    error_css_class = 'is-invalid'
