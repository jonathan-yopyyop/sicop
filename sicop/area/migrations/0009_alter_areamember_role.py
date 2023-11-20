# Generated by Django 4.2.7 on 2023-11-16 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("area", "0008_alter_areamember_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="areamember",
            name="role",
            field=models.ForeignKey(
                blank=True,
                help_text="Area Role",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="area.arearole",
                verbose_name="Area Role",
            ),
        ),
    ]