# Generated by Django 4.1.5 on 2023-03-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0013_remove_reviewdatasm2_last_real_interval'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewdatasm2',
            old_name='last_computed_interval',
            new_name='computed_interval',
        ),
    ]
