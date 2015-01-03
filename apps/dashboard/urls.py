from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='dashboard_index'),
                       url(r'^payment/$', 'apps.payment.views.list_payments', name='list_payments'),
)
