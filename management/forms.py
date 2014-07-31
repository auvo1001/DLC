from django import forms
from django.contrib.admin import widgets
from management.models import Package, Sender, Receiver, Store, User
from django.contrib.auth.models import User
from functools import partial

class PackageCreateForm(forms.ModelForm):
    type_choices = [('Door To Door', 'Door To Door',), ('Air To Air', 'Air To Air',)]
    p_type_field = forms.CharField(widget=forms.RadioSelect(choices=type_choices), initial = 'Door To Door')


    class Meta:
        model = Package
        exclude =['p_receiver','p_sender','p_status','p_insurance','p_tax']

class PackageStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Package
        exclude =['p_receiver','p_sender']


class SenderCreateForm(forms.ModelForm):

    class Meta:
        model = Sender


class ReceiverCreateForm(forms.ModelForm):

    class Meta:
        model = Receiver

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store

