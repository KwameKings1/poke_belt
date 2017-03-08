from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.create_user),
    url(r'^login$', views.login_user),
    url(r'^pokes$', views.main_page),
    url(r'^logout$', views.logout_user),
    url(r'^poke_person/(?P<id>\d+)$', views.poke_person),
]
