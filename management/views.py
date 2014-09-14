import datetime
import StringIO
import os
from itertools import chain
from operator import attrgetter
from decimal import Decimal


from django.utils import timezone
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db.models import Count, Min, Sum, Avg

from management.forms import SenderCreateForm, ReceiverCreateForm, PackageCreateForm, StoreForm
from management.models import Sender, Receiver, Package, Store, Tinh

from PyPDF2 import PdfFileWriter, PdfFileReader

from reportlab.pdfgen import canvas
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def pdf_test(request):

    #get package
    package = Package.objects.get(id =1)
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 12, None)
    #convert to string and draw each attributes. x,y cartesian from bottom left
    #sender
    p_s_fullname = str(package.p_sender.s_fullname())
    can.drawString(0.75*inch, 8.80*inch, p_s_fullname)
    p_s_address1 = str(package.p_sender.s_address1)
    can.drawString(0.75*inch, 8.30*inch, p_s_address1)
    p_s_address2 = str(package.p_sender.s_address2)
    can.drawString(0.75*inch, 8*inch, p_s_address2)
    p_s_city = str(package.p_sender.s_city)
    can.drawString(4*inch, 8.3*inch, p_s_city)
    p_s_state_province = str(package.p_sender.s_state_province)
    can.drawString(4*inch, 7.9*inch, p_s_state_province)
    p_s_zip = str(package.p_sender.s_zip)
    can.drawString(3.75*inch, 7.40*inch, p_s_zip)
    p_s_phone = str(package.p_sender.s_phone)
    can.drawString(0.75*inch, 7.40*inch, p_s_phone)

    #receiver
    p_r_fullname = str(package.p_receiver.r_fullname())
    can.drawString(0.75*inch, 7*inch, p_r_fullname)
    p_r_address1 = str(package.p_receiver.r_address1)
    can.drawString(0.75*inch, 6.5*inch, p_r_address1)
    p_r_address2 = str(package.p_receiver.r_address2)
    can.drawString(0.75*inch, 6.5*inch, p_r_address2)
    p_r_quan_huyen = str(package.p_receiver.r_quan_huyen)
    can.drawString(3.75*inch, 6.5*inch, p_r_quan_huyen)
    p_r_tinh_thanhpho = str(package.p_receiver.r_tinh_thanhpho)
    can.drawString(3.75*inch, 6*inch, p_r_tinh_thanhpho)
    p_r_phone1 = str(package.p_receiver.r_phone1)
    can.drawString(0.75*inch, 5.5*inch, p_r_phone1)
    p_r_phone2 = str(package.p_receiver.r_phone2)
    can.drawString(3.75*inch, 5.5*inch, p_r_phone2)

    #package
    p_piece = str(package.p_piece)
    can.drawString(7.5*inch, 8.75*inch, p_piece)
    p_weight = str(package.p_weight)
    can.drawString(7.5*inch, 8*inch, p_weight)
    p_value = str(package.p_value)
    can.drawString(6*inch, 7*inch, p_value)
    p_extra_charge = str(package.p_extra_charge)
    can.drawString(7.5*inch, 7.3*inch, "$ " +   p_extra_charge)
    p_subtotal = str(package.subtotal())
    can.drawString(7*inch, 6.5*inch,"$ " + p_subtotal)
    p_receiver2 = str(package.p_receiver2)
    can.drawString(6*inch, 6*inch, p_receiver2)
    p_phone2 = str(package.p_phone2)
    can.drawString(6*inch, 5.5*inch, p_phone2)
    p_added = str(datetime.datetime.date(package.p_added))
    can.drawString(3.25*inch, 0.45*inch, p_added)

    if package.p_type_field == "Door To Door":
        can.drawString(5.5*inch, 8.5*inch, "X")
    elif package.p_type_field == "Air To Air":
        can.drawString(5.5*inch, 8*inch, "X")

    p_content = str(package.p_content)
    textobject = can.beginText(0.5*inch, 4.75*inch)

    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)


    can.drawText(textobject)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file("management/DLC_Form.pdf", "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file
    outputStream = file("management/destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    return HttpResponse(p_content)

def index(request):
    context = RequestContext(request)
    context_dict = {}
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    y_p = Package.objects.filter(p_added__contains=yesterday) #yesterday_package
    y_p_d = y_p.filter(p_type_field="Door To Door") #yesterday_package_door
    y_p_d_w = y_p_d.aggregate(Sum('p_weight')) # yesterday_package_door_weight
    y_p_t = sum(Decimal(package.subtotal())  for package in y_p) #yesterday_package_total
    y_p_a = y_p.filter(p_type_field="Air To Air") #yesterday_package_air
    y_p_a_w = y_p_a.aggregate(Sum('p_weight')) # yesterday_package_air_weight


    context_dict['y_p']=y_p
    context_dict['y_p_d']=y_p_d
    context_dict['y_p_a']=y_p_a
    context_dict['y_p_d_w']=y_p_d_w
    context_dict['y_p_a_w']=y_p_a_w
    context_dict['y_p_t']=y_p_t

    t_p = Package.objects.filter(p_added__contains=datetime.date.today()) #today_package
    t_p_d = t_p.filter(p_type_field="Door To Door") #today_package_door
    t_p_d_w = t_p_d.aggregate(Sum('p_weight')) # today_package_door_weight
    t_p_t = sum(Decimal(package.subtotal())  for package in t_p) #today_package_total
    t_p_a = t_p.filter(p_type_field="Air To Air") #today_package_air
    t_p_a_w = t_p_a.aggregate(Sum('p_weight')) # today_package_air_weight
    context_dict['t_p']=t_p
    context_dict['t_p_d']=t_p_d
    context_dict['t_p_a']=t_p_a
    context_dict['t_p_d_w']=t_p_d_w
    context_dict['t_p_a_w']=t_p_a_w
    context_dict['t_p_t']=t_p_t



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
            receiver = Receiver.objects.filter(package__p_receiver__r_phone1=receiver_phone).distinct()
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
            sender = Sender.objects.filter(package__p_sender__s_phone=sender_phone).distinct()
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

@login_required
def report_lab(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
    context_dict ={}

    package = Package.objects.get(id=3)
    context_dict['package'] = package
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(300, 300, str(context_dict))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

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




def daily_report(request):
    error = False
    context_dict ={}
    if 'from_date' and 'to_date' in request.GET:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        if not from_date:
            error = True
        else:
            context_dict['to_date'] = to_date
            context_dict['from_date'] = from_date
            package = Package.objects.filter(Q(p_added__gt=from_date)
                                                  &
                                                Q(p_added__lt=to_date)
                                                )

            context_dict['package'] = package
            return render(request, 'management/daily_report_result.html', context_dict)
    context_dict['error']= error
    return render(request, 'management/date_report_form.html', context_dict)


def display_not_shipped_package(request):
    context_dict ={}
    package = Package.objects.filter(p_status__icontains = "bat dau")
    # if package.p_piece >=1:
    #     context_dict['package'] = package
    #
    context_dict['package'] = package
    return render(request, 'management/not_ship_package.html', context_dict)


def print_receipt(request,package_url):

    context_dict={}
    context_dict['package_url'] = package_url
    context = RequestContext(request)


    #get package
    package = Package.objects.get(id__iexact =package_url)
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 12, None)
    #convert to string and draw each attributes. x,y cartesian from bottom left
    #sender
    p_s_fullname = str(package.p_sender.s_fullname())
    can.drawString(0.75*inch, 8.80*inch, p_s_fullname)
    p_s_address1 = str(package.p_sender.s_address1)
    can.drawString(0.75*inch, 8.30*inch, p_s_address1)
    p_s_address2 = str(package.p_sender.s_address2)
    can.drawString(0.75*inch, 8*inch, p_s_address2)
    p_s_city = str(package.p_sender.s_city)
    can.drawString(4*inch, 8.3*inch, p_s_city)
    p_s_state_province = str(package.p_sender.s_state_province)
    can.drawString(4*inch, 7.9*inch, p_s_state_province)
    p_s_zip = str(package.p_sender.s_zip)
    can.drawString(3.75*inch, 7.40*inch, p_s_zip)
    p_s_phone = str(package.p_sender.s_phone)
    can.drawString(0.75*inch, 7.40*inch, p_s_phone)

    #receiver
    p_r_fullname = str(package.p_receiver.r_fullname())
    can.drawString(0.75*inch, 7*inch, p_r_fullname)
    p_r_address1 = str(package.p_receiver.r_address1)
    can.drawString(0.75*inch, 6.5*inch, p_r_address1)
    p_r_address2 = str(package.p_receiver.r_address2)
    can.drawString(0.75*inch, 6.5*inch, p_r_address2)
    p_r_quan_huyen = str(package.p_receiver.r_quan_huyen)
    can.drawString(3.75*inch, 6.5*inch, p_r_quan_huyen)
    p_r_tinh_thanhpho = str(package.p_receiver.r_tinh_thanhpho)
    can.drawString(3.75*inch, 6*inch, p_r_tinh_thanhpho)
    p_r_phone1 = str(package.p_receiver.r_phone1)
    can.drawString(0.75*inch, 5.5*inch, p_r_phone1)
    p_r_phone2 = str(package.p_receiver.r_phone2)
    can.drawString(3.75*inch, 5.5*inch, p_r_phone2)

    #package
    p_piece = str(package.p_piece)
    can.drawString(7.5*inch, 8.75*inch, p_piece)
    p_weight = str(package.p_weight)
    can.drawString(7.5*inch, 8*inch, p_weight)
    p_value = str(package.p_value)
    can.drawString(6*inch, 7*inch, p_value)
    p_extra_charge = str(package.p_extra_charge)
    can.drawString(7.5*inch, 7.3*inch, "$ " +   p_extra_charge)
    p_subtotal = str(package.subtotal())
    can.drawString(7*inch, 6.5*inch,"$ " + p_subtotal)
    p_receiver2 = str(package.p_receiver2)
    can.drawString(6*inch, 6*inch, p_receiver2)
    p_phone2 = str(package.p_phone2)
    can.drawString(6*inch, 5.5*inch, p_phone2)
    p_added = str(datetime.datetime.date(package.p_added))
    can.drawString(3.25*inch, 0.45*inch, p_added)

    if package.p_type_field == "Door To Door":
        can.drawString(5.5*inch, 8.5*inch, "X")
    elif package.p_type_field == "Air To Air":
        can.drawString(5.5*inch, 8*inch, "X")

    p_content = str(package.p_content)
    # p_content.replace('\r\n','xxooxx')
    textobject = can.beginText(0.5*inch, 4.75*inch)
   #simple but got problem with p_content, this code breaks into each lines but does not get rid of the black rectangle yet

    for c in p_content:
        if c == '\n':
            textobject.textLine()
        elif c == '\r':
            pass # do nothing
        else:
            textobject.textOut(c)


    can.drawText(textobject)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file("management/DLC_Form.pdf", "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file

    filename ="Receipt"+package_url+".pdf"
    filedir = "media/receipts/"
    filepath = os.path.join( MEDIA_ROOT, filedir, filename )


    outputStream = file(filepath, "wb") #need to change if there are multiple stores

    output.write(outputStream)
    outputStream.close()

    pdf=open(filepath)
    response = HttpResponse(pdf.read(),content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response
    # response = HttpResponse(pdf.read(), mimetype='application/pdf')
    # response['Content-Disposition'] = 'attachment;filename=' + filename
    # pdf.closed
    # return response
    # return HttpResponse('complete')

