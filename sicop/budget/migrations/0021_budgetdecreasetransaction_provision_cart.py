# Generated by Django 5.0 on 2023-12-15 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0020_provisioncartapproval_observation"),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetdecreasetransaction",
            name="provision_cart",
            field=models.ForeignKey(
                blank=True,
                help_text="Provision cart",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="provision_cart_transactions",
                to="budget.provisioncart",
                verbose_name="Provision cart",
            ),
        ),
    ]
