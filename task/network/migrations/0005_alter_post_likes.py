# Generated by Django 4.0.3 on 2022-04-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_like_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
