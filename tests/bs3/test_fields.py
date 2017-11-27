
from django import forms
from django.test import TestCase

from template_forms import bs3


def startswith_a(value):
    if value.startswith('a'):
        return value
    raise forms.ValidationError('Value must start with "a".')


class BlockFieldTests(TestCase):
    class Form(bs3.BlockForm):
        field = forms.CharField(required=False, validators=[startswith_a], help_text='Example text.', )

    def get_attrs(self, bf):
        return {
            'name': bf.html_name,
            'id': bf.auto_id,
            'label': bf.label,
        }

    def test_field(self):
        form = self.Form()
        field = form['field']
        template = """
        <div class="form-group">
            <label for="{id}" class="control-label">{label}:</label>
            <input id="{id}" name="{name}" type="text" class="form-control">
            <small class="help-block">Example text.</small>
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
            <label for="{id}" class="control-label">{label}:</label>
            <input id="{id}" name="{name}" type="text" class="form-control" value="a value">
            <small class="help-block">Example text.</small>
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
            <label for="{id}" class="control-label">{label}:</label>
            <input id="{id}" name="{name}" type="text" class="form-control has-error" value="error">
            <small class="help-block">Value must start with &quot;a&quot;.</small>
            <small class="help-block">Example text.</small>
        </div>
        """

        self.assertHTMLEqual(
            template.format(**self.get_attrs(field)),
            form.render_field(field, field.errors)
        )
