from django.shortcuts import render
# Create your views here.
from app.forms import *



from django.core.mail import send_mail

from django.http import HttpResponse
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

