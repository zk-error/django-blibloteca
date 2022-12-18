# Generated by Django 4.1.3 on 2022-12-14 22:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libro', '0002_libro_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_dias', models.SmallIntegerField(default=7, verbose_name='Cantidad de Dias a Reservar')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('fecha_vencimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento de la reserva')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libro.libro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
    ]