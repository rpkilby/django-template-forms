from django.forms import widgets

from .base import TemplateForm


class BlockForm(TemplateForm):
    form_template_name = 'template_forms/bs3/forms/block.html'
    field_template_map = {
        widgets.Widget:         'template_forms/bs3/fields/block.html',  # default
        widgets.CheckboxInput:  'template_forms/bs3/fields/block_checkbox.html',
    }

    outer_css_class = 'form-group'
    label_css_class = 'control-label'
    field_css_class = 'form-control'

    error_css_class = 'has-error'

    def get_field_css_classes(self, bf, errors):
        classes = super().get_field_css_classes(bf, errors)

        # checkboxes and radio buttons don't apply the field classes
        if isinstance(bf.field.widget, (widgets.CheckboxInput,
                                        widgets.CheckboxSelectMultiple,
                                        widgets.RadioSelect, )):
            return []
        return classes
