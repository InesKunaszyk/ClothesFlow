# Generated by Django 4.1.2 on 2022-10-12 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_donation_pick_up_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]