# Generated by Django 2.1.2 on 2018-12-06 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20181127_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='billing',
        ),
    ]