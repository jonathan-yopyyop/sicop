from django.db import models
from django.utils.translation import gettext_lazy as _

from config.models import BaseModel


class Third(BaseModel):
    """Model definition for Third."""

    IdEmpres = models.CharField(
        _("IdEmpres"),
        null=True,
        blank=True,
        help_text=_("IdEmpres"),
        max_length=150,
    )
    IdSucurs = models.CharField(
        _("IdSucurs"),
        null=True,
        blank=True,
        help_text=_("IdSucurs"),
        max_length=150,
    )
    IdTercer = models.CharField(
        _("IdTercer"),
        null=True,
        blank=True,
        help_text=_("IdTercer"),
        max_length=150,
    )
    Nombre = models.CharField(
        _("Nombre"),
        null=True,
        blank=True,
        help_text=_("Nombre"),
        max_length=150,
    )
    Razon = models.CharField(
        _("Razon"),
        null=True,
        blank=True,
        help_text=_("Razon"),
        max_length=150,
    )
    TipoId = models.CharField(
        _("TipoId"),
        null=True,
        blank=True,
        help_text=_("TipoId"),
        max_length=150,
    )
    Nit = models.CharField(
        _("Nit"),
        null=True,
        blank=True,
        help_text=_("Nit"),
        max_length=150,
    )
    Direcc = models.CharField(
        _("Direcc"),
        null=True,
        blank=True,
        help_text=_("Direcc"),
        max_length=150,
    )
    Telefo = models.CharField(
        _("Telefo"),
        null=True,
        blank=True,
        help_text=_("Telefo"),
        max_length=150,
    )
    Fax = models.CharField(
        _("Fax"),
        null=True,
        blank=True,
        help_text=_("Fax"),
        max_length=150,
    )
    Ciudad = models.CharField(
        _("Ciudad"),
        null=True,
        blank=True,
        help_text=_("Ciudad"),
        max_length=150,
    )
    Pais = models.CharField(
        _("Pais"),
        null=True,
        blank=True,
        help_text=_("Pais"),
        max_length=150,
    )
    Contac = models.CharField(
        _("Contac"),
        null=True,
        blank=True,
        help_text=_("Contac"),
        max_length=150,
    )
    TelContac = models.CharField(
        _("TelContac"),
        null=True,
        blank=True,
        help_text=_("TelContac"),
        max_length=150,
    )
    Observ = models.CharField(
        _("Observ"),
        null=True,
        blank=True,
        help_text=_("Observ"),
        max_length=150,
    )
    IdViades = models.CharField(
        _("IdViades"),
        null=True,
        blank=True,
        help_text=_("IdViades"),
        max_length=150,
    )
    IdCodVen = models.CharField(
        _("IdCodVen"),
        null=True,
        blank=True,
        help_text=_("IdCodVen"),
        max_length=150,
    )
    IdCajBan = models.CharField(
        _("IdCajBan"),
        null=True,
        blank=True,
        help_text=_("IdCajBan"),
        max_length=150,
    )
    TipoCta = models.CharField(
        _("TipoCta"),
        null=True,
        blank=True,
        help_text=_("TipoCta"),
        max_length=150,
    )
    NroCuenta = models.CharField(
        _("NroCuenta"),
        null=True,
        blank=True,
        help_text=_("NroCuenta"),
        max_length=150,
    )
    CupoAsig = models.CharField(
        _("CupoAsig"),
        null=True,
        blank=True,
        help_text=_("CupoAsig"),
        max_length=150,
    )
    CupoDisp = models.CharField(
        _("CupoDisp"),
        null=True,
        blank=True,
        help_text=_("CupoDisp"),
        max_length=150,
    )
    FecIngreso = models.CharField(
        _("FecIngreso"),
        null=True,
        blank=True,
        help_text=_("FecIngreso"),
        max_length=150,
    )
    PorDesc = models.CharField(
        _("PorDesc"),
        null=True,
        blank=True,
        help_text=_("PorDesc"),
        max_length=150,
    )
    PorRecargo = models.CharField(
        _("PorRecargo"),
        null=True,
        blank=True,
        help_text=_("PorRecargo"),
        max_length=150,
    )
    PorTarjeta = models.CharField(
        _("PorTarjeta"),
        null=True,
        blank=True,
        help_text=_("PorTarjeta"),
        max_length=150,
    )
    PorVenta = models.CharField(
        _("PorVenta"),
        null=True,
        blank=True,
        help_text=_("PorVenta"),
        max_length=150,
    )
    PorCobro = models.CharField(
        _("PorCobro"),
        null=True,
        blank=True,
        help_text=_("PorCobro"),
        max_length=150,
    )
    ClaseA = models.CharField(
        _("ClaseA"),
        null=True,
        blank=True,
        help_text=_("ClaseA"),
        max_length=150,
    )
    ClaseB = models.CharField(
        _("ClaseB"),
        null=True,
        blank=True,
        help_text=_("ClaseB"),
        max_length=150,
    )
    ClaseC = models.CharField(
        _("ClaseC"),
        null=True,
        blank=True,
        help_text=_("ClaseC"),
        max_length=150,
    )
    ClaseD = models.CharField(
        _("ClaseD"),
        null=True,
        blank=True,
        help_text=_("ClaseD"),
        max_length=150,
    )
    ClaseE = models.CharField(
        _("ClaseE"),
        null=True,
        blank=True,
        help_text=_("ClaseE"),
        max_length=150,
    )
    Url = models.CharField(
        _("Url"),
        null=True,
        blank=True,
        help_text=_("Url"),
        max_length=250,
    )
    IdAgeIva = models.CharField(
        _("IdAgeIva"),
        null=True,
        blank=True,
        help_text=_("IdAgeIva"),
        max_length=150,
    )
    IdAgeIca = models.CharField(
        _("IdAgeIca"),
        null=True,
        blank=True,
        help_text=_("IdAgeIca"),
        max_length=150,
    )
    IdActIca = models.CharField(
        _("IdActIca"),
        null=True,
        blank=True,
        help_text=_("IdActIca"),
        max_length=150,
    )
    Autoreten = models.CharField(
        _("Autoreten"),
        null=True,
        blank=True,
        help_text=_("Autoreten"),
        max_length=150,
    )
    SujRetFte = models.CharField(
        _("SujRetFte"),
        null=True,
        blank=True,
        help_text=_("SujRetFte"),
        max_length=150,
    )
    IdVended = models.CharField(
        _("IdVended"),
        null=True,
        blank=True,
        help_text=_("IdVended"),
        max_length=150,
    )
    IdLisPre = models.CharField(
        _("IdLisPre"),
        null=True,
        blank=True,
        help_text=_("IdLisPre"),
        max_length=150,
    )
    NivAccDat = models.CharField(
        _("NivAccDat"),
        null=True,
        blank=True,
        help_text=_("NivAccDat"),
        max_length=150,
    )
    SujRetCREE = models.CharField(
        _("SujRetCREE"),
        null=True,
        blank=True,
        help_text=_("SujRetCREE"),
        max_length=150,
    )
    PriApell = models.CharField(
        _("PriApell"),
        null=True,
        blank=True,
        help_text=_("PriApell"),
        max_length=150,
    )
    SegApell = models.CharField(
        _("SegApell"),
        null=True,
        blank=True,
        help_text=_("SegApell"),
        max_length=150,
    )
    PriNombre = models.CharField(
        _("PriNombre"),
        null=True,
        blank=True,
        help_text=_("PriNombre"),
        max_length=150,
    )
    OtrosNom = models.CharField(
        _("OtrosNom"),
        null=True,
        blank=True,
        help_text=_("OtrosNom"),
        max_length=150,
    )
    IdBarrio = models.CharField(
        _("IdBarrio"),
        null=True,
        blank=True,
        help_text=_("IdBarrio"),
        max_length=150,
    )
    IdSector = models.CharField(
        _("IdSector"),
        null=True,
        blank=True,
        help_text=_("IdSector"),
        max_length=150,
    )
    IngAnuales = models.CharField(
        _("IngAnuales"),
        null=True,
        blank=True,
        help_text=_("IngAnuales"),
        max_length=150,
    )
    NumEmp = models.CharField(
        _("NumEmp"),
        null=True,
        blank=True,
        help_text=_("NumEmp"),
        max_length=150,
    )
    PaginaWeb = models.CharField(
        _("PaginaWeb"),
        null=True,
        blank=True,
        help_text=_("PaginaWeb"),
        max_length=150,
    )
    CanalEntrega = models.CharField(
        _("CanalEntrega"),
        null=True,
        blank=True,
        help_text=_("CanalEntrega"),
        max_length=150,
    )
    MatMercantil = models.CharField(
        _("MatMercantil"),
        null=True,
        blank=True,
        help_text=_("MatMercantil"),
        max_length=150,
    )
    IdRespFiscal = models.CharField(
        _("IdRespFiscal"),
        null=True,
        blank=True,
        help_text=_("IdRespFiscal"),
        max_length=150,
    )
    Correo2 = models.CharField(
        _("Correo2"),
        null=True,
        blank=True,
        help_text=_("Correo2"),
        max_length=150,
    )
    Correo3 = models.CharField(
        _("Correo3"),
        null=True,
        blank=True,
        help_text=_("Correo3"),
        max_length=150,
    )
    Campo20 = models.CharField(
        _("Campo20"),
        null=True,
        blank=True,
        help_text=_("Campo20"),
        max_length=150,
    )
    IdUsuari = models.CharField(
        _("IdUsuari"),
        null=True,
        blank=True,
        help_text=_("IdUsuari"),
        max_length=150,
    )
    Operac = models.CharField(
        _("Operac"),
        null=True,
        blank=True,
        help_text=_("Operac"),
        max_length=150,
    )
    FecMod = models.CharField(
        _("FecMod"),
        null=True,
        blank=True,
        help_text=_("FecMod"),
        max_length=150,
    )

    @property
    def name(self):
        return f"{self.Nombre} - {self.Nit}"

    class Meta:
        """Meta definition for Third."""

        verbose_name = "Third"
        verbose_name_plural = "Thirds"

    def __str__(self):
        """Unicode representation of Third."""
        return f"{self.Nombre}"


