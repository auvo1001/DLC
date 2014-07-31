from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from management.forms import SenderCreateForm, ReceiverCreateForm, PackageCreateForm, StoreForm
from management.models import Sender, Receiver, Package, Store, Tinh


def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('management/index.html', context_dict, context)


def login_view(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

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


@login_required
def add_sender(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'POST':
        form = SenderCreateForm(request.POST)
        if form.is_valid():
            added = form.save(commit=True)
            sender_url = added.s_phone
            return HttpResponseRedirect(reverse('detail_sender', args=(sender_url,)))

        else:
            print form.errors
    else:
        form = SenderCreateForm()
        context_dict['form'] = form
    return render_to_response('management/add_sender.html', context_dict, context)


@login_required
def add_receiver(request, sender_url):
    context = RequestContext(request)
    context_dict = {}
    context_dict['sender_url'] = sender_url
    if request.method == 'POST':
        form = ReceiverCreateForm(request.POST)
        if form.is_valid():
            added = form.save(commit=True)
            receiver_url = added.r_phone1
            redirect_url = reverse('detail_receiver', args=(sender_url, receiver_url,))
            return HttpResponseRedirect(redirect_url)
        else:
            print form.errors
    else:
        form = ReceiverCreateForm()
        context_dict['form'] = form
    return render_to_response('management/add_receiver.html', context_dict, context)


@login_required
def add_package(request, sender_url, receiver_url):
    context = RequestContext(request)
    context_dict = {}
    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url

    if request.method == 'POST':
        form = PackageCreateForm(request.POST)
        if form.is_valid():
            added = form.save(commit=False)
            added.p_sender = Sender.objects.get(s_phone__iexact=sender_url)
            added.p_receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)
            added = form.save(commit=True)
            package_url = added.id
            redirect_url = reverse('detail_package', args=(sender_url, receiver_url, package_url,))

            return HttpResponseRedirect(redirect_url)
        else:
            print form.errors
    else:
        form = PackageCreateForm()

    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url
    context_dict['form'] = form
    return render_to_response('management/add_package.html', context_dict, context)

    def get_initial(self):
        super(PackageCreateForm, self).get_initial()
        self.p_type_field = {"Door To Door": "Door To Door"}
        return self.p_type_field


@login_required
def detail_sender(request, sender_url):
    context = RequestContext(request)
    context_dict = {}
    try:
        sender = Sender.objects.get(s_phone__iexact=sender_url)
        context_dict['sender'] = sender
        context_dict['sender_url'] = sender.s_phone

    except Sender.DoesNotExist:
        pass

    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('management/detail_sender.html', context_dict, context)


@login_required
def detail_receiver(request, sender_url, receiver_url):
    context = RequestContext(request)
    context_dict = {}
    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url
    try:
        sender = Sender.objects.get(s_phone__iexact=sender_url)
        context_dict['sender'] = sender
        context_dict['sender_url'] = sender_url

        receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)
        context_dict['receiver'] = receiver
        context_dict['receiver_url'] = receiver_url

    except Receiver.DoesNotExist or Sender.DoesNotExist:
        pass
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('management/detail_receiver.html', context_dict, context)


@login_required
def detail_package(request, sender_url, receiver_url, package_url):
    context = RequestContext(request)
    context_dict = {}

    try:
        sender = Sender.objects.get(s_phone__iexact=sender_url)
        context_dict['sender'] = sender
        context_dict['sender_url'] = sender_url

        receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)
        context_dict['receiver'] = receiver
        context_dict['receiver_url'] = receiver_url

        package = Package.objects.get(id__iexact=package_url)
        context_dict['package'] = package
        context_dict['package_url'] = package_url
        context_dict['subtotal'] = package.subtotal()

    except Receiver.DoesNotExist:
        pass
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('management/detail_package.html', context_dict, context)


@login_required
def edit_sender(request ,sender_url):
    context=RequestContext(request)
    sender = Sender.objects.get(s_phone__iexact=sender_url)

    if request.POST:
        form = SenderCreateForm(request.POST, instance=sender)
        if form.is_valid():
            edited = form.save()
            sender_url = edited.s_phone
            redirect_url = reverse('detail_sender',args=(sender_url,))
            return HttpResponseRedirect(redirect_url)

    else:
        form = SenderCreateForm(instance=sender)

    context_dict={}
    context_dict['sender'] =sender
    context_dict['form']=form
    context_dict['sender_url'] = sender_url
    return render_to_response('management/edit_sender_form.html',  context_dict, context)


@login_required
def edit_receiver(request , sender_url, receiver_url):
    context=RequestContext(request)
    receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)

    if request.POST:
        form = ReceiverCreateForm(request.POST, instance=receiver)
        if form.is_valid():
            edited = form.save()
            receiver_url = edited.r_phone1
            redirect_url = reverse('detail_receiver',args=(sender_url, receiver_url,))
            return HttpResponseRedirect(redirect_url)

    else:
        form = ReceiverCreateForm(instance=receiver)

    context_dict={}
    context_dict['receiver'] = receiver
    context_dict['form']=form
    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url
    return render_to_response('management/edit_receiver_form.html',  context_dict, context)


def edit_package(request , sender_url, receiver_url, package_url):
    context=RequestContext(request)
    tinh_list = get_tinh_list()
    sender = Sender.objects.get(s_phone__iexact = sender_url)
    receiver = Receiver.objects.get(r_phone1__iexact = receiver_url)
    package = Package.objects.get(id__iexact = package_url)

    if request.POST:
        sender_form = SenderCreateForm(request.POST, instance = sender)
        receiver_form = ReceiverCreateForm(request.POST, instance = receiver)
        package_form = PackageCreateForm(request.POST, instance = package)
        if sender_form.is_valid() and receiver_form.is_valid() and package_form.is_valid():
            sender_edited = sender_form.save()
            sender_url = sender_edited.s_phone

            receiver_edited = receiver_form.save()
            receiver_url = receiver_edited.r_phone1

            package_edited = package_form.save(commit = False)
            package_edited.sender = sender_edited
            package_edited.receiver = receiver_edited
            package_edited = package_form.save(commit = True)
            package_url = package_edited.id

            redirect_url = reverse('detail_package',args=(sender_url, receiver_url, package_url,))
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponse( "%s %s %s %s %s %s" %(str(sender),sender_form.errors,str(receiver),receiver_form.errors,str(package), package_form.errors))
    else:

        sender_form = SenderCreateForm(instance=sender)
        receiver_form = ReceiverCreateForm(instance=receiver)
        package_form= PackageCreateForm(instance=package)

    context_dict={}
    context_dict['sender'] = sender
    context_dict['receiver'] = receiver
    context_dict['package'] = package
    context_dict['sender_form']= sender_form
    context_dict['receiver_form'] = receiver_form
    context_dict['package_form'] = package_form
    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url
    context_dict['package_url'] = package_url

    return render_to_response('management/edit_package_form.html',  context_dict, context)


def encode_url(stri):
    return stri.replace(' ', '_')


def decode_url(stri):
    return stri.replace('_', ' ')


def logout_view(request):
    logout(request)
    return redirect('/management/')


def get_tinh_list(max_results=0, starts_with=''):
        tinh_list=[]
        if starts_with:
            tinh_list = Tinh.objects.filter(name__istartswith=starts_with)
        else:
            tinh_list = Tinh.objects.all()

        if max_results >0:
            if len(tinh_list) >max_results:
                tinh_list - tinh_list[:max_result]
            return tinh_list