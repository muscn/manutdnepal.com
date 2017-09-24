from django.conf.urls import url
from . import views
from apps.payment import views as payment_views
from apps.users import views as users_views
from apps.stats import views as stats_views

urlpatterns = [
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
    url(r'^move-direct/(?P<pk>\d+)/$', payment_views.move_bank_to_direct_payment,
        name='move_bank_to_direct_payment'),

    url(r'^direct-payment/$', payment_views.DirectPaymentListView.as_view(),
        name='list_direct_payments'),
    url(r'^direct-payment/add/$', payment_views.DirectPaymentCreateView.as_view(),
        name='create_direct_payment'),
    url(r'^direct-payment/membership/(?P<pk>\d+)/$', users_views.DirectPaymentForMembershipCreateView.as_view(),
        name='create_direct_payment_for_membership'),
    url(r'^direct-payment/(?P<pk>\d+)/$', payment_views.DirectPaymentUpdateView.as_view(),
        name='update_direct_payment'),
    url(r'^direct-payment/(?P<pk>\d+)/delete/$', payment_views.DirectPaymentDeleteView.as_view(),
        name='delete_direct_payment'),
    url(r'^esewa-payment/$', payment_views.EsewaPaymentListView.as_view(),
        name='list_esewa_payments'),

    url(r'^audit-log/$', views.AuditLogListView.as_view(), name='audit_log'),

    url(r'^approve_payment_membership/$', views.approve_payment_membership, name='approve_payment_membership'),

    url(r'^membership/add/(?P<pk>\d+)/$', users_views.MembershipCreateView.as_view(),
        name='create_membership'),
    url(r'^membership/(?P<pk>\d+)/$', users_views.MembershipUpdateView.as_view(),
        name='update_membership'),
    url(r'^delete-membership/(?P<pk>\d+)/delete/$', users_views.MembershipDeleteView.as_view(),
        name='delete_membership'),
    url(r'^membership/add/$', users_views.new_user_membership, name='new_membership'),
    url(r'^membership/download/$', users_views.download_all_cards, name='download_all_cards'),

    url(r'^user/$', users_views.UserListView.as_view(), name='list_users'),
    url(r'^user/add/$', users_views.UserCreateView.as_view(), name='create_user'),
    url(r'^user/(?P<pk>\d+)/$', users_views.UserUpdateView.as_view(),
        name='update_user'),
    url(r'^user/(?P<pk>\d+)/delete/$', users_views.UserDeleteView.as_view(),
        name='delete_user'),

    url(r'^staff/$', users_views.StaffListView.as_view(), name='list_staffs'),
    url(r'^staff/(?P<pk>\d+)/$', users_views.StaffDetailView.as_view(), name='view_staff'),

    url(r'^injury/$', stats_views.InjuryListView.as_view(), name='list_injuries'),
    url(r'^injury/add/$', stats_views.InjuryCreateView.as_view(), name='create_injury'),
    url(r'^injury/(?P<pk>\d+)/$', stats_views.InjuryUpdateView.as_view(), name='update_injury'),
    url(r'^injury/(?P<pk>\d+)/delete/$', stats_views.InjuryDeleteView.as_view(),
        name='delete_injury'),

    url(r'^result/$', stats_views.ResultListView.as_view(), name='list_results'),
    url(r'^result/(?P<pk>\d+)/$', stats_views.ResultUpdateView.as_view(), name='update_result'),

    url(r'^fixture/$', stats_views.FixtureListView.as_view(), name='list_fixtures'),
    url(r'^fixture/(?P<pk>\d+)/$', stats_views.FixtureUpdateView.as_view(), name='update_fixture'),

    url(r'^goal/$', stats_views.GoalListView.as_view(), name='list_goals'),
    url(r'^goal/add/$', stats_views.GoalCreateView.as_view(), name='create_goal'),
    url(r'^goal/(?P<pk>\d+)/$', stats_views.GoalUpdateView.as_view(), name='update_goal'),
    url(r'^goal/(?P<pk>\d+)/delete/$', stats_views.GoalDeleteView.as_view(),
        name='delete_goal'),

    url(r'^quote/$', stats_views.QuoteListView.as_view(), name='list_quotes'),
    url(r'^quote/add/$', stats_views.QuoteCreateView.as_view(), name='create_quote'),
    url(r'^quote/(?P<pk>\d+)/$', stats_views.QuoteUpdateView.as_view(), name='update_quote'),
    url(r'^quote/(?P<pk>\d+)/delete/$', stats_views.QuoteDeleteView.as_view(),
        name='delete_quote'),

    url(r'^download_new_cards/$', users_views.download_new_cards, name='download_new_cards'),
    url(r'^email_new_cards/$', users_views.email_new_cards, name='email_new_cards'),

    url(r'^scrape/(?P<slug>[a-zA-Z0-9_.-]+)/$', stats_views.scrape, name='scrape'),

    url(r'^export_awaiting_print/$', users_views.export_awaiting_print, name='export_awaiting_print'),
    url(r'^export_welcome_letters/$', users_views.export_welcome_letters, name='export_welcome_letters'),
    url(r'^export_name_and_number/$', users_views.export_name_and_number, name='export_name_and_number'),
]
