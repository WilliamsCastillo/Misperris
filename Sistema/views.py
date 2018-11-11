from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Persona, Mascota
from .forms import RegistrarPersonaForm, RegistrarAdminForm, LoginForm, RecuperacionForm, RegistrarMascotaForm, RestablecerForm
from social_django.views import auth, complete, disconnect, _do_login


def index(request):
    plantilla=loader.get_template("index.html")
    return HttpResponse(plantilla.render({'titulo':"Mis Perris"},request))

def home(request):
    return render(request, "index.html")

def registroPersona(request):
    registro=1
    personas=Persona.objects.all()
    form=RegistrarPersonaForm(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        new=User.objects.create_user(data.get("rutPersona"),data.get("mailPersona"),data.get("passwordPersona"))
        new.is_staff=False
        new.save()
        regDB=Persona(user=new,nombrePersona=data.get("nombrePersona"),apellidoPersona=data.get("apellidoPersona"),fechaNacimiento=data.get("fechaNacimiento"),numeroFono=data.get("numeroFono"),regionPersona=data.get("regionPersona"),ciudadPersona=data.get("ciudadPersona"),viviendaPersona=data.get("viviendaPersona"))
        regDB.save()
    form=RegistrarPersonaForm()
    return render(request,"registro.html",{'form':form,'personas':personas,'registro':registro,'titulo':"Registro",})

@login_required(login_url='login')
def registroAdmin(request):
    actual=request.user
    registro=2
    personas=Persona.objects.all()
    form=RegistrarAdminForm(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        new=User.objects.create_user(data.get("rutPersona"),data.get("mailPersona"),data.get("passwordPersona"))
        tipo = data.get("tipoPersona")
        if tipo == '1': 
            new.is_staff=False 
          
            new.is_staff=True
        new.save() 
        regDB=Persona(user=new,nombrePersona=data.get("nombrePersona"),apellidoPersona=data.get("apellidoPersona"),fechaNacimiento=data.get("fechaNacimiento"),numeroFono=data.get("numeroFono"),regionPersona=data.get("regionPersona"),ciudadPersona=data.get("ciudadPersona"),viviendaPersona=data.get("viviendaPersona"),tipoPersona=data.get("tipoPersona"))
        regDB.save()
    form=RegistrarAdminForm()
    return render(request,"registro.html",{'form':form,'personas':personas,'actual':actual,'registro':registro,'titulo':"Registro",})

@login_required(login_url='login')
def registroPerro(request):
    actual=request.user
    perros=Mascota.objects.all()
    form=RegistrarMascotaForm(request.POST, request.FILES)
    if form.is_valid():
        data=form.cleaned_data
        regDB=Mascota(imagen=data.get("imagen"),nombreMascota=data.get("nombreMascota"),razaMascota=data.get("razaMascota"),descripcionMascotra=data.get("descripcionMascotra"),estadoMascota=data.get("estadoMascota"))
        regDB.save()
    form = RegistrarMascotaForm()
    return render(request, "registroPerro.html", {'form': form, 'perros':perros, 'actual':actual,'titulo':"Registro Perro",})


def ingreso(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        user=authenticate(username=data.get("username"),password=data.get("password"))
        if user is not None:
            login(request,user)
            return redirect('/')
    return render(request,'login.html',{'form':form,'titulo':'Login',})

def salir(request):
    logout(request)
    return redirect('/index/')

def olvido(request):
    form=RecuperacionForm(request.POST or None)
    mensaje=""
    if form.is_valid():
        data=form.cleaned_data
        user=User.objects.get(username=data.get("username"))
        send_mail(
                'Recuperación de contraseña',
                'Haga click aquí para ingresar una nueva contraseña',
                'recuperatuclav.2019@gmail.com',
                [user.email],
                html_message = 'Pulse <a href="http://localhost:8000/restablecer?user='+user.username+'">aquí</a>',
            )
        mensaje='Correo Enviado a '+user.email
    return render(request,"olvido.html",{'form':form, 'mensaje':mensaje, 'titulo':"Recuperar Contraseña",})

def restablecer(request):
    form=RestablecerForm(request.POST or None)
    mensaje=""
    try:
        username=request.GET["user"]
    except Exception as e:
        username= None
    if username is not None:
        if form.is_valid():
            data=form.cleaned_data
            if data.get("password_A") == data.get("password_B"):
                mensaje="La contraseña se ha restablecido"
                contra=make_password(data.get("password_B"))
                User.objects.filter(username=username).update(password=contra)
            else:
                mensaje="Las contraseñas no coinciden, ingreselas de"
        return render(request,"restablecer.html",{'form':form, 'username':username, 'mensaje':mensaje, 'titulo':"Restablecer Contraseña",})
    else:
        return redirect('/login/')
