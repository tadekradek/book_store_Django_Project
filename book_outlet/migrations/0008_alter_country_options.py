# Generated by Django 4.1.3 on 2022-11-17 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_outlet', '0007_country_alter_address_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
    ]