# Generated by Django 3.1.7 on 2021-03-03 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20210303_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_presale',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
