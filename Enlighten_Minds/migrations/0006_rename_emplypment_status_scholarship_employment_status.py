# Generated by Django 3.2.6 on 2021-10-09 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Enlighten_Minds', '0005_auto_20211009_0932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scholarship',
            old_name='emplypment_status',
            new_name='employment_status',
        ),
    ]
