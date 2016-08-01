from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^fort$', views.fort, name='fort'),
            url(r'^pokestop$', views.pokestop, name='pokestop'),
            url(r'^gym$', views.gym, name='gym'),
            url(r'^pokemon$', views.pokemon, name='pokemon'),
            ]
