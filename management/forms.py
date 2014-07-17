from django import forms
from django.contrib.admin import widgets
from management.models import Package, Sender, Receiver, Store, User
from django.contrib.auth.models import User
from functools import partial
from django.views.generic.edit import UpdateView

class PackageForm(forms.ModelForm):

    class Meta:
        model = Package

class SenderForm(forms.ModelForm):

    class Meta:
        model = Sender


class ReceiverForm(forms.ModelForm):

    class Meta:
        model = Receiver

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store

