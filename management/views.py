from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.db.models import Q
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
def add_package(request):
    context = RequestContext(request)
    context_dict={}
    tinh_list = get_tinh_list()
    if request.method == 'POST':
        sender_form = SenderCreateForm(request.POST)
        receiver_form = ReceiverCreateForm(request.POST)
        package_form = PackageCreateForm(request.POST)

        if sender_form.is_valid() and receiver_form.is_valid() and package_form.is_valid():
            package_added = package_form.save(commit = False)
            sender_form_phone = sender_form.cleaned_data['s_phone']
            receiver_form_phone = receiver_form.cleaned_data['r_phone1']

            try:
                Sender.objects.get(s_phone__iexact = sender_form_phone)
                sender = Sender.objects.select_for_update().get(s_phone__iexact=sender_form_phone)
                sender_added = sender.save()
                sender_url = sender.s_phone
                package_added.p_sender = sender
            except Sender.DoesNotExist:
                sender_added = sender_form.save(commit = True)
                sender_url = sender_added.s_phone
                package_added.p_sender = sender_added

            try:
                Receiver.objects.get(r_phone1__iexact = receiver_form_phone)
                receiver = Receiver.objects.select_for_update().get(r_phone1__iexact=receiver_form_phone)
                receiver_added = receiver.save()
                receiver_url = receiver.r_phone1
                package_added.p_receiver = receiver
            except Receiver.DoesNotExist:
                receiver_added = receiver_form.save(commit = True)
                receiver_url = receiver_added.r_phone1
                package_added.p_receiver = receiver_added

            package_added = package_form.save(commit = True)
            package_url = package_added.id

            redirect_url = reverse('detail_package', args=(package_url,))
            return HttpResponseRedirect(redirect_url)

        else:
            print  HttpResponse( "%s %s %s %s %s %s" %(str("sender"),sender_form.errors,str("receiver"),receiver_form.errors,str("package"), package_form.errors))
    else:
        sender_form = SenderCreateForm()
        receiver_form = ReceiverCreateForm()
        package_form= PackageCreateForm()

    context_dict['sender_form']= sender_form
    context_dict['receiver_form'] = receiver_form
    context_dict['package_form'] = package_form
    return render_to_response('management/add_package.html', context_dict, context)

    def get_initial(self):
        super(PackageCreateForm, self).get_initial()
        self.p_type_field = {"Door To Door": "Door To Door"}
        return self.p_type_field


@login_required
def reorder_package(request, sender_url, receiver_url):
    context = RequestContext(request)
    context_dict={}
    context_dict['sender_url'] = sender_url
    context_dict['receiver_url'] = receiver_url
    sender = Sender.objects.get(s_phone__iexact=sender_url)
    receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)

    if request.method == 'POST':
        sender_form = SenderCreateForm(request.POST, instance = sender)
        receiver_form = ReceiverCreateForm(request.POST, instance = receiver)
        package_form = PackageCreateForm(request.POST)

        if sender_form.is_valid() and receiver_form.is_valid() and package_form.is_valid():
            sender_edited = sender_form.save()
            sender_url = sender_edited.s_phone

            receiver_edited = receiver_form.save()
            receiver_url = receiver_edited.r_phone1

            package = package_form.save(commit = False)
            package.p_sender = sender_edited
            package.p_receiver = receiver_edited
            package = package_form.save(commit = True)
            package_url = package.id
            context_dict['package_url'] = package_url
            context_dict['package'] = package
            redirect_url = reverse('detail_package',args=(package_url,))
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponse( "%s %s %s %s %s %s" %(str(sender),sender_form.errors,str(receiver),receiver_form.errors,str("halo"), package_form.errors))
    else:
        sender_form = SenderCreateForm(instance=sender)
        receiver_form = ReceiverCreateForm(instance=receiver)
        package_form= PackageCreateForm()

    context_dict['sender'] = sender
    context_dict['receiver'] = receiver

    context_dict['sender_form']= sender_form
    context_dict['receiver_form'] = receiver_form
    context_dict['package_form'] = package_form
    return render_to_response('management/reorder_package.html',  context_dict, context)

@login_required
def detail_sender(request, sender_url):
    context = RequestContext(request)
    context_dict = {}
    try:
        sender = Sender.objects.get(s_phone__iexact=sender_url)
        package = Package.objects.filter(p_sender__s_phone__iexact=sender.s_phone)
        for pack in package:
            receiver_phone = pack.p_receiver.r_phone1
            receiver = Receiver.objects.filter(package__p_receiver__r_phone1=receiver_phone)
            context_dict['receiver'] = receiver
        context_dict['sender'] = sender
        context_dict['sender_url'] = sender.s_phone
        context_dict['package'] = package
    except Sender.DoesNotExist:
        pass

    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        if search_term:
            query = query.strip()
            result_list = run_query(search_term)
            context_dict['result_list'] = result_list
    return render_to_response('management/detail_sender.html', context_dict, context)


@login_required
def detail_receiver(request, receiver_url):
    context = RequestContext(request)
    context_dict = {}
    try:

        receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)
        package = Package.objects.filter(p_receiver__r_phone1__iexact=receiver.r_phone1)
        for pack in package:
            sender_phone = pack.p_sender.s_phone
            sender = Sender.objects.filter(package__p_sender__s_phone=sender_phone)
            context_dict['sender'] = sender
        context_dict['receiver'] = receiver
        context_dict['receiver_url'] = receiver.r_phone1
        context_dict['package'] = package
    except Receiver.DoesNotExist:
