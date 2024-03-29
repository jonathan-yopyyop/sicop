# Generated by Django 4.2.7 on 2024-03-20 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("area", "0003_areamember_job_title"),
        ("maloka_menu", "0002_menuoption_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuoption",
            name="special_roles",
            field=models.ManyToManyField(
                blank=True,
                help_text="Special roles",
                null=True,
                related_name="menu_special_options",
                to="area.arearole",
                verbose_name="Special roles",
            ),
        ),
    ]
