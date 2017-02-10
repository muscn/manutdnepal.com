import datetime
from io import BytesIO
import os

from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from django.views.generic import DetailView
from allauth.account.forms import LoginForm, SignupForm
from django.views.generic.list import ListView
from django.db.models import Max, Min
from auditlog.models import LogEntry
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import Membership, User, StaffOnlyMixin, group_required, CardStatus, get_new_cards, Renewal, \
    MembershipSetting
from .forms import MembershipForm, UserForm, UserUpdateForm
from apps.payment.forms import BankDepositForm
from apps.payment.models import BankAccount, Payment, EsewaPayment, DirectPayment
from muscn.utils.football import get_current_season_start
from muscn.utils.helpers import insert_row
from muscn.utils.mixins import UpdateView, CreateView, DeleteView
from apps.payment.forms import BankDepositPaymentForm, DirectPaymentPaymentForm, DirectPaymentReceiptForm
from apps.users import membership_settings


def login_register(request):
    if request.user.is_authenticated():
        return redirect(reverse('membership_form'))
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'account/login_register.html', {'login_form': login_form, 'signup_form': signup_form})


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard_index.html')
    return login(request)


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


@login_required
def membership_form(request):
    user = request.user
    try:
        item = user.membership
        # return redirect(reverse('membership_payment'))
    except Membership.DoesNotExist:
        item = Membership(user=user)
    # item = Membership(user=user)
    accounts = sorted(user.socialaccount_set.all(), key=lambda x: x.provider, reverse=True)
    for account in accounts:
        if account.provider == 'facebook':
            extra_data = account.extra_data
            try:
                item.gender = extra_data['gender'][:1].upper()
            except KeyError:
                pass
            try:
                item.date_of_birth = datetime.datetime.strptime(extra_data['birthday'], '%m/%d/%Y').strftime('%Y-%m-%d')
            except KeyError:
                pass
            try:
                item.temporary_address = extra_data['location']['name']
            except KeyError:
                pass
            try:
                item.permanent_address = extra_data['hometown']['name']
            except KeyError:
                pass

    if request.POST:
        form = MembershipForm(request.POST, request.FILES, instance=item, user=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('membership_payment'))
    else:
        form = MembershipForm(instance=item, user=request.user)
    return render(request, 'membership_form.html', {
        'form': form,
        'base_template': 'base.html',
    })


@login_required
def membership_payment(request):
    # check if membership form has been received
    try:
        membership = request.user.membership
        if membership.status == 'A':
            return redirect(reverse('view_profile'))
        elif membership.status == 'E':
            return redirect(reverse('renew_membership'))
    except Membership.DoesNotExist:
        return redirect(reverse('membership_form'))
    bank_deposit_form = BankDepositForm()
    direct_payment_form = DirectPaymentPaymentForm()
    if request.POST:
        from apps.users import membership_settings

        payment = Payment(user=request.user, amount=membership_settings.membership_fee)
        if request.POST.get('method') == 'direct':
            direct_payment_form = DirectPaymentReceiptForm(request.POST, request.FILES)
            if direct_payment_form.is_valid():
                payment.save()
                direct_payment = direct_payment_form.save(commit=False, user=request.user, payment=payment)
                # direct_payment.payment = payment
                direct_payment.save()
        elif request.POST.get('method') == 'bank':
            bank_deposit_form = BankDepositForm(request.POST, request.FILES)
            bank_deposit = bank_deposit_form.save(commit=False)
            payment.save()
            bank_deposit.payment = payment
            bank_deposit.save()
        if payment.id:
            membership.payment = payment
            membership.save()
            return redirect(reverse('membership_thankyou'))
    bank_accounts = BankAccount.objects.all()
    return render(request, 'membership_payment.html', {
        'membership': membership,
        'bank_deposit_form': bank_deposit_form,
        'direct_payment_form': direct_payment_form,
        'bank_accounts': bank_accounts,
        'base_template': 'base.html',
    })


@login_required
def membership_thankyou(request):
    try:
        membership = request.user.membership
    except Membership.DoesNotExist:
        return redirect(reverse('membership_form'))
    if not membership.payment:
        return redirect(reverse('membership_payment'))
    return render(request, 'membership_thankyou.html', {
        'membership': membership,
        'base_template': 'base.html',
    })


class PublicMembershipListView(ListView):
    model = User
    template_name = 'users/members_list.html'

    def get_queryset(self):
        qs = User.objects.all().select_related('membership__card_status')
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(full_name__icontains=q) |
                Q(email__icontains=q) |
                Q(devil_no__contains=q) |
                Q(membership__telephone__contains=q) |
                Q(membership__mobile__contains=q)
            )
        return qs


