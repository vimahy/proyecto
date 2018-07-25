from __future__ import unicode_literals

from django.contrib import admin

from account.models import (
    Account,
    AccountDeletion,
    EmailAddress,
    PasswordExpiry,
    PasswordHistory,
    SignupCode,
    Division,
    Publicacion,
    Domicilio,
    DomicilioProfesional,
    GradoAcademico,
    CodigoPostal,
    PublicacionDevuelta,
    Cuota,
    Delegado,
    RepresentanteInstitucional,
    PresidenteDivision,
)

from bibliotecas.models import (
    Biblioteca,)


from sociedad.forms import CuotaForm

admin.site.register(Publicacion)
admin.site.register(Division)
admin.site.register(Domicilio)
admin.site.register(DomicilioProfesional)
admin.site.register(GradoAcademico)
admin.site.register(CodigoPostal)
admin.site.register(PublicacionDevuelta)
admin.site.register(Cuota)
admin.site.register(Delegado)
admin.site.register(RepresentanteInstitucional)
admin.site.register(PresidenteDivision)
admin.site.register(Biblioteca)


class BibliotecaAdmin(admin.ModelAdmin):
    list_display=('codigo','nombre','institucion','codigo_postal')


class CuotaForm(admin.ModelAdmin):
    model = Cuota
    form = CuotaForm


class SocioAdmin(admin.ModelAdmin):
    list_display=('numero_socio','nombre')
    list_display_links = ('numero_socio', 'nombre')
    search_fields = ('numero_socio', 'nombre')
    list_per_page = 25



class SignupCodeAdmin(admin.ModelAdmin):

    list_display = ["code", "max_uses", "use_count", "expiry", "created"]
    search_fields = ["code", "email"]
    list_filter = ["created"]
    raw_id_fields = ["inviter"]


class AccountAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    search_fields = ('numero_socio','apellido_materno', 'division', )

class AccountDeletionAdmin(AccountAdmin):

    list_display = ["email", "date_requested", "date_expunged"]


class EmailAddressAdmin(AccountAdmin):

    list_display = ["user", "email", "verified", "primary"]
    search_fields = ["email", "user__username"]


class PasswordExpiryAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]


class PasswordHistoryAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    list_display = ["user", "timestamp"]
    list_filter = ["user"]
    ordering = ["user__username", "-timestamp"]

admin.site.register(Account, AccountAdmin)
admin.site.register(SignupCode, SignupCodeAdmin)
admin.site.register(AccountDeletion, AccountDeletionAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(PasswordExpiry, PasswordExpiryAdmin)
admin.site.register(PasswordHistory, PasswordHistoryAdmin)
