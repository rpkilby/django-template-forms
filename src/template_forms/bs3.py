from django.forms import widgets

from .base import TemplateForm
from .utils import bs3_cols, bs3_inverse_cols


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


class HorizontalForm(TemplateForm):
    form_template_name = 'template_forms/bs3/forms/horizontal.html'
    field_template_map = {
        widgets.Widget:         'template_forms/bs3/fields/horizontal.html',  # default
        widgets.CheckboxInput:  'template_forms/bs3/fields/horizontal_checkbox.html',
    }

    cols = [('md', '9'), ('sm', '7')]

    outer_css_class = 'form-group'
    label_css_class = 'control-label'
    field_css_class = 'form-control'

    error_css_class = 'has-error'

    def get_form_context(self):
        context = super().get_form_context()
        context.update({
            'left': bs3_inverse_cols(self.cols),
            'right': bs3_cols(self.cols),
        })
        return context

    def get_field_context(self, bf, errors):
        context = super().get_field_context(bf, errors)

        # checkboxes and radio buttons use offset, as they don't have a left-content
        offset = isinstance(bf.field.widget, (
            widgets.CheckboxInput,
            widgets.CheckboxSelectMultiple,
            widgets.RadioSelect,
        ))

        context.update({
            'left': bs3_inverse_cols(self.cols, offset=offset),
            'right': bs3_cols(self.cols)
        })

        return context

    def get_field_css_classes(self, bf, errors):
        classes = super().get_field_css_classes(bf, errors)

        # checkboxes and radio buttons don't apply the field classes
        if isinstance(bf.field.widget, (widgets.CheckboxInput,
                                        widgets.CheckboxSelectMultiple,
                                        widgets.RadioSelect, )):
            return []
        return classes

    def get_label_css_classes(self, bf, errors):
        classes = super().get_label_css_classes(bf, errors)
        classes += bs3_inverse_cols(self.cols).split(' ')
        return classes
