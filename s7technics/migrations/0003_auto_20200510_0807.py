# Generated by Django 2.0.5 on 2020-05-10 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('s7technics', '0002_auto_20200510_0426'),
    ]

    operations = [
        migrations.AddField(
            model_name='hangar',
            name='airplane',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='s7technics.AirPlane'),
        ),
        migrations.AddField(
            model_name='hangar',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
