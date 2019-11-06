# encoding=utf8
import datetime
from django.forms import MultiWidget
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.db import models
from account.models import Account,Division, Domicilio, Cuota, PublicacionDevuelta, DomicilioProfesional,PublicacionDevuelta
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


dateTimeOptions = {
'format': 'dd/mm/yyyy',
'autoclose': True,
'showMeridian' : True
}
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

SEXO_OPCIONES = (('', '-------'),('H','Hombre'),('M','Mujer'),('N','No binario'))
CALIDAD_OPCIONES=(('T','Titular'),('E','Estudiante'))
OPCIONES_PUBLICACIONES = (
            ('3', 'Revista'),
            ('1', 'Boletín'),
            ('2', 'Cd_catalogo'),
            ('4', 'Calendario')
            )
OPCIONES_GRADO = (
            ('', '-------'),
            ('Lic.', 'Licenciatura'),
            ('M.', 'Maestría'),
            ('Dr.', 'Doctorado'),
            )


OPCIONES_DOMICILIO = (
            ('', '-------'),
            ('PROFESIONAL', 'PROFESIONAL'),
            ('PARTICULAR', 'PARTICULAR'),
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class SocioForm(forms.ModelForm):
    #nombre = forms.CharField(
        #label='Nombre(s) ',
        #widget=forms.TextInput(attrs={'placeholder': 'Nombre(s)'}),
        #required=True,)
    #apellido_paterno = forms.CharField(
        #widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}),)
    apellido_materno = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno'}))
    #correo_electronico = forms.EmailField(
        #widget=forms.TextInput(attrs={'placeholder': 'Correo Electrónico'}),
        #required=False,)
    sexo = forms.ChoiceField(
        choices = SEXO_OPCIONES,
        required=False,)
    grado_academico = forms.ChoiceField(
        choices = OPCIONES_GRADO,
        required=False,
        help_text = 'Último grado obtenido.')
    institucion = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Institución'}),
        required=False,)
    tipo_domicilio = forms.MultipleChoiceField(
        required=True,
        choices = OPCIONES_DOMICILIO,
        help_text = 'Mantenga oprimida la tecla CTRL para seleccionar las publicaciones.')
    publicacion = forms.MultipleChoiceField(
        required=False,
        choices = OPCIONES_PUBLICACIONES,
        help_text = 'Mantenga oprimida la tecla CTRL para seleccionar las publicaciones.')
    calidad = forms.ChoiceField(
        choices = CALIDAD_OPCIONES,
        required=True,)
    fecha_ingreso = forms.DateField()
    telefono = forms.CharField(
        help_text = '',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),)
    class Meta:
        model = Account
        exclude = ['numero_socio','finado','user']



class PublicacionDevueltaForm(forms.ModelForm):
    fecha_envio = forms.DateField(
    label='Fecha de envio',
    widget=forms.TextInput(attrs={'placeholder': 'AAAA-MM-DD'}),    
        required=True,
    help_text = 'Ingrese la fecha en la que fue enviada la publicación.')
    class Meta:
        model = PublicacionDevuelta
        fields ='__all__'


class DomicilioFormSet(forms.ModelForm):
    class Meta:
        model = Domicilio
        exclude = ['socio']

hoy = datetime.date.today()

class CuotaForm(forms.ModelForm):
    fecha_pago =forms.DateField(initial=hoy,
    label='Fecha de vencimiento',
        localize=True,
        input_formats=['%d-%m-%Y','%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'}),    
        required=True,
    help_text = 'Ingrese la fecha de vencimiento.'
    )
    fecha_fin = forms.DateField(initial=hoy.replace(hoy.year + 1),
        label='Fecha de vencimiento',
        localize=True,
        input_formats=['%d-%m-%Y','%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'}),    
        required=True,
    help_text = 'Ingrese la fecha de vencimiento.'
    )
    numero_factura = forms.Field(
    widget=forms.TextInput(attrs={'placeholder': 'xxxxxxxxx'}),    
        required=False,
    help_text = 'Ingrese el código de la factura.')
    cantidad = models.FloatField(null=True,
        blank =True,
        validators = [MinValueValidator(0.0), MaxValueValidator(10000000)],)
    class Meta:
        model = Cuota
        fields = '__all__'

class DomicilioProfesionalForm(forms.ModelForm):
    codigo_institucion = forms.CharField(
        label='Código de la institución',
        widget=forms.TextInput(attrs={'placeholder': 'Código para la institución'}),
        help_text = 'Asigne un código',
        required=False,)
    codigo_postal = forms.Field(
        widget=forms.TextInput(attrs={'placeholder': 'Código'}),    
        required=False,
        help_text = '')
    institucion = forms.Field(
        widget=forms.TextInput(attrs={'placeholder': 'Institución'}),
        required=False,
        help_text = '')
    dependencia = forms.Field(
        widget=forms.TextInput(attrs={'placeholder': 'Dependencia'}),
        required=False,
        help_text = '')
    calle_numero_apartado_postal = forms.Field(
        label='Calle, número y apartado postal',
        widget=forms.TextInput(attrs={'placeholder': ''}),
        required=False,
        help_text = 'Escriba la calle y el número o en su caso el aparatdo postal')
    colonia = forms.Field(
        widget=forms.TextInput(attrs={'placeholder': 'Colonia'}),
        required=False,
        help_text = '')
    municipio_ciudad = forms.Field(
        label='Estado, municipio y ciudad',
        widget=forms.TextInput(attrs={'placeholder': 'Municipio y ciudad'}),
        required=False,
        help_text = '')
    estado = forms.ChoiceField(
        choices = OPCIONES_ESTADOS,
        required=True,)
    telefono = forms.CharField(
        help_text = '',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}),)
    class Meta:
        model = DomicilioProfesional
        fields ='__all__'
