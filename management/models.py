from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote


# Create your models here.
class Tinh(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=128)
    price_type= models.IntegerField()
    # 1 is SG, 2 is everything else
    def __unicode__(self):
         return self.name

class Sender(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    address1 = models.CharField( max_length=255)
    address2 = models.CharField( max_length=255, blank=True)
    city = models.CharField( max_length=128)
    state_province = models.CharField(max_length=255)
    zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.phone


class Receiver(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    address1 = models.CharField( max_length=255)
    address2 = models.CharField( max_length=255, blank=True)
    quan_huyen = models.CharField( max_length=255)
    tinh_thanhpho = models.ForeignKey(Tinh)
    phone1 = models.CharField(max_length=50)
    phone2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.phone1

class Package(models.Model):
    tracking = models.CharField(max_length=255)
    sender = models.ForeignKey(Sender)
    receiver = models.ForeignKey(Receiver)
    weight = models.IntegerField()
    piece = models.IntegerField()
    content = models.TextField(blank=True)
    value = models.IntegerField()
    insurance = models.IntegerField(blank=True)
    tax = models.IntegerField(blank=True)
    extra_charge = models.IntegerField(blank=True)
    price = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50) #bat dau, tren may bay, den Hai Quan VN, da giao hang
    sender2 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=50)
    #upload file?

    def __unicode__(self):
        return self.tracking

class Store(models.Model):
    name = models.CharField(max_length=255)
    address1 = models.CharField( max_length=255)
    address2 = models.CharField( max_length=255, blank=True)
    city = models.CharField( max_length=128)
    state_province = models.CharField(max_length=255)
    zip = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.city)


class User(models.Model):
    user = models.OneToOneField(User)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

