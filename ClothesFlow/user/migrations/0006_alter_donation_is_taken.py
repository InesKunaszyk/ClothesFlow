# Generated by Django 4.1.2 on 2022-11-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_donation_is_taken_donation_taken_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False, null=True),
        ),
    ]