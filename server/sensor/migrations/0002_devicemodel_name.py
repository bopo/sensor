# Generated by Django 2.0.3 on 2018-03-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicemodel',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=23, unique=True),
        ),
    ]