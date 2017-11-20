from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bs3-block', views.BS3BlockFormView.as_view(), name='bs3-block'),
    path('bs4-block', views.BS4BlockFormView.as_view(), name='bs4-block'),
]
