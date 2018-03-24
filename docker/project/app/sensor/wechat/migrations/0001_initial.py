# Generated by Django 2.0.3 on 2018-03-19 05:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DBImgTextMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='消息名称')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='消息标题')),
                ('description', models.TextField(blank=True, verbose_name='消息描述')),
                ('pic_url', models.URLField(verbose_name='图片地址')),
                ('url', models.URLField(max_length=255, verbose_name='文章地址')),
            ],
            options={
                'verbose_name': '回复管理(图文消息)',
                'verbose_name_plural': '回复管理(图文消息)',
            },
        ),
        migrations.CreateModel(
            name='DBTextMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='消息名字')),
                ('content', models.TextField(verbose_name='消息内容')),
            ],
            options={
                'verbose_name': '回复管理(文字消息)',
                'verbose_name_plural': '回复管理(文字消息)',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('openid', models.CharField(blank=True, help_text='不能为空', max_length=50, unique=True, verbose_name='openid')),
                ('mobile', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='手机号')),
                ('verify', models.CharField(blank=True, max_length=100, null=True, verbose_name='验证码')),
                ('avatar', models.URLField(verbose_name='头像')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信备注')),
                ('wechat', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信用户名')),
                ('nickname', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='昵称')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='姓名')),
                ('city', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='城市')),
                ('country', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='国家')),
                ('province', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='省份')),
                ('language', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='语言')),
                ('headimgurl', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=200, verbose_name='头像')),
                ('unionid', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=200, verbose_name='唯一标示')),
                ('subscribe_time', models.BigIntegerField(blank=True, null=True, verbose_name='关注事件')),
                ('groupid', models.IntegerField(blank=True, null=True, verbose_name='分组ID')),
                ('sex', models.SmallIntegerField(blank=True, null=True, verbose_name='性别')),
            ],
            options={
                'verbose_name': '微信会员',
                'verbose_name_plural': '微信会员',
            },
        ),
        migrations.CreateModel(
            name='PatternE2PT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识规则', max_length=50, verbose_name='规则命名')),
                ('type', models.CharField(choices=[('text', '文本消息'), ('event', '事件消息'), ('image', '图片消息'), ('location', '位置消息'), ('voice', '语音消息'), ('video', '视频消息')], default='event', help_text='除非你清楚这个字段的含义，否则请不要随意更改', max_length=20, verbose_name='用户消息类型(请保持默认)')),
                ('event', models.CharField(choices=[('subscribe', '关注事件'), ('unsubscribe', '取消关注事件'), ('SCAN', '扫描二维码'), ('LOCATION', '上报地理位置'), ('CLICK', '自定义菜单事件'), ('VIEW', '用户点击链接的跳转事件')], default='CLICK', max_length=30, verbose_name='事件类型')),
                ('event_key', models.CharField(blank=True, help_text='<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>', max_length=255, verbose_name='event_key或者自定义url')),
                ('handler', models.ManyToManyField(help_text='最多允许五条，不然会出错', to='wechat.DBImgTextMsg', verbose_name='回复消息')),
            ],
            options={
                'verbose_name': '回复规则(事件>图文消息)',
                'verbose_name_plural': '回复规则(事件>图文消息)',
            },
        ),
        migrations.CreateModel(
            name='PatternE2T',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识规则', max_length=50, verbose_name='规则命名')),
                ('type', models.CharField(choices=[('text', '文本消息'), ('event', '事件消息'), ('image', '图片消息'), ('location', '位置消息'), ('voice', '语音消息'), ('video', '视频消息')], default='event', max_length=20, verbose_name='收到的消息类型(请保持默认)')),
                ('event', models.CharField(choices=[('subscribe', '关注事件'), ('unsubscribe', '取消关注事件'), ('SCAN', '扫描二维码'), ('LOCATION', '上报地理位置'), ('CLICK', '自定义菜单事件'), ('VIEW', '用户点击链接的跳转事件')], default='CLICK', help_text='除非收到的消息类型为“自定义菜单事件或者点击链接跳转事件，否则不要修改本字段”', max_length=30, verbose_name='事件类型')),
                ('event_key', models.CharField(blank=True, help_text='<strong>对于自定义菜单事件和自定义链接跳转事件这个是必填的！</strong>', max_length=255, verbose_name='event_key或者自定义url')),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat.DBTextMsg', verbose_name='回复消息')),
            ],
            options={
                'verbose_name': '回复规则(事件>文本消息)',
                'verbose_name_plural': '回复规则(事件>文本消息)',
            },
        ),
        migrations.CreateModel(
            name='PatternT2PT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识规则', max_length=50, verbose_name='规则命名')),
                ('type', models.CharField(choices=[('text', '文本消息'), ('event', '事件消息'), ('image', '图片消息'), ('location', '位置消息'), ('voice', '语音消息'), ('video', '视频消息')], default='text', help_text='除非你清楚这个字段的含义，否则请不要随意更改', max_length=20, verbose_name='用户消息类型(请保持默认)')),
                ('content', models.CharField(blank=True, help_text='使用正则表达式', max_length=50, verbose_name='需要匹配的消息')),
                ('handler', models.ManyToManyField(help_text='最多允许五条，不然会出错', to='wechat.DBImgTextMsg', verbose_name='回复消息')),
            ],
            options={
                'verbose_name': '回复规则(文本>图文消息)',
                'verbose_name_plural': '回复规则(文本>图文消息)',
            },
        ),
        migrations.CreateModel(
            name='PatternT2T',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识规则', max_length=50, verbose_name='规则命名')),
                ('type', models.CharField(choices=[('text', '文本消息'), ('event', '事件消息'), ('image', '图片消息'), ('location', '位置消息'), ('voice', '语音消息'), ('video', '视频消息')], default='text', help_text='除非你清楚这个字段的含义，否则请不要随意更改', max_length=20, verbose_name='用户消息类型(请保持默认)')),
                ('content', models.CharField(blank=True, help_text='使用正则表达式', max_length=100, verbose_name='收到的消息')),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wechat.DBTextMsg', verbose_name='响应的消息内容')),
            ],
            options={
                'verbose_name': '回复规则(文本>文本消息)',
                'verbose_name_plural': '回复规则(文本>文本消息)',
            },
        ),
        migrations.CreateModel(
            name='WechatMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='名称')),
                ('slug', models.CharField(default='00', max_length=64)),
                ('type', models.CharField(blank=True, choices=[('click', '点击'), ('view', '链接')], max_length=50, verbose_name='类型')),
                ('key', models.CharField(blank=True, help_text='可以为空，仅用来标识消息', max_length=50, verbose_name='键值')),
                ('is_active', models.BooleanField()),
                ('order', models.IntegerField()),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, default='0', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='wechat.WechatMenu')),
            ],
            options={
                'verbose_name': '微信菜单',
                'verbose_name_plural': '微信菜单',
            },
        ),
    ]