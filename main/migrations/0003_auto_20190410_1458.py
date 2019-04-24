# Generated by Django 2.2 on 2019-04-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='mode',
            field=models.CharField(default='Pre-Paid', max_length=40),
            preserve_default=False,
        ),
    ]
