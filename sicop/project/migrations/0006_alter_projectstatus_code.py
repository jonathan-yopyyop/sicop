# Generated by Django 4.2.6 on 2023-10-18 16:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0005_alter_projecttype_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectstatus",
            name="code",
            field=models.SlugField(blank=True, help_text="Code", max_length=150, null=True, verbose_name="Code"),
        ),
    ]
