# Generated by Django 2.0.3 on 2018-03-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0005_auto_20180322_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='action',
            field=models.CharField(blank=True, max_length=64, verbose_name='设备操作'),
        ),
    ]
