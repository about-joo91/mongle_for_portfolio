# Generated by Django 2.0.2 on 2019-06-03 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webpush", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriptioninfo",
            name="endpoint",
            field=models.URLField(max_length=500),
        ),
    ]
