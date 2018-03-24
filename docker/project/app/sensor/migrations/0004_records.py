# Generated by Django 2.0.3 on 2018-03-20 08:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
        ('sensor', '0003_auto_20180320_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('normal', '无状态'), ('agree', '同意'), ('reject', '拒绝')], default='normal', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensor.Device')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat.Member')),
            ],
            options={
                'verbose_name': '使用记录',
                'verbose_name_plural': '使用记录',
            },
        ),
    ]
