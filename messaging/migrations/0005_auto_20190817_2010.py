# Generated by Django 2.2 on 2019-08-17 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_auto_20190805_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.CharField(max_length=27)),
                ('image', models.ImageField(upload_to='image/<function get_filename at 0x7f13cf1582f0>')),
                ('thumbnail', models.ImageField(upload_to='thumbnails/<function get_filename at 0x7f13cf1582f0>')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='messaging.Media'),
        ),
    ]