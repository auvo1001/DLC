from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


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