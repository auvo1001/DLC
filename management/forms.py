from django import forms
from django.contrib.admin import widgets
from management.models import Package, Sender, Receiver, Store, User
from django.contrib.auth.models import User
from functools import partial
from django.views.generic.edit import UpdateView

class PackageCreateForm(forms.ModelForm):
    type_choices = [('Door To Door', 'Door To Door',), ('Air To Air', 'Air To Air',)]
    type_field = forms.ChoiceField(widget=forms.RadioSelect(), choices=type_choices)

    class Meta:
        model = Package
        exclude =['receiver','sender','status','insurance','tax']

class PackageStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Package
        exclude =['receiver','sender']


class SenderCreateForm(forms.ModelForm):

    class Meta:
        model = Sender


class ReceiverCreateForm(forms.ModelForm):

    class Meta:
        model = Receiver

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store

