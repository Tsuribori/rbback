# Generated by Django 2.2 on 2019-04-21 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authtoken', '0002_auto_20160226_1747'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('thread_id', models.CharField(max_length=27, unique=True)),
                ('password_enabled', models.BooleanField(default=False)),
                ('password', models.CharField(editable=False, max_length=300)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='authtoken.Token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('post', models.TextField(editable=False, max_length=10000)),
                ('poster_id', models.CharField(editable=False, max_length=27)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messaging.Thread')),
            ],
        ),
    ]
