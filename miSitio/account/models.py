# encoding=utf8
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
import operator

try:
    from urllib.parse import urlencode
except ImportError:  # python 2
    from urllib import urlencode

from django.urls import reverse
from django.db import models, transaction
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone, translation, six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site

import pytz

from account import signals
from account.conf import settings
from account.hooks import hookset
from account.managers import EmailAddressManager, EmailConfirmationManager
from account.signals import signup_code_sent, signup_code_used




class CodigoPostal(models.Model):
    """
    Clase CodigoPostal
    
    Tiene los atributos asociados a un codigo postal
    """
    codigo_postal = models.CharField(max_length=20)
    asentamiento = models.CharField(max_length=60,
                                        blank=True,
                                        null=True,)
    tipo_asentamiento = models.CharField(max_length=62,
                                        blank=True,
                                        null=True,)
    municipio = models.CharField(max_length=52,
                                        blank=True,
                                        null=True,)
    estado = models.CharField(max_length=62,
                                        blank=True,
                                        null=True,)
    ciudad = models.CharField(max_length=50,
                                        blank=True,
                                        null=True,)
    def __unicode__(self):
        return self.codigo_postal or u''+" "+self.tipo_asentamiento  or u''+" "+self.asentamiento or u''+" "+self.municipio+" "+self.ciudad or u''


class Estado(models.Model):
    AGUASCALIENTES ='AGUASCALIENTES'
    BAJA_CALIFORNIA = 'BAJA CALIFORNIA'
    BAJA_CALIFORNIA_SUR = 'BAJA CALIFORNIA SUR'
    CAMPECHE = 'CAMPECHE'
    CHIAPAS = 'CHIAPAS'
    CHIHUAHUA = 'CHIHUAHUA'
    CIUDAD_DE_MEXICO = 'CIUDAD DE MÉXICO'
    COAHUILA = 'COAHUILA'
    COLIMA = 'COLIMA'
    DURANGO ='DURANGO'
    GUANAJUATO = 'GUANAJUATO'
    GUERRERO = 'GUERRERO'
    HIDALGO = 'HIDALGO'
    JALISCO = 'JALISCO'
    MEXICO = 'MÉXICO'
    MICHOACAN = 'MICHOACÁN'
    MORELOS = 'MORELOS'
    NAYARIT = 'NAYARIT'
    NUEVO_LEON = 'NUEVO LEÓN'
    OAXACA = 'OAXACA'
    PUEBLA = 'PUEBLA'
    QUERETARO = 'QUERÉTARO'
    QUINTANA_ROO = 'QUINTANA ROO'
    SAN_LUIS_POTOSI = 'SAN LUIS POTOSÍ'
    SINALOA = 'SINALOA'
    SONORA = 'SONORA'
    TABASCO = 'TABASCO'
    TAMAULIPAS ='TAMAULIPAS'
    TLAXCALA = 'TLAXCALA'
    VERACRUZ ='VERACRUZ'
    YUCATAN = 'YUCATÁN'
    ZACATECAS ='ZACATECAS'

    ESTADOS = (
        (AGUASCALIENTES ,'AGUASCALIENTES'),
        (BAJA_CALIFORNIA , 'BAJA CALIFORNIA'),
        (BAJA_CALIFORNIA_SUR , 'BAJA CALIFORNIA SUR'),
        (CAMPECHE , 'CAMPECHE'),
        (CHIAPAS , 'CHIAPAS'),
        (CHIHUAHUA , 'CHIHUAHUA'),
        (CIUDAD_DE_MEXICO , 'CIUDAD DE MÉXICO'),
        (COAHUILA , 'COAHUILA'),
        (COLIMA , 'COLIMA'),
        (DURANGO ,'DURANGO'),
        (GUANAJUATO , 'GUANAJUATO'),
        (GUERRERO , 'GUERRERO'),
        (HIDALGO , 'HIDALGO'),
        (JALISCO , 'JALISCO'),
        (MEXICO , 'MÉXICO'),
        (MICHOACAN , 'MICHOACÁN'),
        (MORELOS , 'MORELOS'),
        (NAYARIT , 'NAYARIT'),
        (NUEVO_LEON , 'NUEVO LEÓN'),
        (OAXACA , 'OAXACA'),
        (PUEBLA , 'PUEBLA'),
        (QUERETARO , 'QUERÉTARO'),
        (QUINTANA_ROO , 'QUINTANA ROO'),
        (SAN_LUIS_POTOSI , 'SAN LUIS POTOSÍ'),
        (SINALOA , 'SINALOA'),
        (SONORA , 'SONORA'),
        (TABASCO , 'TABASCO'),
        (TAMAULIPAS ,'TAMAULIPAS'),
        (TLAXCALA , 'TLAXCALA'),
        (VERACRUZ ,'VERACRUZ'),
        (YUCATAN , 'YUCATÁN'),
        (ZACATECAS ,'ZACATECAS')
    )
    estado = models.CharField(
        max_length = 45,
        choices = ESTADOS,
    )
    def __str__(self):
        return self.estado or u''




