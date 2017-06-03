from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.contact_us, name='contact-us'),
]
