# Generated by Django 4.2.7 on 2024-01-10 23:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integration", "0002_contract"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="Cumplido",
            field=models.CharField(
                blank=True, help_text="Cumplido", max_length=250, null=True, verbose_name="Cumplido"
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="IdContrato",
            field=models.CharField(
                blank=True, help_text="IdContrato", max_length=250, null=True, verbose_name="IdContrato"
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="IdEmpres",
            field=models.CharField(
                blank=True, help_text="IdEmpres", max_length=250, null=True, verbose_name="IdEmpres"
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="IdSucurs",
            field=models.CharField(
                blank=True, help_text="IdSucurs", max_length=250, null=True, verbose_name="IdSucurs"
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="TipContrato",
            field=models.CharField(
                blank=True, help_text="TipContrato", max_length=250, null=True, verbose_name="TipContrato"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="Estado",
            field=models.CharField(blank=True, help_text="Estado", max_length=250, null=True, verbose_name="Estado"),
        ),
        migrations.AlterField(
            model_name="contract",
            name="FecMod",
            field=models.CharField(blank=True, help_text="FecMod", max_length=250, null=True, verbose_name="FecMod"),
        ),
        migrations.AlterField(
            model_name="contract",
            name="FechaCon",
            field=models.CharField(
                blank=True, help_text="FechaCon", max_length=250, null=True, verbose_name="FechaCon"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="FechaFin",
            field=models.CharField(
                blank=True, help_text="FechaFin", max_length=250, null=True, verbose_name="FechaFin"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="FechaIni",
            field=models.CharField(
                blank=True, help_text="FechaIni", max_length=250, null=True, verbose_name="FechaIni"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdCenCos",
            field=models.CharField(
                blank=True, help_text="IdCenCos", max_length=250, null=True, verbose_name="IdCenCos"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdCompro",
            field=models.CharField(
                blank=True, help_text="IdCompro", max_length=250, null=True, verbose_name="IdCompro"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdConGas",
            field=models.CharField(
                blank=True, help_text="IdConGas", max_length=250, null=True, verbose_name="IdConGas"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdTercer",
            field=models.CharField(
                blank=True, help_text="IdTercer", max_length=250, null=True, verbose_name="IdTercer"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdTercer1",
            field=models.CharField(
                blank=True, help_text="IdTercer1", max_length=250, null=True, verbose_name="IdTercer1"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="IdUsuari",
            field=models.CharField(
                blank=True, help_text="IdUsuari", max_length=250, null=True, verbose_name="IdUsuari"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="MostrarAutori",
            field=models.CharField(
                blank=True, help_text="MostrarAutori", max_length=250, null=True, verbose_name="MostrarAutori"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="NumCompro",
            field=models.CharField(
                blank=True, help_text="NumCompro", max_length=250, null=True, verbose_name="NumCompro"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="Operac",
            field=models.CharField(blank=True, help_text="Operac", max_length=250, null=True, verbose_name="Operac"),
        ),
        migrations.AlterField(
            model_name="contract",
            name="ValIVA",
            field=models.CharField(blank=True, help_text="ValIVA", max_length=250, null=True, verbose_name="ValIVA"),
        ),
        migrations.AlterField(
            model_name="contract",
            name="ValSinIVA",
            field=models.CharField(
                blank=True, help_text="ValSinIVA", max_length=250, null=True, verbose_name="ValSinIVA"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="ValTot",
            field=models.CharField(blank=True, help_text="ValTot", max_length=250, null=True, verbose_name="ValTot"),
        ),
    ]
