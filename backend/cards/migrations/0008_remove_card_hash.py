# Generated by Django 4.1.5 on 2023-02-28 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='hash',
        ),
    ]
