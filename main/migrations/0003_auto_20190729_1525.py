# Generated by Django 2.2 on 2019-07-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_shipment_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='labels/'),
        ),
    ]