class Division(models.Model):
    """
    Clase Division
    
    Almacena las divisiondes tematicas.
    """
    ASTROFISICA = 'ASTROFÍSICA'
    DINAMICA_DE_FLUIDOS ='DINÁMICA DE FLUIDOS'
    ESTADO_SOLIDO = 'ESTADO SÓLIDO'
    FISICA_ATOMICA_Y_MOLECULAR = 'FÍSICA ATÓMICA Y MOLECULAR'
    FISICA_DE_RADIACIONES = 'FÍSICA DE RADIACIONES'
    FISICA_MEDICA = 'FÍSICA MÉDICA'
    FISICA_NUCLEAR = 'FÍSICA NUCLEAR'
    GRAVITACION_Y_FISICA_MATEMATICA = 'GRAVITACIÓN Y FÍSICA MATEMÁTICA'
    INFORMACION_CUANTICA = 'INFORMACIÓN CUÁNTICA'
    NANOCIENCIAS_Y_NANOTECNOLOGIA = 'NANOCIENCIAS Y NANOTECNOLOGÍA'
    OPTICA = 'ÓPTICA'
    PARTICULAS_Y_CAMPOS = 'PARTÍCULAS Y CAMPOS'
    PLASMAS = 'PLASMAS'
    RAYOS_COSMICOS = 'RAYOS COSMICOS'
    TERMODINAMICA_Y_FISICA_ESTADISTICA = 'TERMODINÁMICA Y FÍSICA ESTADÍSTICA'
    DIVISION_REGIONAL_SAN_LUIS = 'DIVISIÓN REGIONAL DE SAN LUIS POTOSI'
    DIVISION_REGIONAL_PUEBLA = 'DIVISIÓN REGIONAL DE PUEBLA'
    DIVISION_REGIONAL_TABASCO = 'DIVISIÓN REGIONAL TABASCO'
    


    DIVISIONES = (
        (ASTROFISICA, 'ASTROFÍSICA'),
        (DINAMICA_DE_FLUIDOS, 'DINAMICA DE FLUIDOS'),
        (ESTADO_SOLIDO, 'ESTADO SÓLIDO'),
        (FISICA_ATOMICA_Y_MOLECULAR, 'FÍSICA ATÓMICA Y MOLECULAR'),
        (FISICA_DE_RADIACIONES, 'FÍSICA DE RADIACIONES'),
        (FISICA_MEDICA, 'FÍSICA MÉDICA'),
        (FISICA_NUCLEAR, 'FÍSICA NUCLEAR'),
        (GRAVITACION_Y_FISICA_MATEMATICA, 'GRAVITACIÓN Y FÍSICA MATEMÁTICA'),
        (INFORMACION_CUANTICA, 'INFORMACIÓN CUÁNTICA'),
        (NANOCIENCIAS_Y_NANOTECNOLOGIA,'NANOCIENCIAS Y NANOTECNOLOGÍA'),
        (OPTICA, 'ÓPTICA'),
        (PARTICULAS_Y_CAMPOS,'PARTÍCULAS Y CAMPOS'),
        (PLASMAS,'PLASMAS'),
        (RAYOS_COSMICOS,'RAYOS COSMICOS'),
        (TERMODINAMICA_Y_FISICA_ESTADISTICA,'TERMODINÁMICA Y FÍSICA ESTADÍSTICA'),
        (DIVISION_REGIONAL_SAN_LUIS, 'DIVISIÓN REGIONAL DE SAN LUIS POTOSI'),
        (DIVISION_REGIONAL_PUEBLA, 'DIVISIÓN REGIONAL DE PUEBLA'),
        (DIVISION_REGIONAL_TABASCO, 'DIVISIÓN REGIONAL TABASCO'),
    )
    division = models.CharField(
        max_length = 45,
        choices = DIVISIONES,
    )
    prioridad = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.division or u''








