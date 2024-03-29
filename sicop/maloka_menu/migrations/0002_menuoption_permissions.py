# Generated by Django 4.2.7 on 2024-03-20 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("maloka_menu", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuoption",
            name="permissions",
            field=models.ManyToManyField(
                help_text="Permissions", related_name="menu_options", to="auth.permission", verbose_name="Permissions"
            ),
        ),
    ]
