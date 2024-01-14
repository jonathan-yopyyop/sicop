# Generated by Django 4.2.7 on 2024-01-14 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("purchase_order", "0003_alter_purchaseorder_fecentrega"),
        ("contract", "0004_contract_cost_center_contract_third"),
        ("budget", "0053_alter_commitment_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commitment",
            name="user",
            field=models.ForeignKey(
                help_text="User",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_commintments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentcontract",
            name="commitment",
            field=models.ForeignKey(
                help_text="Commitment",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commitment_contract",
                to="budget.commitment",
                verbose_name="Commitment",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentcontract",
            name="contract",
            field=models.ForeignKey(
                help_text="Contract",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contract_commitment_po",
                to="contract.contract",
                verbose_name="Contract",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentpo",
            name="commitment",
            field=models.ForeignKey(
                help_text="Commitment",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commitment_po",
                to="budget.commitment",
                verbose_name="Commitment",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentpo",
            name="po",
            field=models.ForeignKey(
                help_text="Purchase Order",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="purchase_order_commitment_po",
                to="purchase_order.purchaseorder",
                verbose_name="Purchase Order",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentrealeaseitems",
            name="budget",
            field=models.ForeignKey(
                help_text="Budget",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="budget_commitment_release_items",
                to="budget.budget",
                verbose_name="Budget",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentrealeaseitems",
            name="commitment_release",
            field=models.ForeignKey(
                help_text="Commitment Release",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commitment_release_items",
                to="budget.commitmentrelease",
                verbose_name="Commitment Release",
            ),
        ),
        migrations.AlterField(
            model_name="commitmentrelease",
            name="commitment",
            field=models.ForeignKey(
                help_text="Commitment",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commitment_release",
                to="budget.commitment",
                verbose_name="Commitment",
            ),
        ),
    ]
