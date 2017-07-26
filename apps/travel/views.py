# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login.models import User
from django.contrib import messages
from .models import Trip

# Create your views here.
def index(request):
    if 'logged' not in request.session: #checking to see if the session data of logged created in login blocking thos who dont register to the login index
        return redirect('login:index')
    else:
        context = {
                    'user': User.objects.get(id=int(request.session['logged'])),
                    'trips': Trip.objects.all()
                }
        return render(request, 'travel/index.html', context)


def add(request):
    if 'logged' not in request.session:
        return redirect('login:index')
    return render(request, 'travel/add.html')

def make_plan(request):
    if 'logged' not in request.session:
        return redirect('login:index')
    user = int(request.session['logged'])
    plan_valid = Trip.objects.plan_make(dict(request.POST.items()), user) #passes post data collected from the form and sends it to be validated in my models function
    if plan_valid['create']: #if the plan is created redirects the user back to the homepage with a thank you message
        plan = plan_valid['plan']
        messages.add_message(request, messages.INFO, 'Thanks for adding, ' + plan.destination  + ',  To your planned trips')
        return redirect('travel:index')
    else:
        for error in plan_valid['error']: #if the user has entered any of the fields incorrectly then they are redirected to the adding page again where they can attempt to complete the form
            messages.add_message(request, messages.INFO, error)#messages to let them know where the errors have occured
        return redirect('travel:add')


def trip(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    trip = Trip.objects.get(id=id) #grabs the trip id from the anchor tag

    context = {
        'logged': User.objects.get(id=int(request.session['logged'])),
        'trip' : trip,
        'users' : User.objects.all()
    }
    return render(request, 'travel/trip.html', context)


def join(request, id):
    if 'logged' not in request.session:
        return redirect('login:index')
    trip = id
    user = int(request.session['logged'])
    join_trip = Trip.objects.join_trip(user, trip)#this grabs the current user that has logged in and the corresponding trip they would like to join and adds them to the trip

    return redirect('travel:index')
