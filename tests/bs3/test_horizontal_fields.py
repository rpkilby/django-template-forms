
from django import forms
from django.test import TestCase

from template_forms import bs3


def startswith_a(value):
    if value.startswith('a'):
        return value
    raise forms.ValidationError('Value must start with "a".')


def not_now(value):
    if value:
        raise forms.ValidationError('I cannot let you do that right now.')


class StandardFieldTests(TestCase):
    class Form(bs3.HorizontalForm, forms.Form):
        field = forms.CharField(required=False, validators=[startswith_a], help_text='Example text.', )

    def get_attrs(self, bf):
        return {
            'name': bf.html_name,
            'id': bf.auto_id,
            'label': bf.label,
            'left': 'col-md-3 col-sm-5',
            'right': 'col-md-9 col-sm-7',
        }

    def test_field(self):
        form = self.Form()
        field = form['field']
        template = """
        <div class="form-group">
            <label for="{id}" class="control-label {left}">{label}:</label>
            <div class="{right}">
                <input id="{id}" name="{name}" type="text" class="form-control">
                <small class="help-block">Example text.</small>
            </div>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )

    def test_field_bound(self):
        form = self.Form({'field': 'a value'})
        field = form['field']
        template = """
        <div class="form-group">
            <label for="{id}" class="control-label {left}">{label}:</label>
            <div class="{right}">
                <input id="{id}" name="{name}" type="text" class="form-control" value="a value">
                <small class="help-block">Example text.</small>
            </div>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )

    def test_field_error(self):
        form = self.Form({'field': 'error'})
        field = form['field']
        template = """
        <div class="form-group has-error">
            <label for="{id}" class="control-label {left}">{label}:</label>

            <div class="{right}">
                <input id="{id}" name="{name}" type="text" class="form-control has-error" value="error">
                <small class="help-block">Value must start with &quot;a&quot;.</small>
                <small class="help-block">Example text.</small>
            </div>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )


class CheckboxFieldTests(TestCase):
    class Form(bs3.HorizontalForm, forms.Form):
        field = forms.BooleanField(required=False, validators=[not_now], help_text='Example text.')

    def get_attrs(self, bf):
        return {
            'name': bf.html_name,
            'id': bf.auto_id,
            'label': bf.label,
            'left': 'col-md-offset-3 col-sm-offset-5',
            'right': 'col-md-9 col-sm-7',
        }

    def test_field(self):
        form = self.Form()
        field = form['field']
        template = """
        <div class="form-group">
            <div class="{left} {right}">
                <div class="checkbox">
                    <label>
                        <input id="{id}" name="{name}" type="checkbox"> {label}
                    </label>
                </div>
                <small class="help-block">Example text.</small>
            </div>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )

    def test_field_error(self):
        form = self.Form({'field': 'on'})
        field = form['field']
        template = """
        <div class="form-group has-error">
            <div class="{left} {right}">
                <div class="checkbox">
                    <label>
                        <input id="{id}" name="{name}" type="checkbox" checked> {label}
                    </label>
                </div>
                <small class="help-block">I cannot let you do that right now.</small>
                <small class="help-block">Example text.</small>
            </div>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )
