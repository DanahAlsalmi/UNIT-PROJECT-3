# Generated by Django 5.0 on 2023-12-07 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='poster',
            field=models.ImageField(default='images/events.png', upload_to='images/'),
        ),
    ]