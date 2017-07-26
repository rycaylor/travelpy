from django.shortcuts import render, redirect
from .models import UserManager, User
from django.contrib import messages
# Create your views here.

def index(request):
    try:
        if request.session['logged'] != 0: #functions as a keep me logged in field so if the user may have accidently closed all their tabs they can be redirected to their homepage
            return redirect('travel:index')
        else:
            return render(request, 'login/index.html')
    except:
        return render(request, 'login/index.html')


def register(request):
    try:
        user_valid = User.objects.register(dict(request.POST.items())) #sends the potential user to the models where they get validated
    except:
        request.session['logged']=0
        return redirect('login:index')
    if user_valid['register']: #if the registration returns tru the user is created and greeted
        user = user_valid['user']
        messages.add_message(request, messages.INFO, 'Thanks ' + user.first_name  + ' For Creating An Account')
        return redirect('login:index') #the registered user is redirected to the index rather than being logged in so that if this site is built more i would send an email to the registered user to confirm their account
    else:
        request.session['logged'] = 0
        for error in user_valid['error']: #if registered fields did not pass validation the user is returned with errors of the fields that need to be taken care of
            messages.add_message(request, messages.INFO, error) #
        return redirect('login:index')


def login(request):
    try:
        user_valid = User.objects.login(dict(request.POST.items())) #takes login fields and passes them to the models to be validated
    except:
        request.session['logged'] = 0
        return redirect('login:index')
    if user_valid['login']: #if the user has supplied the correct fields they are sent to the home page
        user = user_valid['user']
        request.session['logged'] = user.id
        return redirect('travel:index')
    else:
        request.session['logged'] = 0
        for error in user_valid['error']: #if the user has supplied incorrect field the user is redirected to the login page with an error
            messages.add_message(request, messages.INFO, error)
        return redirect('login:index')

def logout(request):
    request.session['logged'] = 0 #this session is set to zero as another check
    request.session.flush() #the session is flushed on logout to limit unregistered users
    return redirect('login:index')
