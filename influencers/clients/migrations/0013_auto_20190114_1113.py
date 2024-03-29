# Generated by Django 2.1.4 on 2019-01-14 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_auto_20181206_1335'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignedinfluencer',
            options={'ordering': ['influencer']},
        ),
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': ['-start']},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='influencerhistory',
            options={'ordering': ['assigned_influencer'], 'verbose_name_plural': 'Influencer histories'},
        ),
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['name']},
        ),
    ]
