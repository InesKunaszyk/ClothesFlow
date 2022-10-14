# Generated by Django 4.1.2 on 2022-10-12 11:42

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact Phone Number', max_length=31),
        ),
    ]