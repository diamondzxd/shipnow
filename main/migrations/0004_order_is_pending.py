# Generated by Django 2.2 on 2019-07-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190729_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_pending',
            field=models.BooleanField(default=True),
        ),
    ]
