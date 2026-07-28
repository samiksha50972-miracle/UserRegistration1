from django.shortcuts import render
# Create your views here.
from app.forms import *

from app.models import *
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout

from django.urls import reverse

from django.http import HttpResponse,HttpResponseRedirect



@login_required
def changePassword(requset):
    if requset.method=='POST':
        usn=requset.session['username']
        UO=User.objects.get(username=usn)
        npw=requset.POST['npw']
        UO.set_password(npw)
        UO.save()
        return HttpResponse('changed password successfully...')
        

    return render(requset,'changePassword.html')



def resetPassword(request):
    if request.method=='POST':
        newusn=request.POST['newusn']
        print(f'value for post ,{request.POST}')
        LUO=User.objects.filter(username=newusn)
        if LUO:
            UO=LUO[0]
            

            

            return render (request,'resetPassword.html',{'UO':UO})
        else:
            return HttpResponse('User not registerd..')    

    return render(request,'EnterUsername.html')

def save_password(request):
    if request.method =='POST':
        rpwd=request.POST['rpwd']
        username=request.POST['username']
        UO=User.objects.get(username=username)
        UO.set_password(rpwd)
        UO.save()
        return HttpResponse('passwprd reset success')



@login_required
def display_user_details(request):
    if request.session.get('username'):
        username=request.session['username']
        UO=User.objects.get(username=username)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO,'PO':PO}
        return render(request,'display_user_details.html',d)



@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))






def home(request):
    if request.session.get('username'):
        username=request.session['username']
        UO=User.objects.get(username=username)
        d={'UO':UO}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username'] = username

                return HttpResponseRedirect(reverse('home'))
                
            else:
                return HttpResponse('not active user')    
                
        else:
            return HttpResponse('Invalid Credentials...')   
    return render(request,'login_page.html')     

def registration(request):
    if request.method=='POST' and request.FILES:
        NMUMFDO=UserMF(request.POST)
        NMPMFDO=ProfileMF(request.POST,request.FILES)
        if  NMUMFDO.is_valid() and NMPMFDO.is_valid():
            MUMFDO=NMUMFDO.save(commit=False) 
            password=NMUMFDO.cleaned_data['password']
            email=NMUMFDO.cleaned_data['email']
            MUMFDO.set_password(password)
            MUMFDO.save()
            MPMFDO=NMPMFDO.save(commit=False)
            MPMFDO.username=MUMFDO
            MPMFDO.save()
            send_mail('task completition',
                      'congratulation ! your have done completed this task in specific duration',
                            'samiksha.it.aec@gmail.com',
                            [email],
                            fail_silently=False
                      )
            return HttpResponse('registration success')
        else:
            print(NMUMFDO.errors,NMPMFDO.errors)
            return HttpResponse('invalid data')
    EPMFO=ProfileMF()
    EUMFO=UserMF()
    d={'EPMFO':EPMFO,'EUMFO':EUMFO}
    return render(request,'registration.html',d)

