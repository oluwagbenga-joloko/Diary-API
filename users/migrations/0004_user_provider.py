# Generated by Django 2.1.2 on 2018-11-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181016_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='provider',
            field=models.TextField(default='default', max_length=60),
        ),
    ]