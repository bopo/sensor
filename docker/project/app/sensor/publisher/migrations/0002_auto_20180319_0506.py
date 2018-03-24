# Generated by Django 2.0.3 on 2018-03-19 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publisher', '0001_initial'),
        ('sensor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensor.Topic'),
        ),
        migrations.AddField(
            model_name='client',
            name='auth',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='publisher.Auth'),
        ),
        migrations.AddField(
            model_name='client',
            name='client_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sensor.ClientId'),
        ),
        migrations.AddField(
            model_name='client',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.Server'),
        ),
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('host', 'port')},
        ),
        migrations.AlterUniqueTogether(
            name='data',
            unique_together={('client', 'topic')},
        ),
    ]
