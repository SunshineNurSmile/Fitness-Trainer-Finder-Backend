# Generated by Django 4.0.2 on 2022-04-13 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0036_alter_note_trainee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='trainee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='base.trainee'),
        ),
    ]
