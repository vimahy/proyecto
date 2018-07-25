# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-26 18:05
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('numero_socio', models.AutoField(primary_key=True, serialize=False)),
                ('apellido_materno', models.CharField(blank=True, max_length=20, null=True)),
                ('fotografia', models.ImageField(default='static/default-profile.png', upload_to='socios/Fotos')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('H', 'Hombre'), ('M', 'Mujer'), ('N', 'No binario')], max_length=1, null=True)),
                ('grado_academico', models.CharField(blank=True, max_length=15, null=True)),
                ('institucion', models.CharField(blank=True, max_length=50, null=True)),
                ('calidad', models.CharField(blank=True, choices=[('T', 'Titular'), ('E', 'Estudiante')], max_length=1, null=True)),
                ('finado', models.CharField(choices=[('N', 'No'), ('S', 'Si')], default='N', max_length=1, null=True)),
                ('fecha_ingreso', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_domicilio', models.CharField(choices=[('PRO', 'Profesional'), ('PAR', 'Particular'), ('NO', 'No deseo recibir ninguna publicaci\xf3n')], max_length=30)),
                ('telefono', models.CharField(blank=True, max_length=62, null=True)),
                ('ocupacion', models.CharField(blank=True, choices=[('INVESTIGADOR', 'Investigador/Profesor'), ('ESTUDIANTE', 'Estudiante'), ('PROFESIONISTA', 'Profesionista')], max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountDeletion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_requested', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date requested')),
                ('date_expunged', models.DateTimeField(blank=True, null=True, verbose_name='date expunged')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'account deletion',
                'verbose_name_plural': 'account deletions',
            },
        ),
        migrations.CreateModel(
            name='CodigoPostal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_postal', models.CharField(max_length=20)),
                ('asentamiento', models.CharField(blank=True, max_length=60, null=True)),
                ('tipo_asentamiento', models.CharField(blank=True, max_length=62, null=True)),
                ('municipio', models.CharField(blank=True, max_length=52, null=True)),
                ('estado', models.CharField(blank=True, max_length=62, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(null=True)),
                ('fecha_fin', models.DateField(null=True)),
                ('cantidad', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10000000)])),
                ('numero_factura', models.CharField(blank=True, max_length=32, null=True)),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Delegado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vigencia', models.DateField()),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(choices=[('ASTROF\xcdSICA', 'ASTROF\xcdSICA'), ('DIN\xc1MICA DE FLUIDOS', 'DINAMICA DE FLUIDOS'), ('ESTADO S\xd3LIDO', 'ESTADO S\xd3LIDO'), ('F\xcdSICA AT\xd3MICA Y MOLECULAR', 'F\xcdSICA AT\xd3MICA Y MOLECULAR'), ('F\xcdSICA DE RADIACIONES', 'F\xcdSICA DE RADIACIONES'), ('F\xcdSICA M\xc9DICA', 'F\xcdSICA M\xc9DICA'), ('F\xcdSICA NUCLEAR', 'F\xcdSICA NUCLEAR'), ('GRAVITACI\xd3N Y F\xcdSICA MATEM\xc1TICA', 'GRAVITACI\xd3N Y F\xcdSICA MATEM\xc1TICA'), ('INFORMACI\xd3N CU\xc1NTICA', 'INFORMACI\xd3N CU\xc1NTICA'), ('NANOCIENCIAS Y NANOTECNOLOG\xcdA', 'NANOCIENCIAS Y NANOTECNOLOG\xcdA'), ('\xd3PTICA', '\xd3PTICA'), ('PART\xcdCULAS Y CAMPOS', 'PART\xcdCULAS Y CAMPOS'), ('PLASMAS', 'PLASMAS'), ('RAYOS COSMICOS', 'RAYOS COSMICOS'), ('TERMODIN\xc1MICA Y F\xcdSICA ESTAD\xcdSTICA', 'TERMODIN\xc1MICA Y F\xcdSICA ESTAD\xcdSTICA'), ('DIVISI\xd3N REGIONAL DE SAN LUIS POTOSI', 'DIVISI\xd3N REGIONAL DE SAN LUIS POTOSI'), ('DIVISI\xd3N REGIONAL DE PUEBLA', 'DIVISI\xd3N REGIONAL DE PUEBLA'), ('DIVISI\xd3N REGIONAL TABASCO', 'DIVISI\xd3N REGIONAL TABASCO')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_postal', models.PositiveIntegerField(blank=True, null=True)),
                ('calle_numero_apartado_postal', models.CharField(blank=True, max_length=192, null=True)),
                ('colonia', models.CharField(blank=True, max_length=182, null=True)),
                ('municipio_delegacion', models.CharField(blank=True, max_length=182, null=True)),
                ('ciudad_y_estado', models.CharField(blank=True, max_length=182, null=True)),
                ('telefono', models.CharField(blank=True, max_length=65, null=True)),
                ('socio', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='DomicilioProfesional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_institucion', models.CharField(blank=True, max_length=64, null=True)),
                ('codigo_postal', models.PositiveIntegerField(blank=True, null=True)),
                ('institucion', models.CharField(blank=True, max_length=200, null=True)),
                ('dependencia', models.CharField(blank=True, max_length=200, null=True)),
                ('calle_numero_apartado_postal', models.CharField(blank=True, max_length=192, null=True)),
                ('colonia', models.CharField(blank=True, max_length=200, null=True)),
                ('estado_municipio_ciudad', models.CharField(blank=True, max_length=200, null=True)),
                ('telefono', models.CharField(blank=True, max_length=200, null=True)),
                ('correo_electronico', models.EmailField(blank=True, max_length=254, null=True)),
                ('socio', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('verified', models.BooleanField(default=False, verbose_name='verified')),
                ('primary', models.BooleanField(default=False, verbose_name='primary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'email address',
                'verbose_name_plural': 'email addresses',
            },
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('sent', models.DateTimeField(null=True)),
                ('key', models.CharField(max_length=64, unique=True)),
                ('email_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.EmailAddress')),
            ],
            options={
                'verbose_name': 'email confirmation',
                'verbose_name_plural': 'email confirmations',
            },
        ),
        migrations.CreateModel(
            name='GradoAcademico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grado', models.CharField(choices=[('Licenciatura', 'Licenciatura'), ('Maestria', 'Maestria'), ('Doctorado', 'Doctorado'), ('Estudios Postdoctorales', 'Estudios Postdoctorales')], max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordExpiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='password_expiry', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='password_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'password history',
                'verbose_name_plural': 'password histories',
            },
        ),
        migrations.CreateModel(
            name='PresidenteDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vigencia', models.DateField()),
                ('division', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.Division')),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicacion', models.CharField(choices=[('Revista', 'Revista'), ('Bolet\xedn', 'Bolet\xedn'), ('Cd_catalogo', 'Cd_catalogo'), ('Calendario', 'Calendario')], max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='PublicacionDevuelta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_envio', models.DateField()),
                ('estatus', models.CharField(blank=True, choices=[('Enviado', 'Enviado'), ('Devuelto', 'Devuelto'), ('Apartado postal no existe', 'Apartado postal no existe'), ('Apartado postal cancelado', 'Apartado postal cancelado')], max_length=25, null=True)),
                ('comentario', models.TextField(blank=True, null=True)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Publicacion')),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='RepresentanteInstitucional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vigencia', models.DateField()),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True, verbose_name='code')),
                ('max_uses', models.PositiveIntegerField(default=0, verbose_name='max uses')),
                ('expiry', models.DateTimeField(blank=True, null=True, verbose_name='expiry')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('sent', models.DateTimeField(blank=True, null=True, verbose_name='sent')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('use_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='use count')),
                ('inviter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'signup code',
                'verbose_name_plural': 'signup codes',
            },
        ),
        migrations.CreateModel(
            name='SignupCodeResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('signup_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.SignupCode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='division',
            field=models.ManyToManyField(blank=True, to='account.Division'),
        ),
        migrations.AddField(
            model_name='account',
            name='publicacion',
            field=models.ManyToManyField(blank=True, to='account.Publicacion'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
