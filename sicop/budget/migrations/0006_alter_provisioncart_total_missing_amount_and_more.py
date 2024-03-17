# Generated by Django 4.2.7 on 2023-11-26 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0005_provisioncart_total_missing_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="provisioncart",
            name="total_missing_amount",
            field=models.FloatField(
                blank=True,
                default=0,
                help_text="Total provisioned amount",
                null=True,
                verbose_name="Total provisioned amount",
            ),
        ),
        migrations.AlterField(
            model_name="provisioncart",
            name="total_provisioned_amount",
            field=models.FloatField(
                blank=True,
                default=0,
                help_text="Total provisioned amount",
                null=True,
                verbose_name="Total provisioned amount",
            ),
        ),
        migrations.AlterField(
            model_name="provisioncart",
            name="total_required_amount",
            field=models.FloatField(
                blank=True,
                default=0,
                help_text="Total provisioned amount",
                null=True,
                verbose_name="Total provisioned amount",
            ),
        ),
    ]
