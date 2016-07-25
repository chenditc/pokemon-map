from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^fort$', views.fort, name='fort'),
            url(r'^pokemon$', views.pokemon, name='pokemon'),
            ]
