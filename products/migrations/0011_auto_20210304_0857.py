# Generated by Django 3.1.7 on 2021-03-04 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_ticket_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='code',
            field=models.IntegerField(null=True),
        ),
    ]
