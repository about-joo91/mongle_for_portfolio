# Generated by Django 4.0.6 on 2022-07-13 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jin', '0002_alter_letter_letter_author_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Woory_Category',
        ),
        migrations.RenameField(
            model_name='woory_category',
            old_name='Cate_name',
            new_name='cate_name',
        ),
    ]
