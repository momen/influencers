# Generated by Django 2.1 on 2018-09-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0004_auto_20180920_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencer',
            name='account_holder_name',
            field=models.CharField(max_length=50),
        ),
    ]