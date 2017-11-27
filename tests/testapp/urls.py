from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.HomeView.as_view(), name='home'),
    url(r'^bs3-block', views.BS3BlockFormView.as_view(), name='bs3-block'),
    url(r'^bs4-block', views.BS4BlockFormView.as_view(), name='bs4-block'),
]
