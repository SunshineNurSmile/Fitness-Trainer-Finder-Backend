# Generated by Django 4.0.2 on 2022-04-06 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_file_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='eof',
            field=models.BooleanField(default=False),
        ),
    ]