class CostCenter(BaseModel):
    """Model definition for Cost Center."""

    IdEmpres = models.CharField(
        _("IdEmpres"),
        null=True,
        blank=True,
        help_text=_("IdEmpres"),
        max_length=150,
    )
    IdSucurs = models.CharField(
        _("IdSucurs"),
        null=True,
        blank=True,
        help_text=_("IdSucurs"),
        max_length=150,
    )
    IdCenCos = models.CharField(
        _("IdCenCos"),
        null=True,
        blank=True,
        help_text=_("IdCenCos"),
        max_length=150,
    )
    Nombre = models.CharField(
        _("Nombre"),
        null=True,
        blank=True,
        help_text=_("Nombre"),
        max_length=150,
    )
    Nemoni = models.CharField(
        _("Nemoni"),
        null=True,
        blank=True,
        help_text=_("Nemoni"),
        max_length=150,
    )
    IdTipCen = models.CharField(
        _("IdTipCen"),
        null=True,
        blank=True,
        help_text=_("IdTipCen"),
        max_length=150,
    )
    IdSubcue = models.CharField(
        _("IdSubcue"),
        null=True,
        blank=True,
        help_text=_("IdSubcue"),
        max_length=150,
    )
    IdConGas = models.CharField(
        _("IdConGas"),
        null=True,
        blank=True,
        help_text=_("IdConGas"),
        max_length=150,
    )
    IdTipCenCos = models.CharField(
        _("IdTipCenCos"),
        null=True,
        blank=True,
        help_text=_("IdTipCenCos"),
        max_length=150,
    )
    NivAccDat = models.CharField(
        _("NivAccDat"),
        null=True,
        blank=True,
        help_text=_("NivAccDat"),
        max_length=150,
    )
    IdUsuari = models.CharField(
        _("IdUsuari"),
        null=True,
        blank=True,
        help_text=_("IdUsuari"),
        max_length=150,
    )
    Operac = models.CharField(
        _("Operac"),
        null=True,
        blank=True,
        help_text=_("Operac"),
        max_length=150,
    )
    FecMod = models.CharField(
        _("FecMod"),
        null=True,
        blank=True,
        help_text=_("FecMod"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Cost Center."""

        verbose_name = "Cost Center"
        verbose_name_plural = "Cost Centers"

    def __str__(self):
        """Unicode representation of Cost Center."""
        return self.Nombre


class BusinessUnit(BaseModel):
    """Model definition for Business Unit."""

    IdTipCen = models.CharField(
        _("IdTipCen"),
        null=True,
        blank=True,
        help_text=_("IdTipCen"),
        max_length=150,
    )
    Nombre = models.CharField(
        _("Nombre"),
        null=True,
        blank=True,
        help_text=_("Nombre"),
        max_length=150,
    )
    Nemoni = models.CharField(
        _("Nemoni"),
        null=True,
        blank=True,
        help_text=_("Nemoni"),
        max_length=150,
    )
    IdUsuari = models.CharField(
        _("IdUsuari"),
        null=True,
        blank=True,
        help_text=_("IdUsuari"),
        max_length=150,
    )
    Operac = models.CharField(
        _("Operac"),
        null=True,
        blank=True,
        help_text=_("Operac"),
        max_length=150,
    )
    FecMod = models.CharField(
        _("FecMod"),
        null=True,
        blank=True,
        help_text=_("FecMod"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Business Unit."""

        verbose_name = "Business Unit"
        verbose_name_plural = "Business Units"

    def __str__(self):
        """Unicode representation of Business Unit."""
        return str(self.id)


class ExpenseType(BaseModel):
    """Model definition for Expense Type."""

    IdTipGas = models.CharField(
        _("IdTipGas"),
        null=True,
        blank=True,
        help_text=_("IdTipGas"),
        max_length=150,
    )
    Nombre = models.CharField(
        _("Nombre"),
        null=True,
        blank=True,
        help_text=_("Nombre"),
        max_length=150,
    )
    Nemoni = models.CharField(
        _("Nemoni"),
        null=True,
        blank=True,
        help_text=_("Nemoni"),
        max_length=150,
    )
    ClaseTipGas = models.CharField(
        _("ClaseTipGas"),
        null=True,
        blank=True,
        help_text=_("ClaseTipGas"),
        max_length=150,
    )
    IdOpeGas = models.CharField(
        _("IdOpeGas"),
        null=True,
        blank=True,
        help_text=_("IdOpeGas"),
        max_length=150,
    )
    IdUsuari = models.CharField(
        _("IdUsuari"),
        null=True,
        blank=True,
        help_text=_("IdUsuari"),
        max_length=150,
    )
    Operac = models.CharField(
        _("Operac"),
        null=True,
        blank=True,
        help_text=_("Operac"),
        max_length=150,
    )
    FecMod = models.CharField(
        _("FecMod"),
        null=True,
        blank=True,
        help_text=_("FecMod"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Expense Type."""

        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"

    def __str__(self):
        """Unicode representation of Expense Type."""
        return self.Nombre


class ExpenseConcept(BaseModel):
    """Model definition for Expense Concept."""

    IdConGas = models.CharField(
        _("IdConGas"),
        null=True,
        blank=True,
        help_text=_("IdConGas"),
        max_length=150,
    )
    Nombre = models.CharField(
        _("Nombre"),
        null=True,
        blank=True,
        help_text=_("Nombre"),
        max_length=150,
    )
    Nemoni = models.CharField(
        _("Nemoni"),
        null=True,
        blank=True,
        help_text=_("Nemoni"),
        max_length=150,
    )
    TipoPresup = models.CharField(
        _("TipoPresup"),
        null=True,
        blank=True,
        help_text=_("TipoPresup"),
        max_length=150,
    )
    IdRetFte = models.CharField(
        _("IdRetFte"),
        null=True,
        blank=True,
        help_text=_("IdRetFte"),
        max_length=150,
    )
    IdTipGas = models.CharField(
        _("IdTipGas"),
        null=True,
        blank=True,
        help_text=_("IdTipGas"),
        max_length=150,
    )
    IdConGasDistrib = models.CharField(
        _("IdConGasDistrib"),
        null=True,
        blank=True,
        help_text=_("IdConGasDistrib"),
        max_length=150,
    )
    CtGtoCauPag = models.CharField(
        _("CtGtoCauPag"),
        null=True,
        blank=True,
        help_text=_("CtGtoCauPag"),
        max_length=150,
    )
    ECtGtoCauPag = models.CharField(
        _("ECtGtoCauPag"),
        null=True,
        blank=True,
        help_text=_("ECtGtoCauPag"),
        max_length=150,
    )
    IdTipIVA = models.CharField(
        _("IdTipIVA"),
        null=True,
        blank=True,
        help_text=_("IdTipIVA"),
        max_length=150,
    )
    PorIva = models.CharField(
        _("PorIva"),
        null=True,
        blank=True,
        help_text=_("PorIva"),
        max_length=150,
    )
    CodEquival = models.CharField(
        _("CodEquival"),
        null=True,
        blank=True,
        help_text=_("CodEquival"),
        max_length=150,
    )
    CtGastos = models.CharField(
        _("CtGastos"),
        null=True,
        blank=True,
        help_text=_("CtGastos"),
        max_length=150,
    )
    ECtGastos = models.CharField(
        _("ECtGastos"),
        null=True,
        blank=True,
        help_text=_("ECtGastos"),
        max_length=150,
    )
    EsBaseImpto = models.CharField(
        _("EsBaseImpto"),
        null=True,
        blank=True,
        help_text=_("EsBaseImpto"),
        max_length=150,
    )
    ValorBase = models.CharField(
        _("ValorBase"),
        null=True,
        blank=True,
        help_text=_("ValorBase"),
        max_length=150,
    )
    ValorMax = models.CharField(
        _("ValorMax"),
        null=True,
        blank=True,
        help_text=_("ValorMax"),
        max_length=150,
    )
    IdConMedMag = models.CharField(
        _("IdConMedMag"),
        null=True,
        blank=True,
        help_text=_("IdConMedMag"),
        max_length=150,
    )
    Campo1 = models.CharField(
        _("Campo1"),
        null=True,
        blank=True,
        help_text=_("Campo1"),
        max_length=150,
    )
    IdUsuari = models.CharField(
        _("IdUsuari"),
        null=True,
        blank=True,
        help_text=_("IdUsuari"),
        max_length=150,
    )
    Operac = models.CharField(
        _("Operac"),
        null=True,
        blank=True,
        help_text=_("Operac"),
        max_length=150,
    )
    FecMod = models.CharField(
        _("FecMod"),
        null=True,
        blank=True,
        help_text=_("FecMod"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Expense Concept."""

        verbose_name = "Expense Concept"
        verbose_name_plural = "Expense Concepts"

    def __str__(self):
        """Unicode representation of Expense Concept."""
        return self.Nombre
