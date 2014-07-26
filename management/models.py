from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote
from decimal import Decimal

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
    sender = models.ForeignKey(Sender)
    receiver = models.ForeignKey(Receiver)
    weight = models.DecimalField(max_digits= 10, decimal_places=2)
    piece = models.IntegerField()
    content = models.TextField()
    value = models.DecimalField(max_digits= 10, decimal_places=2) #not used
    insurance = models.DecimalField(max_digits= 10, decimal_places=2, default=0) #not used
    tax = models.DecimalField(max_digits= 10, decimal_places=2,  default=0) #not used
    extra_charge = models.DecimalField(max_digits= 10, decimal_places=2,  default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    receiver2 = models.CharField(max_length=255,blank=True)
    phone2 = models.CharField(max_length=50,blank=True)
    receipt_signature = models.FileField(upload_to='receipt_signature/%Y/%m/%d', max_length=100, blank=True)

    #tracking choices
    bat_dau = "bat dau"
    tren_may_bay = "tren may bay"
    den_Hai_Quan_VN = "den Hai Quan VN"
    da_giao_hang= "da giao hang"
    status_choices = (
        (bat_dau,  "bat dau"),
        (tren_may_bay, "tren may bay"),
        (den_Hai_Quan_VN, "den Hai Quan VN"),
        (da_giao_hang, "da giao hang"),
                    )
    status = models.CharField(max_length=50, choices = status_choices, default = bat_dau ) #bat dau, tren may bay, den Hai Quan VN, da giao hang

    #type
    to_air = "Air To Air"
    to_door = "Door To Door"
    type_choices = (
        (to_air, "Air To Air"),
        (to_door,"Door To Door"),
                    )
    type_field = models.CharField(max_length=100, choices = type_choices, default = to_door )

    def is_delivered(self):
        return self.status in (self.da_giao_hang)

    def get_rate(self):
        if self.type_field == self.to_door:
            price_type = Tinh.objects.get(name = self.receiver.tinh_thanhpho).price_type
            if self.weight <=5:
                return Decimal(price_type) * 5
            elif self.weight > 5 and self.weight <10:
                return self.weight * price_type
            elif self.weight >= 10 and self.weight <30:
                return self.weight * ( Decimal(price_type) - Decimal(0.25))
            elif self.weight >= 30:
                return self.weight * ( Decimal(price_type) - Decimal(0.5))
        elif self.type == self.to_air:
            return 1.20

    def subtotal(self):
        return self.get_rate() + self.extra_charge + self.tax + self.insurance


    def get_absolute_url(self):
        return self.id


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

