
from .base import TemplateForm


class BlockForm(TemplateForm):
    form_template_name = 'template_forms/bs3/forms/block.html'
    field_template_name = 'template_forms/bs3/fields/block.html'

    outer_css_class = 'form-group'
    label_css_class = 'control-label'
    field_css_class = 'form-control'

    error_css_class = 'has-error'
