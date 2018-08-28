# encoding=utf8
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext as ctx
from django.forms.models import inlineformset_factory
from account.models import Account, DomicilioProfesional,Cuota, Domicilio,PublicacionDevuelta
from django.http import HttpResponseRedirect
from reportlab.pdfgen import canvas
from .forms import SocioForm,UserForm,DomicilioFormSet,CuotaForm,PublicacionDevueltaForm,DomicilioProfesionalForm,DomicilioFormSet
import sys
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save






def xstr(s):
    if s is None:
        return ' '
    return str(s)


reload(sys)  
sys.setdefaultencoding('utf8')


@user_passes_test(lambda u: u.is_staff)
def detalle_socio(request, pk):
    """
    Muestra los datos del socio
    """
    socio = get_object_or_404(Account, pk=pk)
    return render(request, 'sociedad/detalle_socio.html', {'socio': socio})

@user_passes_test(lambda u: u.is_staff)
def detalle_cuota(request, pk):
    """
    Muestra los datos relacionados a la cuota de un socio
    """
    cuota = get_object_or_404(Cuota, pk=pk)
    return render(request, 'sociedad/detalle_cuota.html', {'cuota': cuota})


@user_passes_test(lambda u: u.is_staff)
def cargar_publicacion(request):
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
        if request.method =="POST":
            publicacionDevueltaForm = PublicacionDevueltaForm(request.POST)
            if publicacionDevueltaForm.is_valid():
               publicacionDevuelta = publicacionDevueltaForm.save()
               return redirect(detalle_publicacion, pk=publicacionDevuelta.pk)
        else:
            publicacionDevueltaForm  = PublicacionDevueltaForm ()
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/cargar_publicacionesDevueltas.html', {'publicacionDevueltaForm':publicacionDevueltaForm,})



@user_passes_test(lambda u: u.is_staff)
def cargar_domicilio(request):
    """
    Agrega una dirección profesional a la base de datos
    """
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
        if request.method =="POST":
            domicilioProfesional= DomicilioProfesionalForm(request.POST)
            if domicilioProfesional.is_valid():
               domicilioP = domicilioProfesional.save()
               return redirect(detalle_domicilio, pk=domicilioP.pk)
        else:
            domicilioProfesional  = DomicilioProfesionalForm ()
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/cargar_domicilioP.html', {'domicilioProfesional':domicilioProfesional,})





@user_passes_test(lambda u: u.is_staff)
def detalle_domicilio(request, pk):
    """

    """
    domicilioProfesional = get_object_or_404(DomicilioProfesional, pk=pk)
    return render(request, 'sociedad/detalle_domicilioP.html', {'domicilioProfesional': domicilioProfesional})




@user_passes_test(lambda u: u.is_staff)
def editar_domicilio(request, pk):
    usuario = request.user
    domicilioProfesional = get_object_or_404(DomicilioProfesional, pk=pk)
    if usuario.groups.filter(name='secretaria').exists():
        if request.method == "POST":
            form = DomicilioProfesionalForm(request.POST, instance = domicilioProfesional)
            if form.is_valid():
                form.save()
                return redirect(detalle_domicilio,pk=domicilioProfesional.pk)
        else:
            form = DomicilioProfesionalForm(instance = domicilioProfesional)
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/editar_domicilioP.html',{'form':form})






@user_passes_test(lambda u: u.is_staff)
def detalle_publicacion(request, pk):
    """
    Muestra los datos relacionados a una publicacion que no fue entregada
    """
    publicacion = get_object_or_404(PublicacionDevuelta, pk=pk)
    return render(request, 'sociedad/detalle_publicacionesDevueltas.html', {'publicacion': publicacion})



@user_passes_test(lambda u: u.is_staff)
def editar_publicacion(request, pk):
    usuario = request.user
    publicacionDevuelta = get_object_or_404(PublicacionDevuelta, pk=pk)
    if usuario.groups.filter(name='secretaria').exists():
        if request.method == "POST":
            form = PublicacionDevueltaForm(request.POST, instance = publicacionDevuelta)
            if form.is_valid():
                form.save()
                return redirect(detalle_publicacion,pk=publicacionDevuelta.pk)
        else:
            form = PublicacionDevueltaForm(instance = publicacionDevuelta)
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/editar_publicacion.html',{'form':form})



@user_passes_test(lambda u: u.is_staff)
def cargar_cuota(request):
    """
    Agrega un pago de un socio. 
    """
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
    #if usuario.has_perm('sociedad.add_cuota'):
        if request.method =="POST":
            cuotaForm = CuotaForm(request.POST)
            if cuotaForm.is_valid():
               cuota = cuotaForm.save()
               return redirect(detalle_cuota, pk=cuota.pk)
        else:
            cuotaForm = CuotaForm()
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/cargar_cuota.html', {'cuotaForm':cuotaForm,})



