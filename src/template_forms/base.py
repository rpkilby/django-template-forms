from collections import OrderedDict

from django.forms.forms import BaseForm
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


def add_css_classes(boundfield, css_classes):
    """
    Add a single or multiple css classes to a form widget. To add multiple classes, pass
    them as a whitespace delimited string or a list. eg, `add_classes(boundfield, 'foo bar')`
    """
    if not css_classes:
        return

    if isinstance(css_classes, str):
        css_classes = css_classes.split()

    widget = boundfield.field.widget
    classes = OrderedDict.fromkeys(widget.attrs.get('class', '').split())
    classes.update(OrderedDict.fromkeys(css_classes))

    widget.attrs['class'] = " ".join(classes)


class TemplateForm(BaseForm):
    """
    Generic mixin that implements the template rendering logic for the fields and the form.

    This mixin should precede `forms.Form` or `forms.ModelForm` to ensure that the correct
    rendering function is called by default.
    """
    form_template_name = None
    field_template_name = None

    outer_css_class = None
    label_css_class = None
    field_css_class = None

    error_css_class = None

    def format_hidden_error(self, name, error):
        return _('(Hidden field %(name)s) %(error)s') % {
            'name': name,
            'error': force_text(error)
        }

    def get_form_template_name(self):
        return self.form_template_name

    def get_field_template_name(self, boundfield):
        return self.field_template_name

    def get_form_context(self):
        # Errors that should be displayed above all fields.
        top_errors = self.non_field_errors()
        output, hidden_output = [], []

        for name, field in self.fields.items():
            bf = self[name]

            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])

            if not bf.is_hidden:
                output.append(self.render_field(bf, bf_errors))
            else:
                hidden_output.append(str(bf))
                top_errors += [self.format_hidden_error(name, e) for e in bf_errors]

        return {
            'top_errors': top_errors,
            'hidden_output': hidden_output,
            'output': output,
            'form': self,
        }

    def get_field_context(self, bf, errors):
        # add the field_css_class to the widget attrs
        field_css_classes = self.get_field_css_classes(bf, errors)
        if field_css_classes:
            add_css_classes(bf, ' '.join(field_css_classes))

        # build the set of css classes for the outer html
        # element that wraps the inner label/field.
        outer_classes = bf.css_classes(self.outer_css_class)

        # don't render label tag if label=''
        label = bf.label_tag(
            conditional_escape(force_text(bf.label)),
            attrs={'class': self.label_css_class},
        ) if bf.label else ''

        return {
            'outer_classes': outer_classes,
            'label': force_text(label),
            'field': str(bf),
            'help_text': force_text(bf.help_text),
            'errors': errors,
            'bf': bf,
        }

    def get_field_css_classes(self, bf, errors):
        classes = []
        if self.field_css_class:
            classes.append(self.field_css_class)
        if errors and self.error_css_class:
            classes.append(self.error_css_class)
        return classes

    def render_field(self, bf, errors):
        template_name = self.get_field_template_name(bf)
        context = self.get_field_context(bf, errors)

        return mark_safe(self.renderer.render(template_name, context))

    def render(self):
        template_name = self.get_form_template_name()
        context = self.get_form_context()

        return mark_safe(self.renderer.render(template_name, context))

    def __str__(self):
        return self.render()
