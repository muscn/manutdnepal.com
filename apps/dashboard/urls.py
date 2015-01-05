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
                       url(r'^bank-deposit/add/$', payment_views.BankDepositCreateView.as_view(),
                           name='create_bank_deposit'),
                       url(r'^bank-deposit/(?P<pk>\d+)/$', payment_views.BankDepositUpdateView.as_view(),
                           name='update_bank_deposit'),
                       url(r'^bank-deposit/(?P<pk>\d+)/delete/$', payment_views.BankDepositDeleteView.as_view(),
                           name='delete_bank_deposit'),

                       url(r'^direct-payment/$', payment_views.DirectPaymentListView.as_view(),
                           name='list_direct_payments'),
                       url(r'^direct-payment/add/$', payment_views.DirectPaymentCreateView.as_view(),
                           name='create_direct_payment'),
                       url(r'^direct-payment/(?P<pk>\d+)/$', payment_views.DirectPaymentUpdateView.as_view(),
                           name='update_direct_payment'),
                       url(r'^direct-payment/(?P<pk>\d+)/delete/$', payment_views.DirectPaymentDeleteView.as_view(),
                           name='delete_direct_payment'),
)