@user_passes_test(lambda u: u.is_staff)
def editar_cuota(request, pk):
    cuota = get_object_or_404(Cuota, pk=pk)
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
        if request.method == "POST":
            form = CuotaForm(request.POST, instance = cuota)
            if form.is_valid():
                form.save()
                return redirect(detalle_cuota,pk=cuota.pk)
        else:
            form = CuotaForm(instance = cuota)
    else:
        return HttpResponse("Permission to add denied")
    return render(request,'sociedad/editar_cuota.html',{'form':form})


@user_passes_test(lambda u: u.is_staff)
def agregar_cuota(request, pk):
    """
    Registra un pago o cuota de un socio
    """
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == "POST":
        form = CuotaForm(request.POST, instance = socio)
        if form.is_valid():
            form.save()
            return redirect(detalle_cuota,pk=cuota.pk)
    else:
        nombre = Socio.objects.get(pk=pk)
        form = CuotaForm(instance = socio)
    return render(request,'sociedad/agregar_cuota.html',{'form':form})




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'sociedad/prueba.html', {'form': form})



@user_passes_test(lambda u: u.is_staff)
def cargar_socio(request):
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
        DomicilioFormSet = inlineformset_factory(Account,Domicilio,fields=('codigo_postal',
                            'calle_numero_apartado_postal',
                            'colonia',
                            'municipio_delegacion',
                            'ciudad',
                            'estado',
                            'telefono')
                            ,can_delete=False)
        socio=Account()
        if request.method == "POST":
            form = SocioForm(request.POST, instance=socio)
            domicilioFormset = DomicilioFormSet(request.POST, instance=socio)
            if form.is_valid() and domicilioFormset.is_valid():
                form.save()
                domicilioFormset.save()
                return redirect(detalle_socio, pk=socio.pk)
        else:
            form = SocioForm(instance=socio)
            domicilioFormset = DomicilioFormSet(instance=socio)
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/cargar_socio.html', {'form':form,'domicilioFormset':domicilioFormset})

#Este pedazo de codigo es para crear el formulario de crear un socio nuevo
#def create_profile(sender, **kwargs):
#    user = kwargs["instance"]
#    if kwargs["created"]:
#        user_profile = Account(user=user)
#        user_profile.save()
#post_save.connect(create_profile, sender=User)



@user_passes_test(lambda u: u.is_staff)
def cargar_cuota(request):
    """
    Agrega un pago de un socio. 
    """
    usuario = request.user
    if usuario.groups.filter(name='secretaria').exists():
    #if usuario.has_perm('sociedad.add_cuota'):
        if request.method =="POST":
            cuotaForm = CuotaForm(request.POST)
            if cuotaForm.is_valid():
               cuota = cuotaForm.save()
               return redirect(detalle_cuota, pk=cuota.pk)
        else:
            cuotaForm = CuotaForm()
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/cargar_cuota.html', {'cuotaForm':cuotaForm,})


@login_required() # only logged in users should access this
def editar_socio(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)
    usuario = request.user
    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)
    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User,Account , fields=( 'apellido_materno','sexo',
        'grado_academico','institucion','publicacion','calidad','telefono','division'),can_delete=False)
    formset = ProfileInlineFormset(instance=user)
    if usuario.groups.filter(name='secretaria').exists():
        if request.user.is_authenticated(): #and request.user.id == user.id:
            if request.method == "POST":
                form = UserForm(request.POST, request.FILES, instance=user)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    created_user = form.save(commit=False)
                    formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                    if formset.is_valid():
                        created_user.save()
                        formset.save()
                        #return redirect(detalle_cuota,pk=cuota.pk)
                        return redirect(detalle_socio,pk)
    else:
        return HttpResponse("Permission to add denied")
    return render(request, 'sociedad/editar_socio.html', {'formset': formset,'user_form':user_form})



#@permission_required('polls.can_vote')
#@user_passes_test(lambda u: u.is_staff)
#def editar_socio(request, pk):
#    DomicilioFormSet = inlineformset_factory(Account,Domicilio,fields=('codigo_postal',
#                        'calle_numero_apartado_postal',
#                        'colonia',
#                        'municipio_delegacion',
#                        'ciudad_y_estado',
#                        'telefono'),
#                         can_delete=False)
#    socio = get_object_or_404(Account, pk=pk)
#    if request.method == "POST":
#        form = SocioForm(request.POST, instance=socio)
#        domicilioFormset = DomicilioFormSet(request.POST, instance=socio)
#        if form.is_valid() and domicilioFormset.is_valid():
#            form.save()
#            domicilioFormset.save()
#            return redirect(detalle_socio, pk=socio.pk)
#    else:
#        form = SocioForm(instance=socio)
#        domicilioFormset = DomicilioFormSet(instance=socio)
#    return render(request, 'sociedad/editar_socio.html', {'form': form,'domicilioFormset':domicilioFormset})



@user_passes_test(lambda u: u.is_staff)
def lista_cuotas(request, pk):
    """
    Lista los pagos de un socio
    """
    socio = get_object_or_404(Account, pk=pk)
    cuotas = socio.cuota_set.order_by('-id')
    return render(request, 'sociedad/lista_cuotas.html', {'cuotas': cuotas,'socio':socio})