#raise error here
        pass
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            query = query.strip()
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('management/detail_receiver.html', context_dict, context)




@login_required
def detail_package(request, package_url):
    context = RequestContext(request)
    context_dict = {}
    context_dict['package_url'] = package_url
    try:
        package = Package.objects.get(id__iexact=package_url)
        sender = Sender.objects.get(s_phone__iexact=package.p_sender.s_phone)
        receiver = Receiver.objects.get(r_phone1__iexact=package.p_receiver.r_phone1)

        context_dict['sender'] = sender
        context_dict['sender_url'] =  sender.s_phone

        context_dict['receiver'] = receiver
        context_dict['receiver_url'] = receiver.r_phone1
        context_dict['package'] = package

    except Package.DoesNotExist:
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
    return render_to_response('management/edit_sender.html',  context_dict, context)


@login_required
def edit_receiver(request , receiver_url):
    context=RequestContext(request)
    receiver = Receiver.objects.get(r_phone1__iexact=receiver_url)

    if request.POST:
        form = ReceiverCreateForm(request.POST, instance=receiver)
        if form.is_valid():
            edited = form.save()
            receiver_url = edited.r_phone1
            redirect_url = reverse('detail_receiver',args=(receiver_url,))
            return HttpResponseRedirect(redirect_url)

    else:
        form = ReceiverCreateForm(instance=receiver)

    context_dict={}
    context_dict['receiver'] = receiver
    context_dict['form']=form
    context_dict['receiver_url'] = receiver_url
    return render_to_response('management/edit_receiver.html',  context_dict, context)


def edit_package(request , package_url):
    context = RequestContext(request)
    context_dict = {}
    context_dict['package_url'] = package_url
    try:
        package = Package.objects.get(id__iexact=package_url)
        sender = Sender.objects.get(s_phone__iexact=package.p_sender.s_phone)
        receiver = Receiver.objects.get(r_phone1__iexact=package.p_receiver.r_phone1)

    except Package.DoesNotExist:
        pass


    if request.method == 'POST':
        sender_form = SenderCreateForm(request.POST, instance = sender)
        receiver_form = ReceiverCreateForm(request.POST, instance = receiver)
        package_form = PackageCreateForm(request.POST, instance = package)

        if sender_form.is_valid() and receiver_form.is_valid() and package_form.is_valid():
            sender_edited = sender_form.save()
            sender_url = sender_edited.s_phone
            context_dict['sender_url'] = sender_url

            receiver_edited = receiver_form.save()
            receiver_url = receiver_edited.r_phone1
            context_dict['receiver_url'] = receiver_url

            package_edited = package_form.save(commit = False)
            package_edited.p_sender = sender_edited
            package_edited.p_receiver = receiver_edited
            package_edited = package_form.save(commit = True)
            package_url = package_edited.id
            context_dict['package_url'] = package_url
            redirect_url = reverse('detail_package',args=(package_url,))
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

    return render_to_response('management/edit_package.html',  context_dict, context)


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


def search(request):
    error = False
    context_dict ={}
    if 'search_term' in request.GET:
        search_term = request.GET['search_term']

        if not search_term:
            error = True
        else:
            context_dict['search_term'] = search_term
            result_list = []
            sender_list = Sender.objects.filter(Q(s_phone__icontains=search_term) |
                                                Q(s_fname__icontains=search_term)|
                                                Q(s_lname__icontains=search_term) |
                                                Q(s_address1__icontains=search_term)|
                                                Q(s_address2__icontains=search_term)|
                                                Q(s_city__icontains=search_term)|
                                                Q(s_state_province__icontains=search_term) |
                                                Q(s_zip__icontains=search_term)|
                                                Q(s_added__icontains=search_term) |
                                                Q(s_email__icontains=search_term)
                                                )
            receiver_list = Receiver.objects.filter(
                                                Q(r_phone1__icontains=search_term) |
                                                Q(r_fname__icontains=search_term)|
                                                Q(r_lname__icontains=search_term) |
                                                Q(r_address1__icontains=search_term)|
                                                Q(r_address2__icontains=search_term)|
                                                Q(r_quan_huyen__icontains=search_term)|
                                                Q(r_phone2__icontains=search_term)|
                                                Q(r_email__icontains=search_term)|
                                                Q(r_added__icontains=search_term)
                                                )

            package_list = Package.objects.filter(
                                                Q(p_content__icontains=search_term) |
                                                Q(p_receiver2__icontains=search_term) |
                                                Q(p_phone2__icontains=search_term)|
                                                Q(p_added__icontains=search_term)|
                                                Q(p_updated__icontains=search_term)|
                                                Q(p_status__icontains=search_term)|
                                                Q(p_type_field__icontains=search_term)
                                                )
            result_list = list(chain(sender_list,receiver_list,package_list))
            context_dict['result_list'] = result_list
            context_dict['sender_list'] = sender_list
            context_dict['receiver_list'] = receiver_list
            context_dict['package_list'] = package_list
            return render(request, 'management/search_results.html', context_dict)
    context_dict['error']= error
    return render(request, 'management/search_form.html', context_dict)