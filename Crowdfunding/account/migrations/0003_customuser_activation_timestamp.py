# Generated by Django 4.2.6 on 2023-10-27 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]