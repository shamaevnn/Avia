# Generated by Django 2.0.5 on 2020-05-10 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s7technics', '0003_auto_20200510_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplane',
            name='x_in_hangar',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='airplane',
            name='y_in_hangar',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
