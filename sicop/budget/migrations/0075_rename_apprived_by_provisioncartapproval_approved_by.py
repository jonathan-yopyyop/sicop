# Generated by Django 4.2.7 on 2024-03-23 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0074_provisioncartapproval_apprived_by"),
    ]

    operations = [
        migrations.RenameField(
            model_name="provisioncartapproval",
            old_name="apprived_by",
            new_name="approved_by",
        ),
    ]