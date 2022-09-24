"""
All Model should be an sql table.
"""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


BOOK_TYPES = [
    ('ebook', 'EBOOK'),
    ('paper', 'PAPERBOOK'),
]

TRACK_TYPES = [
    ('cancelled', 'CANCELLED'),
    ('preparing', 'PREPARING'),
    ('dispatched', 'DISPATCHED'),
    ('handover', 'HANDOVER_TO_TRANSPORT'),
    ('moving', 'MOVING'),
    ('delivered', 'DELIVERED'),
    ('outofdelivery', 'OUT_OF_DELIVERY'),
]


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_publisher = models.BooleanField(_('publisher'), default=False)
    is_buyer = models.BooleanField(_('buyer'), default=False)
    is_transporter = models.BooleanField(_('transporter'), default=False)
    publisher = models.ForeignKey('Publisher', null=True, blank=True, on_delete=models.CASCADE)  # NOQA
    transporter = models.ForeignKey('Transporter', null=True, blank=True, on_delete=models.CASCADE)  # NOQA

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UploadFile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True)


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Transporter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    ebook_rate = models.IntegerField(default=0, blank=True)
    paperbook_rate = models.IntegerField(default=0, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True)  # NOQA


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # NOQA
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # NOQA
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES)


class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address_line1 = models.TextField(default=None, blank=True, null=True)
    address_line2 = models.TextField(default=None, blank=True, null=True)
    address_line3 = models.TextField(default=None, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # NOQA


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # NOQA
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # NOQA
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # NOQA
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES)
    rate = models.IntegerField(default=0, blank=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_reason = models.TextField(default=None, blank=True, null=True)
    cancelled_at = models.DateTimeField(default=None, blank=True, null=True)


class PaperBookOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)  # NOQA
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)  # NOQA
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)  # NOQA
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE)  # NOQA
    is_dispatched = models.BooleanField(default=False)
    dispatched_at = models.DateTimeField(default=None, blank=True, null=True)
    is_handover_to_transporter = models.BooleanField(default=False)
    handover_to_transporter_at = models.DateTimeField(default=None, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(default=None, blank=True, null=True)


class PaperBookOrderTrack(models.Model):
    id = models.AutoField(primary_key=True)
    paper_book_order = models.ForeignKey(PaperBookOrder, on_delete=models.CASCADE)  # NOQA
    tracker = models.CharField(max_length=20, choices=TRACK_TYPES)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