class GradoAcademico(models.Model):
    """
    Clase almacena los grados academicos de un socio
    """
    LICENCIATURA = 'Licenciatura'
    MAESTRIA = 'Maestria'
    DOCTOR = 'Doctorado'
    POSTDOCTOR = 'Estudios Postdoctorales'
    OPCIONES_GRADO = (
            (LICENCIATURA, 'Licenciatura'),
            (MAESTRIA, 'Maestria'),
            (DOCTOR, 'Doctorado'),
            (POSTDOCTOR, 'Estudios Postdoctorales'),
            )
    grado = models.CharField(
        max_length = 24,
        choices = OPCIONES_GRADO,
        )
    def __str__(self):
        return self.grado or u''




class Publicacion(models.Model):
    """
    Clase almacena las publiaciones que son enviadas.
    """
    BOLETIN = 'Boletín'
    CD_CATALOGO = 'Cd_catalogo'
    REVISTA = 'Revista'
    CALENDARIO = 'Calendario'

    OPCIONES_PUBLICACIONES = (
            (REVISTA, 'Revista'),
            (BOLETIN, 'Boletín'),
            (CD_CATALOGO, 'Cd_catalogo'),
            (CALENDARIO, 'Calendario')
            )
    publicacion = models.CharField(
        max_length = 11,
        choices = OPCIONES_PUBLICACIONES,
        )
    def __str__(self):
        return self.publicacion or u''	




