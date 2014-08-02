from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote
from decimal import Decimal



# Create your models here.
class Tinh(models.Model):
    t_name = models.CharField(max_length=255)
    t_region = models.CharField(max_length=128)
    t_price_type= models.IntegerField()
    # 1 is SG, 2 is everything else
    def __unicode__(self):
         return self.t_name

class Sender(models.Model):
    s_fname = models.CharField(max_length=255)
    s_lname = models.CharField(max_length=255)
    s_address1 = models.CharField( max_length=255)
    s_address2 = models.CharField( max_length=255, blank=True)
    s_city = models.CharField( max_length=128)
    s_state_province = models.CharField(max_length=255)
    s_zip = models.CharField(max_length=100)
    s_phone = models.CharField(max_length=50)
    s_email = models.EmailField(max_length=100, blank=True)
    s_added = models.DateTimeField(auto_now_add=True)
    s_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.s_phone

    def s_fullname(self):
        return '%s %s' % (self.s_lname, self.s_fname)


class Receiver(models.Model):
    r_fname = models.CharField(max_length=255)
    r_lname = models.CharField(max_length=255)
    r_address1 = models.CharField( max_length=255)
    r_address2 = models.CharField( max_length=255, blank=True)
    r_quan_huyen = models.CharField( max_length=255)
    r_tinh_thanhpho = models.ForeignKey(Tinh)
    r_phone1 = models.CharField(max_length=50)
    r_phone2 = models.CharField(max_length=50, blank=True)
    r_email = models.EmailField(max_length=100, blank=True)
    r_added = models.DateTimeField(auto_now_add=True)
    r_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.r_phone1

    def r_fullname(self):
        return '%s %s' % (self.r_lname, self.r_fname)

class Package(models.Model):
    p_sender = models.ForeignKey(Sender)
    p_receiver = models.ForeignKey(Receiver)
    p_weight = models.DecimalField(max_digits= 10, decimal_places=2)
    p_piece = models.IntegerField()
    p_content = models.TextField()
    p_value = models.DecimalField(max_digits= 10, decimal_places=2) #not used
    p_insurance = models.DecimalField(max_digits= 10, decimal_places=2, default=0) #not used
    p_tax = models.DecimalField(max_digits= 10, decimal_places=2,  default=0) #not used
    p_extra_charge = models.DecimalField(max_digits= 10, decimal_places=2,  default=0)
    p_added = models.DateTimeField(auto_now_add=True)
    p_updated = models.DateTimeField(auto_now=True)
    p_receiver2 = models.CharField(max_length=255,blank=True)
    p_phone2 = models.CharField(max_length=50,blank=True)
    p_receipt_signature = models.FileField(upload_to='receipt_signature/%Y/%m/%d', max_length=100, blank=True)

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
    p_status = models.CharField(max_length=50, choices = status_choices, default = bat_dau ) #bat dau, tren may bay, den Hai Quan VN, da giao hang

    #type
    to_air = "Air To Air"
    to_door = "Door To Door"
    type_choices = (
        (to_air, "Air To Air"),
        (to_door,"Door To Door"),
                    )
    p_type_field = models.CharField(max_length=100, choices = type_choices, default = to_door )

    def is_not_shipped(self):
        return self.p_status in (self.bat_dau)

    def is_en_route(self):
        return self.p_status in (self.tren_may_bay)

    def is_delivered(self):
        return self.p_status in (self.da_giao_hang)

    def is_at_custom(self):
        return self.p_status in (self.den_Hai_Quan_VN)

    def get_rate(self):
        if self.p_type_field == self.to_door:
            price_type = Tinh.objects.get(t_name = self.p_receiver.r_tinh_thanhpho).t_price_type
            if self.p_weight <=5:
                return Decimal(price_type) * 5
            elif self.p_weight > 5 and self.p_weight <10:
                return self.p_weight * price_type
            elif self.p_weight >= 10 and self.p_weight <30:
                return self.p_weight * ( Decimal(price_type) - Decimal(0.25))
            elif self.p_weight >= 30:
                return self.p_weight * ( Decimal(price_type) - Decimal(0.5))
        elif self.p_type_field == self.to_air:
            if self.p_weight <=20:
                return 20 * 1.20
            else:
                return p_weight * 1.20

    def subtotal(self):
        return Decimal(self.get_rate()) + self.p_extra_charge + self.p_tax + self.p_insurance

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return self.id


class Store(models.Model):
    st_name = models.CharField(max_length=255)
    st_address1 = models.CharField( max_length=255)
    st_address2 = models.CharField( max_length=255, blank=True)
    st_city = models.CharField( max_length=128)
    st_state_province = models.CharField(max_length=255)
    st_zip = models.CharField(max_length=100)
    st_added = models.DateTimeField(auto_now_add=True)
    st_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.city)


class User(models.Model):
    u_user = models.OneToOneField(User)
    u_added = models.DateTimeField(auto_now_add=True)
    u_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

