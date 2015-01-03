from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.account.signals import user_logged_in
from apps.payment.models import Payment


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, full_name=''):
        # import pdb
        # pdb.set_trace()
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, full_name=''):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            full_name=full_name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def by_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return self.filter(groups=group)
        except Group.DoesNotExist:
            return False


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=245)
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
        db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)

    def is_member(self):
        # TODO handle RelatedObjectDoesNotExist
        return True if self.membership.payment and self.membership.approved_date and self.membership.approved_by and self.membership.status == 'A' else False

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by username
        return self.username

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email):
        pass

    def is_admin(self):
        return self.is_superuser

    def in_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return group in self.groups.all()
        except Group.DoesNotExist:
            return False

    def add_to_group(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            self.groups.add(group)
            return True
        except Group.DoesNotExist:
            return False

    def get_sample_card(self):
        from django.core.cache import cache

        cached = cache.get('sample_card_' + str(self.id))
        if cached:
            return cached

        from django.conf import settings
        from PIL import ImageFont
        from PIL import Image
        from PIL import ImageDraw
        from urllib import urlretrieve
        import os
        import re

        pk = self.pk
        name = self.full_name
        phone = self.membership.mobile
        devil_number = u'007'

        # The co-ordinates
        devil_number_ending_xy = (744, 68)
        name_ending_xy = (1010, 438)
        phone_ending_xy = (1010, 520)
        qr_xy = (65, 393)

        # The font-sizes
        devil_number_size = 58
        name_size = 60
        phone_size = 43

        # Configuration
        base_image = os.path.join(settings.STATIC_ROOT, 'img', 'watermarked.jpg')
        draw_qr = True
        # possible values: L, M, Q, H
        qr_error_correction = 'M'

        # Pre-process the name
        name = name.upper()
        names = name.split()
        last_name = names[-1]
        names_sans_last = names[0:-1]
        if len(names_sans_last) > 1:
            middle_names = names_sans_last[1:]
            # multiple middle names support - Amrit Bahadur Khanal Kshetri :D
            middle_name_initials_list = [middle_name[0] + '.' for middle_name in middle_names]
            middle_name_initials = '  '.join(middle_name_initials_list)
            name_sans_last = names_sans_last[0] + '  ' + middle_name_initials + ' '
        else:
            name_sans_last = names_sans_last[0] + ' '

        # Pre-process the phone number
        phone_code = None
        pattern = '^([0|\\+[0-9]{1,5})?[-\s]?([7-9][0-9]{9})$'
        matches = re.search(pattern, phone)
        if matches:
            phone_code = matches.groups()[0]
            phone = matches.groups()[1]
            if phone_code:
                phone_code = phone_code.strip('\n\t\r\+\-')
                phone_code = phone_code.lstrip('00')
            else:
                phone_code = '977'
            phone_code = '+' + phone_code + '  '

        img = Image.open(base_image)
        # img = Image.open('watermarked_with_qr.jpg')
        # img = Image.open('front.jpg')

        draw = ImageDraw.Draw(img)

        # write devil number
        devil_number_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-ThinItalic.otf'),
                                               devil_number_size)
        devil_number_text_size = draw.textsize('#' + devil_number, font=devil_number_font)
        devil_number_xy = (devil_number_ending_xy[0] - devil_number_text_size[0], devil_number_ending_xy[1])
        draw.text(devil_number_xy, '#' + devil_number, (255, 255, 255), font=devil_number_font)

        # write name
        name_sans_last_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-ThinItalic.otf'),
                                                 name_size)
        name_sans_last_size = draw.textsize(name_sans_last, font=name_sans_last_font)
        last_name_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-Italic.otf'),
                                            name_size)
        last_name_size = draw.textsize(last_name, last_name_font)
        name_length = name_sans_last_size[0] + last_name_size[0]
        name_xy = (name_ending_xy[0] - name_length, name_ending_xy[1])
        last_name_xy = (name_xy[0] + name_sans_last_size[0], name_xy[1])
        draw.text(name_xy, name_sans_last, (255, 255, 255), font=name_sans_last_font)
        draw.text(last_name_xy, last_name, (255, 255, 255), font=last_name_font)

        # write phone number
        phone_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-Italic.otf'),
                                        phone_size)
        phone_font_size = draw.textsize(phone, phone_font)
        phone_xy = (phone_ending_xy[0] - phone_font_size[0], phone_ending_xy[1])
        draw.text(phone_xy, phone, (255, 255, 255), font=phone_font)
        if phone_code:
            phone_code_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-ThinItalic.otf'),
                                                 phone_size)
            phone_code_size = draw.textsize(phone_code, phone_code_font)
            phone_code_xy = (phone_xy[0] - phone_code_size[0], phone_ending_xy[1])
            draw.text(phone_code_xy, phone_code, (255, 255, 255), font=phone_code_font)

        if draw_qr:
            # download qr
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'qrs')):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qrs'))
            urlretrieve(
                'http://api.qrserver.com/v1/create-qr-code/?data=http://manutd.org.np/' + devil_number + '&size=208x208&ecc=' + qr_error_correction + '&color=ffffff&bgcolor=000',
                os.path.join(settings.MEDIA_ROOT, 'qrs', str(pk) + '.png'))
            qr = Image.open(os.path.join(settings.MEDIA_ROOT, 'qrs', str(pk) + '.png'))
            #make qr transparent
            qr = qr.convert('RGBA')
            data = qr.getdata()
            new_data = []
            for item in data:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            qr.putdata(new_data)
            qr.save(os.path.join(settings.MEDIA_ROOT, 'qrs', str(pk) + '.png'))
            # write qr to image
            img = img.convert('RGBA')
            img.paste(qr, qr_xy, qr)

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'sample_cards')):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'sample_cards'))

        img.save(os.path.join(settings.MEDIA_ROOT, 'sample_cards', str(pk) + '.png'))

        # img = Image.open(os.path.join(settings.STATIC_ROOT, 'img', 'watermarked_card.jpg'))
        # draw = ImageDraw.Draw(img)
        # # write devil number
        # font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-ThinItalic.otf'), 19)
        # draw.text((613, 75), "#007", (255, 255, 255), font=font)
        # # write name
        # font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-Regular.otf'), 19)
        # draw.text((433, 438), self.full_name, (255, 255, 255), font=font)
        # # write phone number
        # font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'fonts', 'Aileron-Regular.otf'), 19)
        # draw.text((643, 521), self.membership.mobile, (255, 255, 255), font=font)
        # # download qr
        # # if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'qrs')):
        # # os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qrs'))
        # # urlretrieve('http://api.qrserver.com/v1/create-qr-code/?data=http://manutd.org.np/007&size=160x160&ecc=H',
        # #             os.path.join(settings.MEDIA_ROOT, 'qrs', str(self.id) + '.png'))
        # # qr = Image.open(os.path.join(settings.MEDIA_ROOT, 'qrs', str(self.id) + '.png'))
        # # write qr to image
        # # draw.bitmap((65, 302), qr)
        # if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'sample_cards')):
        #     os.makedirs(os.path.join(settings.MEDIA_ROOT, 'sample_cards'))
        # img.save(os.path.join(settings.MEDIA_ROOT, 'sample_cards', str(self.id) + '.jpg'))
        # import ipdb
        # ipdb.set_trace()

        url = settings.MEDIA_URL + 'sample_cards/' + str(pk) + '.png'
        cache.set('sample_card_' + str(self.id), url)
        return url

    objects = UserManager()


