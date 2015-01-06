from django.conf.urls import patterns, url
from . import views
from apps.payment import views as payment_views
from apps.users import views as users_views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='dashboard_index'),

                       # TODO Move to payment app
                       url(r'^payment/$', payment_views.PaymentListView.as_view(), name='list_payments'),
                       # url(r'^payment/add/$', payment_views.PaymentCreateView.as_view(), name='create_payment'),
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

                       url(r'^audit-log/$', views.AuditLogListView.as_view(), name='audit_log'),

                       url(r'^membership/$', users_views.MembershipListView.as_view(), name='list_memberships'),
                       url(r'^membership/add/(?P<pk>\d+)/$', users_views.MembershipCreateView.as_view(),
                           name='create_membership'),
                       url(r'^membership/(?P<pk>\d+)/$', users_views.MembershipUpdateView.as_view(),
                           name='update_membership'),
                       url(r'^delete-membership/(?P<pk>\d+)/delete/$', users_views.MembershipDeleteView.as_view(),
                           name='delete_membership'),
                       url(r'^membership/add/$', users_views.new_user_membership, name='new_membership'),

                       url(r'^user/$', users_views.UserListView.as_view(), name='list_users'),
                       url(r'^user/add/$', users_views.UserCreateView.as_view(), name='create_user'),
                       url(r'^user/(?P<pk>\d+)/$', users_views.UserUpdateView.as_view(),
                           name='update_user'),
                       url(r'^delete-user/(?P<pk>\d+)/delete/$', users_views.UserDeleteView.as_view(),
                           name='delete_user'),

                       url(r'^staff/$', users_views.StaffListView.as_view(), name='list_staffs'),
)
