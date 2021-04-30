from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout , login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.mail import send_mail

from .forms import UserCreationForm
#from django.urls import reverse_lazy
#from django.views import generic

# Create your views here.

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('DA:index'))

def register(request):

    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            uname = new_user.username
            pword = request.POST['password1']
            emaill = request.POST['email']
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'], email=emaill)
            login(request, authenticated_user)

            subject = 'welcome to the world'
            message = f'Hi {uname}, thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [emaill, ]
            #send_mail( subject, message, email_from, recipient_list,fail_silently=False )
            return HttpResponseRedirect(reverse('DA:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