class MembershipListView(StaffOnlyMixin, ListView):
    model = Membership

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = Membership.objects.filter(
                Q(user__username__icontains=q) |
                Q(user__full_name__icontains=q) |
                Q(user__email__icontains=q) |
                Q(user__devil_no__contains=q) |
                Q(telephone__contains=q) |
                Q(mobile__contains=q)
            )
        return super(MembershipListView, self).get(request, *args, **kwargs)


class RenewalListView(StaffOnlyMixin, ListView):
    model = Renewal

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = Renewal.objects.filter(
                Q(membership__user__username__icontains=q) |
                Q(membership__user__full_name__icontains=q) |
                Q(membership__user__email__icontains=q) |
                Q(membership__user__devil_no__contains=q) |
                Q(membership__telephone__contains=q) |
                Q(membership__mobile__contains=q)
            )
        return super(RenewalListView, self).get(request, *args, **kwargs)


class MembershipCreateView(StaffOnlyMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def get_form(self, form_class):
        form = super(MembershipCreateView, self).get_form(form_class)
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipUpdateView(StaffOnlyMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            obj = self.get_object()

            if request.POST['action'] == 'Approve':
                if not hasattr(obj, 'payment') or not obj.payment:
                    messages.error(request, 'No payment associated with the membership!')
                elif not obj.payment.verified:
                    messages.error(request, 'Associated payment hasn\'t been verified!')
                else:
                    obj.approved_by = request.user
                    if not obj.user.devil_no:
                        max_devil_no = User.objects.aggregate(Max('devil_no'))['devil_no__max']
                        if max_devil_no is None:
                            max_devil_no = 100
                        obj.user.devil_no = max_devil_no + 1
                        obj.user.save()
                    obj.approved_date = datetime.datetime.now()
                    obj.expiry_date = get_current_season_start() + datetime.timedelta(days=365)
                    messages.info(request, 'The membership is approved!')
                    obj.save()
                    if not hasattr(obj, 'card_status'):
                        card_status = CardStatus(membership=obj)
                    else:
                        card_status = CardStatus.objects.get(membership=obj)
                    card_status.status = 1
                    card_status.notify()
                    card_status.save()
            elif request.POST['action'] == 'Disprove':
                obj.approved_by = None
                messages.info(request, 'The membership is disproved!')
                obj.save()
            elif request.POST['action'] == 'Download Card':
                return obj.user.get_card_download()
            return redirect(reverse_lazy('update_membership', kwargs={'pk': obj.pk}))
        else:
            return super(MembershipUpdateView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(MembershipUpdateView, self).get_form(form_class)
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipDeleteView(StaffOnlyMixin, DeleteView):
    model = Membership
    success_url = reverse_lazy('list_memberships')


class UserListView(StaffOnlyMixin, ListView):
    model = User

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = User.objects.filter(
                Q(username__icontains=q) |
                Q(full_name__icontains=q) |
                Q(email__icontains=q) |
                Q(devil_no__contains=q) |
                Q(membership__telephone__contains=q) |
                Q(membership__mobile__contains=q)
            )
        return super(UserListView, self).get(request, *args, **kwargs)


class UserCreateView(StaffOnlyMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('list_users')


class UserUpdateView(StaffOnlyMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('list_users')


class UserDeleteView(StaffOnlyMixin, DeleteView):
    model = User
    success_url = reverse_lazy('list_users')


class StaffListView(StaffOnlyMixin, ListView):
    model = User
    template_name = 'users/staff_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(groups__name='Staff')
        return queryset


class StaffDetailView(StaffOnlyMixin, DetailView):
    model = User
    template_name = 'users/staff_detail.html'

    def get_queryset(self):
        queryset = User.objects.filter(groups__name='Staff')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        staff = self.get_object()
        context['memberships_approved'] = staff.memberships_approved.all()
        context['payments_verified'] = staff.verified_payments.all()
        context['audit_log'] = LogEntry.objects.filter(actor=staff)
        return context


@group_required('Staff')
def new_user_membership(request):
    user_form = UserForm(prefix='uf')
    member_form = MembershipForm(prefix='mf')

    payment_initial = {
        'amount': membership_settings.membership_fee,
        'date_time': datetime.datetime.now()
    }
    bank_deposit_form = BankDepositPaymentForm(prefix='bf', initial=payment_initial)
    direct_payment_form = DirectPaymentPaymentForm(prefix='df', initial=payment_initial)
    if request.POST:

        user_form = UserForm(request.POST, request.FILES, prefix='uf')
        member_form = MembershipForm(request.POST, request.FILES, prefix='mf', exclude='full_name')

        # find out the payment form from the hidden field
        if request.POST['payment_method'] == 'bank-deposit':
            bank_deposit_form = BankDepositPaymentForm(request.POST, request.FILES, prefix='bf', exclude='user')
            payment_form = bank_deposit_form
        elif request.POST['payment_method'] == 'direct-payment':
            direct_payment_form = DirectPaymentPaymentForm(request.POST, prefix='df', exclude='user')
            payment_form = direct_payment_form

        if user_form.is_valid() and member_form.is_valid() and payment_form.is_valid():
            user = user_form.save()
            payment_method = payment_form.save(user=user)
            membership = member_form.save(commit=False)
            membership.user = user
            membership.payment = payment_method.payment
            membership.save()
            return redirect(reverse_lazy('list_memberships'))
    context = {
        'user_form': user_form,
        'membership_form': member_form,
        'bank_deposit_form': bank_deposit_form,
        'direct_payment_form': direct_payment_form,
    }
    return render(request, 'users/new_user_membership.html', context)


def esewa_success(request):
    # {u'oid': [u'm_2_2015'], u'amt': [u'150'], u'refId': [u'0000ELD']}
    response = dict(request.GET)
    membership = request.user.membership
    payment = Payment(user=request.user, amount=membership_settings.membership_fee)
    esewa_payment = EsewaPayment(amount=payment.amount, pid=response['oid'][0], ref_id=response['refId'][0])
    if esewa_payment.verify():
        payment.save()
        esewa_payment.payment = payment
        esewa_payment.get_details()
        esewa_payment.save()
        membership.payment = payment
        membership.save()
        messages.success(request, 'Membership fee received via eSewa.')
        return redirect(reverse('membership_thankyou'))
    else:
        messages.error(request, 'Payment via eSewa failed!')
        return redirect('membership_payment')


def esewa_failure(request):
    # {u'q': [u'fu']}
    messages.error(request, 'eSewa transaction failed or cancelled!')
    return redirect('membership_payment')


def download_all_cards(request):
    filtered = [x for x in Membership.objects.all() if x.approved()]


def devil_no_handler(request, devil_no):
    # if int(devil_no) < 100:
    #     raise Http404('Member does not exist!')
    user = get_object_or_404(User, devil_no=devil_no)
    return redirect(reverse_lazy('view_member_profile', kwargs={'slug': user.username}))


class MemberProfileView(DetailView):
    model = User
    slug_field = 'username'


class DirectPaymentForMembershipCreateView(StaffOnlyMixin, CreateView):
    model = DirectPayment
    form_class = DirectPaymentPaymentForm
    # success_url = reverse_lazy('list_memberships')

    def get_success_url(self):
        return reverse_lazy('update_direct_payment', kwargs={'pk': self.object.id})

    def get_initial(self):
        membership = get_object_or_404(Membership, id=self.kwargs['pk'])
        return {'amount': membership_settings.membership_fee, 'received_by': self.request.user, 'user': membership.user,
                'date_time': datetime.datetime.now(), 'remarks': 'For Membership'}

    def form_valid(self, form):
        membership = get_object_or_404(Membership, id=self.kwargs['pk'])
        ret = super(DirectPaymentForMembershipCreateView, self).form_valid(form)
        membership.payment = form.instance.payment
        membership.save()
        return ret


@group_required('Staff')
def download_new_cards(request):
    from django.http import HttpResponse

    zip_name, new_cards = get_new_cards()
    response = HttpResponse(new_cards.getvalue(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=' + zip_name
    return response


@group_required('Staff')
def email_new_cards(request):
    zip_name, new_cards = get_new_cards()
    mail = EmailMessage(zip_name, zip_name, settings.DEFAULT_FROM_EMAIL, [settings.ADMINS[0][1]])
    mail.attach(zip_name, new_cards.getvalue(), 'application/zip')
    mail.send()
    messages.info(request, "E-mail sent to " + settings.ADMINS[0][1])
    return redirect(reverse_lazy('list_memberships'))


@login_required
def renew(request):
    user = request.user
    if not hasattr(user, 'membership'):
        return redirect(reverse_lazy('membership_form'))
    if hasattr(user, 'membership') and not user.membership.payment_id:
        return redirect(reverse_lazy('membership_payment'))
    if user.is_member():
        return redirect(reverse_lazy('home'))
    pending_renewal = Renewal.objects.filter(membership__user=request.user, payment__verified_by__isnull=True)
    if pending_renewal.exists():
        messages.warning(request, 'One of your renewal requests is already pending.')
    membership = user.membership
    bank_deposit_form = BankDepositForm()
    direct_payment_form = DirectPaymentPaymentForm()
    if request.POST:
        from apps.users import membership_settings

        payment = Payment(user=request.user, amount=membership_settings.membership_fee, remarks='Renewal')
        if request.POST.get('method') == 'direct':
            direct_payment_form = DirectPaymentReceiptForm(request.POST, request.FILES)
            if direct_payment_form.is_valid():
                payment.save()
                direct_payment = direct_payment_form.save(commit=False, user=request.user, payment=payment)
                # direct_payment.payment = payment
                direct_payment.save()
        elif request.POST.get('method') == 'bank':
            bank_deposit_form = BankDepositForm(request.POST, request.FILES)
            bank_deposit = bank_deposit_form.save(commit=False)
            payment.save()
            bank_deposit.payment = payment
            bank_deposit.save()
        if payment.id:
            renewal = Renewal(membership=membership, payment=payment)
            renewal.save()
            return redirect(reverse('membership_thankyou'))
    bank_accounts = BankAccount.objects.all()
    return render(request, 'users/renew.html', {
        'membership': membership,
        'bank_deposit_form': bank_deposit_form,
        'direct_payment_form': direct_payment_form,
        'bank_accounts': bank_accounts,
        'base_template': 'base.html',
    })


def export_awaiting_print(request):
    query = Membership.objects.filter(card_status__status=1)
    table_header = ['Full Name', 'Gender', 'Devil No.']
    wb = Workbook()
    ws = wb.active
    row_index = insert_row(ws, 1, table_header)
    for obj in query:
        data = [obj.user.full_name.title(), obj.get_gender_display(), obj.user.devil_no]
        row_index = insert_row(ws, row_index, data)
    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
    file_name = 'Awaiting-Print.xlsx'
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response


def export_welcome_letters(request):
    awaiting_members = Membership.objects.filter(card_status__status=1).order_by('-user__devil_no')
    devil_no = Membership.objects.filter(card_status__status=1).aggregate(max_devil_no=Max('user__devil_no'),
                                                                          min_devil_no=Min('user__devil_no'))
    pdfmetrics.registerFont(TTFont('Lato', os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Lato-Regular.ttf')))
    try:
        member_settings = MembershipSetting.objects.get()
    except MembershipSetting.DoesNotExist:
        messages.warning(request, 'Membership Settings Does not exists.')
        return HttpResponseRedirect(reverse('list_memberships'))

    # To insert next line in pdf
    content = member_settings.welcome_letter_content.replace('\n', '<br/>')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="welcome-letters-' + str(
        devil_no.get('min_devil_no')) + '-' + str(devil_no.get('max_devil_no')) + '.pdf'

    buffer = BytesIO()

    if awaiting_members:
        _canvas = canvas.Canvas(buffer)
        _canvas.setFont("Lato", 12)
        width, height = 19 * cm, 40.7 * cm
        style = getSampleStyleSheet()['Normal']
        style.wordWrap = 'LTR'
        style.fontName = 'Lato'
        style.leading = 18
        style.fontSize = 12
        for awaiting_member in awaiting_members:
            _canvas.drawString(50, 630, datetime.date.today().strftime('%b %d, %Y'))
            _canvas.drawString(50, 570, 'Dear ' + awaiting_member.user.full_name.title() + ' ( #' + str(
                awaiting_member.user.devil_no) + ' ),')
            p = Paragraph(content, style)
            data = [[p]]
            table = Table(data)
            table.wrapOn(_canvas, width, height)
            table.drawOn(_canvas, 45, 320)
            _canvas.drawString(50, 220, "With best regards,")
            _canvas.drawString(50, 145, "Chairman")
            _canvas.drawString(50, 125, "Manchester United Supporters' Club - Nepal")
            _canvas.showPage()
        _canvas.save()
    else:
        messages.warning(request, 'No Awaiting members.')
        return HttpResponseRedirect(reverse('list_memberships'))
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def export_name_and_number(request):
    awaiting_members = Membership.objects.filter(card_status__status=1).order_by('-user__devil_no')
    devil_no = Membership.objects.filter(card_status__status=1).aggregate(max_devil_no=Max('user__devil_no'),
                                                                          min_devil_no=Min('user__devil_no'))
    pdfmetrics.registerFont(TTFont('Lato', os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Lato-Regular.ttf')))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="name-number-' + str(
        devil_no.get('min_devil_no')) + '-' + str(devil_no.get('max_devil_no')) + '.pdf'

    buffer = BytesIO()

    if awaiting_members:
        _canvas = canvas.Canvas(buffer)
        style = getSampleStyleSheet()['Normal']
        style.wordWrap = 'LTR'
        style.fontName = 'Lato'
        style.leading = 18
        style.fontSize = 12
        for awaiting_member in awaiting_members:
            _canvas.setFont("Lato", 12)
            _canvas.setPageSize((4.5 * inch, 9.5 * inch))
            _canvas.drawCentredString(2.25 * inch, 620, '# ' + str(awaiting_member.user.devil_no))
            _canvas.drawCentredString(2.25 * inch, 605, awaiting_member.user.full_name.title())
            _canvas.drawCentredString(2.25 * inch, 590, awaiting_member.mobile)
            _canvas.showPage()
        _canvas.save()
    else:
        messages.warning(request, 'No Awaiting members.')
        return HttpResponseRedirect(reverse('list_memberships'))
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
