# Generated by Django 4.2.1 on 2023-06-20 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_producto_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigosAlternos',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nomCodSat',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nomUniSat',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombreProveedor',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