class Membership(models.Model):
    user = models.OneToOneField(User, related_name='membership')
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(null=True, max_length=1)
    temporary_address = models.TextField(null=True)
    permanent_address = models.TextField(null=True)
    homepage = models.URLField(null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    identification_type = models.CharField(max_length=50, null=True)
    identification_file = models.FileField(null=True)
    shirt_size = models.CharField(max_length=4, null=True)
    present_status = models.CharField(max_length=1, null=True)
    registration_date = models.DateField(null=True)
    approved_date = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(User, related_name='memberships_approved', null=True, blank=True)
    MEMBERSHIP_STATUSES = (
        ('P', 'Pending'),
        ('A', 'Active'),
        ('E', 'Expired'),
    )
    status = models.CharField(max_length=1, choices=MEMBERSHIP_STATUSES, null=True)
    payment = models.ForeignKey(Payment, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            # if bool(u.groups.filter(name__in=group_names)) | u.is_superuser():
            # return True
            if bool(u.groups.filter(name__in=group_names)):
                return True
            raise PermissionDenied()
        return False

    return user_passes_test(in_groups)


class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = _('Group')
        # verbose_name_plural = _('Groups')


# @receiver(user_signed_up)
@receiver(user_logged_in)
def get_extra_data(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        extra_data = sociallogin.account.extra_data

        if sociallogin.account.provider == 'twitter':
            user.full_name = extra_data['name']

        if sociallogin.account.provider == 'facebook':
            user.full_name = extra_data['name']
            if extra_data['gender'] == 'male':
                user.gender = 'M'
            elif extra_data['gender'] == 'female':
                user.gender = 'F'

        if sociallogin.account.provider == 'google':
            pass
            # user.first_name = sociallogin.account.extra_data['given_name']
            # user.last_name = sociallogin.account.extra_data['family_name']
            # verified = sociallogin.account.extra_data['verified_email']
            # picture_url = sociallogin.account.extra_data['picture']

        user.save()