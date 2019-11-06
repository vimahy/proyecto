# encoding=utf8
from __future__ import unicode_literals
import datetime
import re
import sys  
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import ChoiceField
from django.contrib import auth
from django.contrib.auth import get_user_model

from account.conf import settings
from account.hooks import hookset
from account.models import EmailAddress, Domicilio,Division, Account
from account.utils import get_user_lookup_kwargs
from .models import DomicilioProfesional

from django.forms import widgets




alnum_re = re.compile(r"^\w+$")


CALIDAD_OPCIONES=(('T','Titular'),('E','Estudiante'))
SEXO_OPCIONES = (('', '-------'),('H','Hombre'),('M','Mujer'),('N','No binario'))


OPCIONES_DOMICILIO = (
            ('PRO', 'Domicilio profesional'),
            ('PAR', 'Domicilio Particular'),
            ('NO', 'No deseo recibir ninguna publicación'),
            )


OPCIONES_GRADO = (
            ('', '-------'),
            ('Lic.', 'Licenciatura'),
            ('M.', 'Maestría'),
            ('Dr.', 'Doctorado'),
            )
OPCIONES_PUBLICACIONES = (
            ('1', 'Boletín'),
            ('2', 'Cd_catalogo'),
            )

OPCIONES_PRIORIDAD = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            )

OPCIONES_OCUPACION = (
            ('', '------------'),
            ('INVESTIGADOR', 'Investigador/Profesor'),	
            ('ESTUDIANTE', 'Estudiante'),
            ('PROFESIONISTA', 'Profesionista')
            )

OPCIONES_DIVISION = (
        ('1', 'ASTROFÍSICA'),
        ('2', 'DINAMICA DE FLUIDOS'),
        ('3', 'ESTADO SÓLIDO'),
        ('4', 'FÍSICA ATÓMICA Y MOLECULAR'),
        ('5', 'FÍSICA DE RADIACIONES'),
        ('6', 'FÍSICA MÉDICA'),
        ('7', 'FÍSICA NUCLEAR'),
        ('8', 'GRAVITACIÓN Y FÍSICA MATEMÁTICA'),
        ('9', 'INFORMACIÓN CUÁNTICA'),
        ('10','NANOCIENCIAS Y NANOTECNOLOGÍA'),
        ('11', 'ÓPTICA'),
        ('12','PARTÍCULAS Y CAMPOS'),
        ('13','PLASMAS'),
        ('14','RAYOS COSMICOS'),
        ('15','TERMODINÁMICA Y FÍSICA ESTADÍSTICA'),
        ('16', 'DIVISIÓN REGIONAL DE SAN LUIS POTOSI'),
        ('17', 'DIVISIÓN REGIONAL DE PUEBLA'),
        ('18', 'DIVISIÓN REGIONAL TABASCO'),
        )

OPCIONES_ESTADOS =(
        ('AGUASCALIENTES', 'AGUASCALIENTES'),
        ('BAJA CALIFORNIA', 'BAJA CALIFORNIA'),
        ('BAJA CALIFORNIA SUR', 'BAJA CALIFORNIA SUR'),
        ('CAMPECHE', 'CAMPECHE'),
        ('CHIAPAS', 'CHIAPAS'),
        ('CHIHUAHUA', 'CHIHUAHUA'),
        ('CIUDAD DE MÉXICO', 'CIUDAD DE MÉXICO'),
        ('COAHUILA', 'COAHUILA'),
        ('COLIMA', 'COLIMA'),
        ('DURANGO','DURANGO'),
        ('GUANAJUATO', 'GUANAJUATO'),
        ('GUERRERO','GUERRERO'),
        ('HIDALGO','HIDALGO'),
        ('JALISCO','JALISCO'),
        ('MÉXICO','MÉXICO'),
        ('MICHOACÁN', 'MICHOACÁN'),
        ('MORELOS', 'MORELOS'),
        ('NAYARIT', 'NAYARIT'),
        ('NUEVO LEÓN', 'NUEVO LEÓN'),
        ('OAXACA', 'OAXACA'),
        ('PUEBLA', 'PUEBLA'),
        ('QUERÉTARO', 'QUERÉTARO'),
        ('QUINTANA ROO', 'QUINTANA ROO'),
        ('SAN LUIS POTOSÍ', 'SAN LUIS POTOSÍ'),
        ('SINALOA', 'SINALOA'),
        ('SONORA', 'SONORA'),
        ('TABASCO', 'TABASCO'),
        ('TAMAULIPAS','TAMAULIPAS'),
        ('TLAXCALA', 'TLAXCALA'),
        ('VERACRUZ','VERACRUZ'),
        ('YUCATÁN','YUCATÁN'),
        ('ZACATECAS','ZACATECAS'),
        )


