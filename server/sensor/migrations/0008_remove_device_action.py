# Generated by Django 2.0.3 on 2018-03-26 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0007_auto_20180326_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='action',
        ),
    ]
