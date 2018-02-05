from django import forms
from django.forms import widgets
from django.test import TestCase

from template_forms import TemplateForm


class GetFieldTemplateNameTests(TestCase):
    class NotSet(TemplateForm, forms.Form):
        pass

    class Form(TemplateForm, forms.Form):
        field_template_map = {
            widgets.Input: 'default.html',
            widgets.Select: 'select.html',
        }

        string = forms.CharField()
        choice = forms.ChoiceField(choices=[('a', 'a')])

    def test_class_template(self):
        form = self.Form()
        field = form['choice']

        template_name = form.get_field_template_name(field)

        self.assertEqual(template_name, 'select.html')

    def test_parent_template(self):
        form = self.Form()
        field = form['string']

        template_name = form.get_field_template_name(field)

        self.assertEqual(template_name, 'default.html')

    def test_not_set(self):
        form = self.NotSet()
        msg = '`NotSet.field_template_map` should be a mapping of widgets to template names.'
        with self.assertRaisesMessage(AssertionError, msg):
            form.get_field_template_name(None)


class GetFieldCSSClassesTests(TestCase):
    def test_error_css_class(self):
        """
        This result is "incorrect", but operates in accordance to the behavior
        of `BoundField`, which will error when the attribute is a `NoneType`.
        """
        class Form(TemplateForm, forms.Form):
            field = forms.CharField()
            error_css_class = None

        form = Form()
        bf = form['field']

        self.assertEqual([None], form.get_field_css_classes(bf, 'error'))
