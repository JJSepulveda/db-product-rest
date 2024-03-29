# Generated by Django 4.2.1 on 2024-03-25 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_producto_existencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='existenciaDistr',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaMakita',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaPiso',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaProd',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaStaRosa',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaTanques',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaTotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='existenciaTubos',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
