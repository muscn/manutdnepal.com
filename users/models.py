from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.account.signals import user_logged_in


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
        user.is_admin = True
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

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)

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

    objects = UserManager()


class Membership(models.Model):
    user = models.ForeignKey(User, related_name='membership')
    date_of_birth = models.DateField(null=True)
    temporary_address = models.TextField(null=True)
    permanent_address = models.TextField(null=True)
    homepage = models.URLField(null=True)
    mobile = models.CharField(max_length=50, null=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    identification_type = models.CharField(max_length=50, null=True)
    identification_file = models.FileField(null=True)
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    shirt_size = models.CharField(max_length=4, choices=SHIRT_SIZES, null=True)
    PRESENT_STATUSES = (
        ('S', 'Student'),
        ('E', 'Employed'),
        ('U', 'Unemployed'),
    )
    present_status = models.CharField(max_length=1, choices=PRESENT_STATUSES, null=True)
    registration_date = models.DateField(null=True)
    approved_date = models.DateField(null=True, blank=True)
    MEMBERSHIP_STATUSES = (
        ('P', 'Pending'),
        ('A', 'Active'),
        ('E', 'Expired'),
    )
    membership_status = models.CharField(max_length=1, choices=MEMBERSHIP_STATUSES, null=True)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            # if bool(u.groups.filter(name__in=group_names)) | u.is_superuser():
            # return True
            if bool(u.groups.filter(name__in=group_names)):
                return True
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
    import ipdb

    ipdb.set_trace()

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