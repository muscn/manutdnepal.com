from django.conf.urls import patterns, url
from . import views



urlpatterns = patterns('',
                       url(r'^$', views.EventsList.as_view(), name='list_events'),
                       # url(r'^payment/$', views.PaymentListView.as_view(), name='list_payments'),
                       # # url(r'^payment/add/$', payment_views.PaymentCreateView.as_view(), name='create_payment'),
                       # url(r'^payment/(?P<pk>\d+)/$', payment_views.PaymentUpdateView.as_view(), name='update_payment'),
                       # url(r'^payment/(?P<pk>\d+)/delete/$', payment_views.PaymentDeleteView.as_view(),
                       #     name='delete_payment'),

)
