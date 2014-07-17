from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from management.forms import SenderForm, ReceiverForm, PackageForm, StoreForm
from management.models import Sender, Receiver, Package, Store

def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response ('management/index.html', context_dict, context)


def login_view(request):
    context= RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username , password = password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/management/')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid login details {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('management/login.html', {}, context)


def logout_view(request):
    logout(request)
    return redirect('/management/')

def add_package(request):
    context = RequestContext(request)
    context_dict={}
    senderform =add_sender(request)
    context_dict['sender'] = senderform
    receiverform = add_receiver(request)
    context_dict['receiverform']= receiverform
    return render_to_response('management/add_package.html',context_dict,context)

def add_sender(request):
    context = RequestContext(request)
    context_dict={}
    if request.method =='POST':
        form = SenderForm(request.POST)
        if form.is_valid():
            added = form.save(commit=True)
           # encoded_sender = added.phone
            #return HttpResponseRedirect(reverse('sender_detail', args=(encoded_sender,)))
            return render_to_response('management/login.html',context_dict,context)
        else:
            print form.errors
    else:
        form = SenderForm()
        context_dict['senderform']=form
    return render_to_response('management/add_package.html',context_dict,context)

def add_receiver(request):
    context = RequestContext(request)
    context_dict={}
    if request.method =='POST':
        form = ReceiverForm(request.POST)
        if form.is_valid():
            added = form.save(commit=True)
            encoded_sender = added.phone1
            #return HttpResponseRedirect(reverse('sender_detail', args=(encoded_sender,)))
            return render_to_response('management/add_package.html',context_dict,context)
        else:
            print form.errors
    else:
        form = ReceiverForm()
        context_dict['receiverform']= form
    return render_to_response('management/add_receiver.html',context_dict,context)

def detail_sender(request,sender_url):
    context = RequestContext(request)
    context_dict={}
    context_dict['sender_url'] = sender_url

    try:

        sender = Sender.objects.get(phone__iexact=sender_url)
        context_dict['sender'] =sender

        #trips = Trip.objects.filter(org=organization).order_by('-date')
        #context_dict['trips'] = trips

        #reps = Representative.objects.filter(org=organization)
        #context_dict['reps'] = reps

    except Sender.DoesNotExist:
        pass

    if request.method =='POST':
        query =request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list']=result_list
    return render_to_response('management/detail_sender.html',context_dict, context)

def encode_url(stri):
    return stri.replace(' ', '_')

def decode_url(stri):
    return stri.replace('_', ' ')
