# Generated by Django 4.1.2 on 2022-10-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_date_joined_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Kategoria'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(to='user.category', verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='description',
            field=models.TextField(verbose_name='Opis instytucji'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Nazwa instytucji'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[(1, 'FOUNDATION'), (2, 'NON-GOVERNMENTAL ORGANIZATION'), (3, 'LOCAL COLLECTION')], default='FOUNDATION', max_length=2, verbose_name='Rodzaj instytucji'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='adres e-mail'),
        ),
    ]