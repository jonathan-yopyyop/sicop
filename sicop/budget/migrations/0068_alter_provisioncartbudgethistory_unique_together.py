# Generated by Django 4.2.7 on 2024-02-04 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0067_provisioncarthistory_provisioncartbudgethistory"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="provisioncartbudgethistory",
            unique_together=set(),
        ),
    ]