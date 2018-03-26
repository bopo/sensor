# Generated by Django 2.0.3 on 2018-03-26 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0006_device_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='device',
            name='action',
            field=models.CharField(blank=True, choices=[('start', '开机'), ('close', '关机'), ('clock', '定时')], max_length=64, verbose_name='设备操作'),
        ),
    ]
