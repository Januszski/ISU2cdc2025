# Generated by Django 5.1.6 on 2025-03-06 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_downloadlink_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(max_length=10)),
                ('release_date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
    ]
