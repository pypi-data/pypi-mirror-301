# Generated by Django 2.2.12 on 2020-09-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0142_add_testrun_file_storage'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='storage',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
