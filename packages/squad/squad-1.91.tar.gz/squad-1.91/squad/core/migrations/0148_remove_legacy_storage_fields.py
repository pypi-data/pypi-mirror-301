# Generated by Django 2.2.17 on 2020-12-10 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0147_add_build_and_environment_to_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='old_data',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='old_log_file',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='old_metrics_file',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='old_tests_file',
        ),
    ]
