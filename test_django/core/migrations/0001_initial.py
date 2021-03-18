# Generated by Django 3.1.7 on 2021-03-17 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('adress', models.CharField(blank=True, max_length=50, null=True, verbose_name='Адрес')),
            ],
        ),
    ]