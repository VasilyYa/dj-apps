# Generated by Django 3.1.7 on 2021-03-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210317_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='adress',
            field=models.CharField(blank=True, db_column='addr', max_length=50, null=True, verbose_name='Адрес'),
        ),
    ]