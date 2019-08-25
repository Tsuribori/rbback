# Generated by Django 2.2 on 2019-04-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_auto_20190421_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room',
            new_name='thread',
        ),
        migrations.AlterField(
            model_name='message',
            name='post',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='message',
            name='poster_id',
            field=models.CharField(max_length=27),
        ),
        migrations.AlterField(
            model_name='thread',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]