@python_2_unicode_compatible
class Account(models.Model):
    numero_socio = models.AutoField(primary_key=True)
    apellido_materno = models.CharField(max_length=20,
                                        blank=True,
                                        null=True,)
    fotografia = models.ImageField(upload_to='socios/Fotos',
                                default='static/default-profile.png',)
    fecha_nacimiento = models.DateField(null=True,
                                        blank=True,)
    sexo = models.CharField(max_length=1,
                                        blank=True,
                                        null=True,
                                        choices=(
                                        ('H', 'Hombre'),
                                        ('M', 'Mujer'),
                                        ('N', 'No binario'),))
    grado_academico = models.CharField(max_length=15,
                                        blank=True,
                                        null=True,)
    institucion = models.CharField(
                                    max_length =50,
                                    blank=True,
                                    null=True,)

    publicacion = models.ManyToManyField(Publicacion,
                                        blank=True)
    calidad = models.CharField(max_length=1,
                                        blank=True,
                                        null=True,
                                        choices=(
                                        ('T', 'Titular'), 
                                        ('E', 'Estudiante')))
    finado = models.CharField(max_length=1,
                                        choices=(
                                        ('N', 'No'), 
                                        ('S', 'Si')),
                                        null = True,
                                        default='N')
    fecha_ingreso = models.CharField(max_length =50,
                                        blank=True,
                                        null=True,)
    division = models.ManyToManyField(Division,
                                        blank=True,)
    tipo_domicilio = models.CharField(max_length =30,
                                        choices=(
                                        ('PRO', 'Profesional'),
                                        ('PAR', 'Particular'),
                                        ('NO', 'No deseo recibir ninguna publicación'),))
    telefono =models.CharField(max_length=62,
                                        null=True,
                                        blank=True,)
    #Campo que me pidio agregar Ricardo
    ocupacion =models.CharField(max_length=30,
                                        choices=(
                                        ('INVESTIGADOR', 'Investigador/Profesor'),
                                        ('ESTUDIANTE', 'Estudiante'),
                                        ('PROFESIONISTA', 'Profesionista')),
                                        null = True,
                                        blank=True,)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="account", verbose_name=_("user"),on_delete=models.CASCADE)

    @classmethod
    def for_request(cls, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            try:
                return Account._default_manager.get(user=user)
            except Account.DoesNotExist:
                pass
        return AnonymousAccount(request)

    @classmethod
    def create(cls, request=None, **kwargs):
        create_email = kwargs.pop("create_email", True)
        confirm_email = kwargs.pop("confirm_email", None)
        account = cls(**kwargs)
        account.save()
        if create_email and account.user.email:
            kwargs = {"primary": True}
            if confirm_email is not None:
                kwargs["confirm"] = confirm_email
            EmailAddress.objects.add_email(account.user, account.user.email, **kwargs)
        return account

    def __str__(self):
        #return str(self.user.first_name+" "+self.user.last_name)
         return str(self.user.id) +" " + str(self.user.first_name+" "+self.user.last_name)

    def now(self):
        """
        Returns a timezone aware datetime localized to the account's timezone.
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        timezone = self.timezone
        return now.astimezone(pytz.timezone(timezone))

    def localtime(self, value):
        """
        Given a datetime object as value convert it to the timezone of
        the account.
        """
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        if value.tzinfo is None:
            value = pytz.timezone(settings.TIME_ZONE).localize(value)
        return value.astimezone(pytz.timezone(timezone))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, **kwargs):
    """
    After User.save is called we check to see if it was a created user. If so,
    we check if the User object wants account creation. If all passes we
    create an Account object.

    We only run on user creation to avoid having to check for existence on
    each call to User.save.
    """

    # Disable post_save during manage.py loaddata
    if kwargs.get("raw", False):
        return False

    user, created = kwargs["instance"], kwargs["created"]
    disabled = getattr(user, "_disable_account_creation", not settings.ACCOUNT_CREATE_ON_SAVE)
    if created and not disabled:
        Account.create(user=user)


@python_2_unicode_compatible
class AnonymousAccount(object):

    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
    def __str__(self):
        return "AnonymousAccount"


@python_2_unicode_compatible
class SignupCode(models.Model):

    class AlreadyExists(Exception):
        pass

    class InvalidCode(Exception):
        pass

    code = models.CharField(_("code"), max_length=64, unique=True)
    max_uses = models.PositiveIntegerField(_("max uses"), default=0)
    expiry = models.DateTimeField(_("expiry"), null=True, blank=True)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, blank=True,unique =True)
    notes = models.TextField(_("notes"), blank=True)
    sent = models.DateTimeField(_("sent"), null=True, blank=True)
    created = models.DateTimeField(_("created"), default=timezone.now, editable=False)
    use_count = models.PositiveIntegerField(_("use count"), editable=False, default=0)

    class Meta:
        verbose_name = _("signup code")
        verbose_name_plural = _("signup codes")

    def __str__(self):
        if self.email:
            return "{0} [{1}]".format(self.email, self.code)
        else:
            return self.code

    @classmethod
    def exists(cls, code=None, email=None):
        checks = []
        if code:
            checks.append(Q(code=code))
        if email:
            checks.append(Q(email=code))
        if not checks:
            return False
        return cls._default_manager.filter(six.moves.reduce(operator.or_, checks)).exists()

    @classmethod
    def create(cls, **kwargs):
        email, code = kwargs.get("email"), kwargs.get("code")
        if kwargs.get("check_exists", True) and cls.exists(code=code, email=email):
            raise cls.AlreadyExists()
        expiry = timezone.now() + datetime.timedelta(hours=kwargs.get("expiry", 24))
        if not code:
            code = hookset.generate_signup_code_token(email)
        params = {
            "code": code,
            "max_uses": kwargs.get("max_uses", 0),
            "expiry": expiry,
            "inviter": kwargs.get("inviter"),
            "notes": kwargs.get("notes", "")
        }
        if email:
            params["email"] = email
        return cls(**params)

    @classmethod
    def check_code(cls, code):
        try:
            signup_code = cls._default_manager.get(code=code)
        except cls.DoesNotExist:
            raise cls.InvalidCode()
        else:
            if signup_code.max_uses and signup_code.max_uses <= signup_code.use_count:
                raise cls.InvalidCode()
            else:
                if signup_code.expiry and timezone.now() > signup_code.expiry:
                    raise cls.InvalidCode()
                else:
                    return signup_code

    def calculate_use_count(self):
        self.use_count = self.signupcoderesult_set.count()
        self.save()

    def use(self, user):
        """
        Add a SignupCode result attached to the given user.
        """
        result = SignupCodeResult()
        result.signup_code = self
        result.user = user
        result.save()
        signup_code_used.send(sender=result.__class__, signup_code_result=result)

    def send(self, **kwargs):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        if "signup_url" not in kwargs:
            signup_url = "{0}://{1}{2}?{3}".format(
                protocol,
                current_site.domain,
                reverse("account_signup"),
                urlencode({"code": self.code})
            )
        else:
            signup_url = kwargs["signup_url"]
        ctx = {
            "signup_code": self,
            "current_site": current_site,
            "signup_url": signup_url,
        }
        ctx.update(kwargs.get("extra_ctx", {}))
        hookset.send_invitation_email([self.email], ctx)
        self.sent = timezone.now()
        self.save()
        signup_code_sent.send(sender=SignupCode, signup_code=self)


class SignupCodeResult(models.Model):

    signup_code = models.ForeignKey(SignupCode,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, **kwargs):
        super(SignupCodeResult, self).save(**kwargs)
        self.signup_code.calculate_use_count()


@python_2_unicode_compatible
class EmailAddress(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    verified = models.BooleanField(_("verified"), default=False)
    primary = models.BooleanField(_("primary"), default=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        if not settings.ACCOUNT_EMAIL_UNIQUE:
            unique_together = [("user", "email")]

    def __str__(self):
        return "{0} ({1})".format(self.email, self.user)

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.email = self.email
        self.user.save()
        return True

    def send_confirmation(self, **kwargs):
        confirmation = EmailConfirmation.create(self)
        #confirmation.send(**kwargs)
        return confirmation

    def change(self, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.user.email = new_email
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation()


@python_2_unicode_compatible
class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(EmailAddress,on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    sent = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for {0}".format(self.email_address)

    @classmethod
    def create(cls, email_address):
        key = hookset.generate_email_confirmation_token(email_address.email)
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(days=settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            signals.email_confirmed.send(sender=self.__class__, email_address=email_address)
            return email_address

    #def send(self, **kwargs):
        #current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        #protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        #activate_url = "{0}://{1}{2}".format(
            #protocol,
            #current_site.domain,
            #reverse(settings.ACCOUNT_EMAIL_CONFIRMATION_URL, args=[self.key])
        #)
        #ctx = {
            #"email_address": self.email_address,
            #"user": self.email_address.user,
            #"activate_url": activate_url,
            #"current_site": current_site,
            #"key": self.key,
        #}
        #hookset.send_confirmation_email([self.email_address.email], ctx)
        #self.sent = timezone.now()
        #self.save()
        #signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)


class AccountDeletion(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=254)
    date_requested = models.DateTimeField(_("date requested"), default=timezone.now)
    date_expunged = models.DateTimeField(_("date expunged"), null=True, blank=True)

    class Meta:
        verbose_name = _("account deletion")
        verbose_name_plural = _("account deletions")

    @classmethod
    def expunge(cls, hours_ago=None):
        if hours_ago is None:
            hours_ago = settings.ACCOUNT_DELETION_EXPUNGE_HOURS
        before = timezone.now() - datetime.timedelta(hours=hours_ago)
        count = 0
        for account_deletion in cls.objects.filter(date_requested__lt=before, user__isnull=False):
            settings.ACCOUNT_DELETION_EXPUNGE_CALLBACK(account_deletion)
            account_deletion.date_expunged = timezone.now()
            account_deletion.save()
            count += 1
        return count

    @classmethod
    def mark(cls, user):
        account_deletion, created = cls.objects.get_or_create(user=user)
        account_deletion.email = user.email
        account_deletion.save()
        settings.ACCOUNT_DELETION_MARK_CALLBACK(account_deletion)
        return account_deletion


class PasswordHistory(models.Model):
    """
    Contains single password history for user.
    """
    class Meta:
        verbose_name = _("password history")
        verbose_name_plural = _("password histories")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="password_history",on_delete=models.CASCADE)
    password = models.CharField(max_length=255)  # encrypted password
    timestamp = models.DateTimeField(default=timezone.now)  # password creation time


class PasswordExpiry(models.Model):
    """
    Holds the password expiration period for a single user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="password_expiry", verbose_name=_("user"),on_delete=models.CASCADE)
    expiry = models.PositiveIntegerField(default=0)