class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.PasswordInput(render_value=False))
        self.strip = kwargs.pop("strip", True)
        super(PasswordField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return ""
        value = force_text(value)
        if self.strip:
            value = value.strip()
        return value


class SignupForm(forms.Form):

    username = forms.CharField(
        label=_("Username"),
        max_length=64,
        widget=forms.TextInput(),
        required=True
    )
    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )
    password_confirm = PasswordField(
        label=_("Password (again)"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )  
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(), required=True)

    """code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )"""
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


class LoginForm(forms.Form):

    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return hookset.get_user_credentials(self, self.identifier_field)


class LoginUsernameForm(LoginForm):

    username = forms.CharField(label=_("Username"), max_length=64)
    authentication_fail_message = _("The username and/or password you specified are not correct.")
    identifier_field = "username"

    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        field_order = ["username", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class LoginEmailForm(LoginForm):

    email = forms.EmailField(label=_("Email"))
    authentication_fail_message = _("The email address and/or password you specified are not correct.")
    identifier_field = "email"

    def __init__(self, *args, **kwargs):
        super(LoginEmailForm, self).__init__(*args, **kwargs)
        field_order = ["email", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class ChangePasswordForm(forms.Form):

    password_current = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_new_confirm"]


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not EmailAddress.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordResetTokenForm(forms.Form):

    password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_confirm"]


class SettingsForm(forms.Form):
    nombre = forms.CharField(
    label='Nombre(s) ',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre(s)'}),
        required=True,)
    #APELLIDO1, APELLIDO 2 ASI LOS NOMBRO RICARDO
    apellido_paterno = forms.CharField(label=_("Apellido 1"),
        widget=forms.TextInput(attrs={'placeholder': 'Apellido 1'}),)
    apellido_materno = forms.CharField(label=_("Apellido 2"),
        widget=forms.TextInput(attrs={'placeholder': 'Apellido 1'}),
        required=False)
    #fecha_nacimiento = forms.DateField(widget=forms.extras.widgets.SelectDateWidget(years=range(1900,2100)),
        #required=False)
    #CORREO ELECTRONICO ES OBLIGATORIO
    email = forms.EmailField(label=_("Email"),
        required=True,
        widget=forms.DateInput(attrs={'placeholder': 'micorreo@ejemplo.com'}),
        help_text = 'A este correo se le enviaran notificaciones')
    #SEXO TAMBIEN ES OBLIGATORIO
    sexo = forms.ChoiceField(label=_("Género"),
        choices = SEXO_OPCIONES,
        required=True,)
    #fotografia = forms.ImageField(required=False)
    grado_academico = forms.ChoiceField(label=_("Último grado academico"),
        choices = OPCIONES_GRADO,
        required=False)
    ocupacion = forms.ChoiceField(label=_("Actualmente soy"),
        choices = OPCIONES_OCUPACION,
        required=False)
    institucion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Institución'}),
        required=False)
    telefono = forms.CharField(
        help_text = '',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),)
    #SELECCIONAR MINIMO 1 MAXIMO 3
    division = forms.MultipleChoiceField(
        label=_("Indique a que divisón o divisiones desea afiliarse"),
        required=True,
    #Esta advertencia mostrarla al PRINCIPIO
        widget=forms.CheckboxSelectMultiple(),
        help_text = 'Minímo 1 máximo 3 divisiones',
        choices = OPCIONES_DIVISION)
    #division2 = forms.ChoiceField(choices=OPCIONES_DIVISION)
    #division3 = forms.ChoiceField(choices=OPCIONES_PRIORIDAD)
    tipo_domicilio = forms.ChoiceField(label=_("Deseo recibir la correspondencia en:"),
        choices = OPCIONES_DOMICILIO,
        required=False)
    publicacion = forms.MultipleChoiceField(
        label=_("Todas las publicaciones se te harán llegar en formato electrónico, sin embargo ¿Cuál de las siguientes quieres recibir en impreso?"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text = '',
        choices = OPCIONES_PUBLICACIONES)

    def clean_division(self):
        value = self.cleaned_data['division']
        if len(value) > 3:
            raise forms.ValidationError("No puedes elegir más de 3 divisiones.")
        return value

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("Un socio ya esta regisrado con este correo."))



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class SocioForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre(s) ',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre(s)'}),
        required=True,)
    apellido_paterno = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}),)
    apellido_materno = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno'}))
    correo_electronico = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Correo Electrónico'}),
        required=False,)
    sexo = forms.ChoiceField(
        choices = SEXO_OPCIONES,
        required=False,)
    grado_academico = forms.ChoiceField(
        choices = OPCIONES_GRADO,
        required=False,
        help_text = 'Último grado obtenido.')
    institucion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Institución'}),)
    publicacion = forms.MultipleChoiceField(
        required=False,
        choices = OPCIONES_PUBLICACIONES,
        help_text = 'Mantenga oprimida la tecla CTRL para seleccionar las publicaciones.')
    calidad = forms.ChoiceField(
        choices = CALIDAD_OPCIONES,
        required=True,)
    fecha_ingreso = forms.DateField(
        required=False,)
    telefono = forms.CharField(
        help_text = '',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),)
    class Meta:
        model = Account
        exclude = ['numero_socio','finado',]


