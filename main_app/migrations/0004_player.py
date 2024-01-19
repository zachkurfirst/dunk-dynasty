# Generated by Django 5.0.1 on 2024-01-19 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=3)),
                ('height_feet', models.IntegerField()),
                ('height_inches', models.IntegerField()),
                ('weight_pounds', models.IntegerField()),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.franchise')),
            ],
        ),
    ]