class Domicilio(models.Model):
    codigo_postal = models.PositiveIntegerField(
                                        blank=True,
                                        null=True,)
    socio = models.OneToOneField(Account,
                                        blank=True,on_delete=models.CASCADE)
    calle_numero_apartado_postal = models.CharField(max_length=192,
                                        blank=True,
                                        null=True,)
    colonia = models.CharField(max_length=182,
                                        blank=True,
                                        null=True,)
    municipio_delegacion = models.CharField(max_length=182,
                                        blank=True,
                                        null=True,)
    ciudad = models.CharField(max_length=182,
                                        blank=True,
                                        null=True,)
    estado = models.CharField(max_length=182,
                                        blank=True,
                                        null=True,)
    telefono =models.CharField(max_length=65,
                                        blank=True,
                                        null=True,)
    pais = models.CharField(max_length=30,
                                        default='MÉXICO',
                                        null=False,)
    def __unicode__(self):
        return self.calle_numero_apartado_postal or u''


class DomicilioProfesional(models.Model):
    """
    Clase DomicilioProfesional
    
    Representa una dirección particular de un socio.
    """
    codigo_institucion = models.CharField(max_length=64,
                                        blank=True,
                                        null=True,)
    codigo_postal = models.PositiveIntegerField(
                                        blank=True,
                                        null=True,)
    socio = models.OneToOneField(Account,
                                        blank=True,on_delete=models.CASCADE)
    institucion = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    dependencia = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    calle_numero_apartado_postal = models.CharField(max_length=192,
                                        blank=True,
                                        null=True,)
    colonia = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    municipio_ciudad = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    estado = models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    telefono =models.CharField(max_length=200,
                                        blank=True,
                                        null=True,)
    pais = models.CharField(max_length=30,
                                        default='MÉXICO',
                                        null=False,)
    def __str__(self):
        return self.codigo_institucion or u''