class DomicilioProfAccounForm(forms.ModelForm):
    codigo_institucion = forms.CharField(
        label='Siglas de la institución',
        widget=forms.TextInput(attrs={'placeholder': 'Siglas de la institución'}),
        required=False,)
    dependencia = forms.Field(
        label='Dependencia',
        widget=forms.TextInput(attrs={'placeholder': 'Dependencia'}),
        help_text = '',
        required=False,)
    institucion = forms.Field(
        label='Institución',
        widget=forms.TextInput(attrs={'placeholder': 'Institución'}),
        help_text = '',
        required=False,)
    calle_numero_apartado_postal = forms.Field(
        label='Apartado Postal o Calle y número',
        widget=forms.TextInput(attrs={'placeholder': 'Apartado Postal o Calle y número'}),
        help_text = '',
        required=False,)
    colonia = forms.Field(
        widget=forms.TextInput(attrs={'placeholder': 'Colonia'}),
        help_text = '',
        required=False,)
    codigo_postal = forms.IntegerField(
        label='Código postal',
        widget=forms.TextInput(attrs={'placeholder': 'Código postal'}),    
        required=False,
        initial=0,
        help_text = '')
    municipio_ciudad = forms.Field(
        label='Delegación o Municipio',
        widget=forms.TextInput(attrs={'placeholder': 'Delegación o Municipio'}),
        help_text = '',
        required=False,)
    estado = forms.ChoiceField(label=_("Estado"),
        choices = OPCIONES_ESTADOS,
        required=False)
    telefono = forms.CharField(
        help_text = '',
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        required=False,)
    class Meta:
        model = DomicilioProfesional
        exclude = ['socio']




class DomicilioFormSet(forms.ModelForm):
    calle_numero_apartado_postal = forms.Field(
        label='Apartado Postal o Calle y número',
        widget=forms.TextInput(attrs={'placeholder': 'Apartado Postal o Calle y número'}),    
        required=False,
        help_text = '')
    colonia = forms.Field(
        label='Colonia',
        widget=forms.TextInput(attrs={'placeholder': 'Colonia'}),    
        required=False,
        help_text = '')
    municipio_delegacion = forms.Field(
        label='Delegación o Municipio',
        widget=forms.TextInput(attrs={'placeholder': 'Delegación o Municipio'}),    
        required=False,
        help_text = '')
    codigo_postal = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Código postal'}),    
        required=False,
        help_text = '')
    ciudad = forms.Field(
        label='Ciudad',
        widget=forms.TextInput(attrs={'placeholder': 'Ciudad'}),    
        required=False,
        help_text = '')
    estado = forms.ChoiceField(label=_("Estado"),
        choices = OPCIONES_ESTADOS,
        required=False)
    telefono = forms.Field(	
        widget=forms.TextInput(attrs={'placeholder': 'Telefono'}),    
        required=False,
        help_text = '')
    class Meta:
        domicilioProfesional = forms.ChoiceField(
        #widget=forms.TextInput(attrs={'placeholder': 'Institución'}),
        required=False)
        model = Domicilio
        exclude = ['socio']
