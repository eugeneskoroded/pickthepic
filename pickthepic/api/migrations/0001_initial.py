# Generated by Django 4.0.3 on 2022-03-10 08:54

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cover', models.ImageField(upload_to=api.models.upload_root)),
                ('show', models.BooleanField(default=True)),
                ('slug', models.SlugField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.models.upload_root)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.collection')),
            ],
        ),
    ]