class Delegado(models.Model):
    vigencia = models.DateField()
    socio = models.ForeignKey(Account,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.socio.nombre or u'' +" "+ self.socio.apellido_paterno or u'' +" "+ self.socio.apellido_materno or u''

class Cuota(models.Model):
    socio = models.ForeignKey(Account,on_delete=models.CASCADE)
    fecha_pago = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    cantidad = models.FloatField(null=True,blank =True,
    validators = [MinValueValidator(0.0), MaxValueValidator(10000000)])
    numero_factura = models.CharField(max_length=32,
                                        blank=True,
                                        null=True,)
    class Meta:
        ordering =('fecha_fin','fecha_pago')

    def __unicode__(self):
        return self.fecha_fin



class RepresentanteInstitucional(models.Model):
    vigencia = models.DateField()
    socio = models.ForeignKey(Account,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.socio.nombre or u'' +" "+ self.socio.apellido_paterno or u'' +" "+ self.socio.apellido_materno or u''


class PresidenteDivision(models.Model):
    vigencia = models.DateField()
    socio = models.ForeignKey(Account,on_delete=models.CASCADE)
    division = models.OneToOneField(Division,on_delete=models.CASCADE)
    def __unicode__(self):
        return self.socio.nombre +" "+ self.socio.apellido_paterno or u'' +" "+ self.socio.apellido_materno or u'' + " " +self.division.division 

class PublicacionDevuelta(models.Model):
    socio = models.ForeignKey(Account,on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion,on_delete=models.CASCADE)
    fecha_envio = models.DateField()
    Enviado = 'Enviado'
    Devuelto = 'Devuelto'
    NoExiste = 'Apartado postal no existe'
    Cancelado = 'Apartado postal cancelado'
    OPCIONES_ESTATUS =(
            (Enviado, 'Enviado'),
            (Devuelto, 'Devuelto'),
            (NoExiste, 'Apartado postal no existe'),
            (Cancelado, 'Apartado postal cancelado'),
            )
    estatus = models.CharField(max_length=25,
                                        choices = OPCIONES_ESTATUS,
                                        blank=True,
                                        null=True,)
    comentario = models.TextField(blank=True,
                                        null=True,)
    def __unicode__(self):
        return self.estatus or u''


class tarjetonSocio(models.Model):
    numero_socio = models.AutoField(primary_key=True)
    #user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
class Meta:
        managed = False
        db_table = 'account_account'
