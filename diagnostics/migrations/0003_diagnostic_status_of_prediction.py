# Generated by Django 5.1.1 on 2024-12-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_rename_patient_id_diagnostic_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='status_of_prediction',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]