@user_passes_test(lambda u: u.is_staff)
def tarjetas(request):
    """Realiza busquedas de socios.
    """
    codigos = DomicilioProfesional.objects.all()
    total = Account.objects.latest('pk').pk
    errors = []
    # Busca a los socios por las siglas de su institucion
    if 'i' in request.GET:
        i = request.GET['i']
        if not i:
            errors.append('Ingrese un domicilio profesional')
        elif len(i) > 62:
            errors.append('Ingresa menos de 20 caracteres')
        else:
            institucion = Account.objects.filter(institucion__icontains=i).order_by('-apellido_materno')
            print(institucion)
            return render(request, 'sociedad/tarjetas.html',
                {'institucion': institucion, 'query': i})





    # Busca un socio por su número
    # Falta arreglar las excepciones. Si se 
    # busca un socio por numero que no existe o no se ingresa algun valor
    if 'q' in request.GET:
        try:
            q = request.GET['q']
            numero = Account.objects.get(numero_socio=q)
        except (Account.DoesNotExist, ValueError):
            numero = None
        return render(request, 'sociedad/tarjetas.html',
            {'numero': numero, 'query': q,'codigos':codigos})

    #SIRVE
    # Hace una búsqueda de socios por nombre, apellido paterno y apellido materno
    elif 'n' in request.GET:
        n = request.GET['n']
        if not n:
            errors.append('Ingrese un nombre o apellido')
            print('ingrese un nombre')
        if len(n) > 62:
            errors.append('Ingresa menos de 20 caracteres')
        else:
            socios = User.objects.annotate(
                search=SearchVector('first_name', 'last_name'),
            ).filter(search=n)
            print(socios)
            return render(request, 'sociedad/tarjetas.html',
                {'socios': socios, 'query': n,'codigos':codigos})




    # Hace una búsqueda de socios por nombre
    #elif 'n' in request.GET:
     #   n = request.GET['n']
      #  if not n:
       #     errors.append('Ingrese un nombre o apellido')
        #    print('ingrese un nombre')
        #if len(n) > 20:
         #   errors.append('Ingresa menos de 20 caracteres')
          #  print ('Ingresa menos de 20 caracteres')
       # else:
        #    socios = User.objects.filter(first_name__icontains=n).order_by('last_name','account__apellido_materno').reverse()
         #   print(socios)
          #  return render(request, 'sociedad/tarjetas.html',
           #     {'socios': socios, 'query': n,'codigos':codigos})


    # Hace una búsqueda de socios por apellido paterno
    elif 'ap' in request.GET:
        ap = request.GET['ap']
        if not ap:
            errors.append('Ingrese un apellido paterno')
            print('ingrese un apellido paterno')
        if len(ap) > 62:
            errors.append('Ingresa menos de 62 caracteres')
        else:
            paternos = User.objects.filter(last_name__icontains=ap).order_by('-last_name')
            print(paternos)
            return render(request, 'sociedad/tarjetas.html',
                {'paternos': paternos, 'query': ap})


    # Hace una búsqueda de socios por apellido materno
    elif 'am' in request.GET:
        am = request.GET['am']
        if not am:
            errors.append('Ingrese un apellido materno')
            print('ingrese un apellido materno')
        if len(am) > 62:
            errors.append('Ingresa menos de 62 caracteres')
        else:
            usuarios = Account.objects.filter(apellido_materno__icontains=am
            )
            print(usuarios)
            return render(request, 'sociedad/tarjetas.html',
                {'usuarios': usuarios, 'query': am})



    # Sirve
    # Hace una búsqueda de socios por perido de cuotas
    elif 'inicio' and 'fin' in request.GET:
        inicio = request.GET['inicio']
        fin = request.GET['fin']
        if not inicio:
            errors.append('Ingrese una fecha valida')
        elif not fin:
            errors.append('Ingrese una fecha valida')
        else:
            cuota = Account.objects.filter(cuota__fecha_fin__range=[inicio,fin]).distinct()
            #PAra obtener un query set de la consulta anterior
            return render(request, 'sociedad/tarjetas.html',
                {'cuota': cuota, 'codigos':codigos,'inicio':inicio,'fin':fin},)

    # sirve
    # Busca a los socios cuyas cuotas estan vigentes.
    elif 'vigente' in request.GET:
        vigente = request.GET['vigente']
        hoy = datetime.date.today()
        cuota= Account.objects.filter(cuota__fecha_fin__gte=hoy).distinct()
        
        #socios=Socio.objects.filter(socio_id__in=cuota)
        print(cuota)
        return render(request, 'sociedad/tarjetas.html',
            {'cuota':cuota, 'query': vigente,'codigos':codigos})

    context = {'errors': errors,'codigos':codigos}


    return render(request, 'sociedad/tarjetas.html',context)
