from django.conf.urls import patterns, url
from . import views
from apps.payment import views as payment_views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='dashboard_index'),

                       # TODO Move to payment app
                       url(r'^payment/$', payment_views.PaymentListView.as_view(), name='list_payments'),
                       url(r'^payment/add/$', payment_views.PaymentCreateView.as_view(), name='create_payment'),
                       url(r'^payment/(?P<pk>\d+)/$', payment_views.PaymentUpdateView.as_view(), name='update_payment'),
                       url(r'^payment/(?P<pk>\d+)/delete/$', payment_views.PaymentDeleteView.as_view(),
                           name='delete_payment'),

                       url(r'^bank-account/$', payment_views.BankAccountListView.as_view(), name='list_bank_accounts'),
                       url(r'^bank-account/(?P<pk>\d+)/$', payment_views.BankAccountUpdateView.as_view(),
                           name='update_bank_account'),
                       url(r'^bank-account/(?P<pk>\d+)/delete/$', payment_views.BankAccountDeleteView.as_view(),
                           name='delete_bank_account'),
                       url(r'^bank-account/add/$', payment_views.BankAccountCreateView.as_view(),
                           name='create_bank_account'),

                       url(r'^bank-deposit/$', payment_views.BankDepositListView.as_view(), name='list_bank_deposits'),
)
