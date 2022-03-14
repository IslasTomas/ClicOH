# Generated by Django 4.0.3 on 2022-03-14 02:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.FloatField()),
                ('stock', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
