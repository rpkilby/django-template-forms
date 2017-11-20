# from django.shortcuts import render

from django import forms
from django.views import generic

from template_forms import bs3, bs4


def not_startswith_a(value):
    if value.startswith('a'):
        raise forms.ValidationError('Value must not start with "a".')


# forms ########################################################
class Mixin(forms.Form):
    username = forms.CharField(min_length=8, max_length=10, validators=[not_startswith_a], help_text='Please enter your username')
    account_type = forms.ChoiceField(help_text='Chose your pricing plan', choices=(
        ('corp', 'Corporate'),
        ('strt', 'Start-up'),
        ('comm', 'Commmunity'),
    ))

    def clean(self):
        super().clean()
        raise forms.ValidationError('This is a non-field error')


class BS3BlockForm(Mixin, bs3.BlockForm):
    pass


class BS4BlockForm(Mixin, bs4.BlockForm):
    pass


# views ########################################################
class HomeView(generic.TemplateView):
    template_name = 'home.html'


class BaseFormView(generic.FormView):
    title = 'Form Example'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class BS3BlockFormView(BaseFormView):
    template_name = 'bs3.html'
    form_class = BS3BlockForm
    title = 'BS3 Block Form'


class BS4BlockFormView(BaseFormView):
    template_name = 'bs4.html'
    form_class = BS4BlockForm
    title = 'BS4 Block Form'
