from django import forms
from django.forms import widgets
from django.test import TestCase
from django.utils.translation import gettext as _

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


class RenderingTests(TestCase):
    def test_top_errors(self):
        class Form(TemplateForm, forms.Form):
            form_template_name = 'tests/base_form.html'
            field_template_map = {widgets.Widget: 'tests/base_field.html'}

            def clean(self):
                super().clean()
                raise forms.ValidationError([
                    forms.ValidationError('Error 1', code='error1'),
                    forms.ValidationError('Error 2', code='error2'),
                ])

        self.assertHTMLEqual("""
            <div class="errors">
                The following errors have occurred:
                <ul class="errorlist nonfield">
                    <li>Error 1</li>
                    <li>Error 2</li>
                </ul>
            </div>
        """, str(Form({})))

    def test_field_help_text_html(self):
        """
        Field.help_text should be considered safe. This is the default form behavior, and
        is necessary for proper rendering of password validation help text.
        """
        class Form(TemplateForm, forms.Form):
            form_template_name = 'tests/base_form.html'
            field_template_map = {widgets.Widget: 'tests/base_field.html'}

            field = forms.CharField(help_text='<span>help text</span>')

        self.assertHTMLEqual("""
            <div class="">
                <label class="" for="id_field">Field:</label>
                <input type="text" name="field" id="id_field" required>

                <p class="helptext">
                    <span>help text</span>
                </p>
            </div>
        """, str(Form()))

    def test_field_help_text_gettext(self):
        class Form(TemplateForm, forms.Form):
            form_template_name = 'tests/base_form.html'
            field_template_map = {widgets.Widget: 'tests/base_field.html'}

            field = forms.CharField(help_text=_('help text'))

        self.assertHTMLEqual("""
            <div class="">
                <label class="" for="id_field">Field:</label>
                <input type="text" name="field" id="id_field" required>

                <p class="helptext">
                    help text
                </p>
            </div>
        """, str(Form()))
