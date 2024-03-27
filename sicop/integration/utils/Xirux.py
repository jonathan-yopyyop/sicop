import os
import platform
import subprocess
import time
from datetime import datetime, timedelta

import pyodbc

from sicop.business_unit.models import BusinessUnit as SicopBusinessUnit
from sicop.contract.models import Contract as SicopContract
from sicop.contractor.models import Contractor as SicopContractor
from sicop.cost_center.models import CostCenter as SicopCostCenter
from sicop.expense_concept.models import ExpenseConcept as SicopExpenseConcept
from sicop.expense_type.models import ExpenseType as SicopExpenseType
from sicop.integration.models import (
    BusinessUnit,
    Contract,
    CostCenter,
    ExpenseConcept,
    ExpenseType,
    PurchaseOrder,
    Third,
)
from sicop.purchase_order.models import PurchaseOrder as SicopPurchaseOrder


class XiruxIntegration:
    def __init__(self, develop=False):
        if develop:
            self.xirux_user = "sicop"
            self.xirux_password = "S1c0p2024+"
            self.xirux_host = "10.0.1.156"
            self.xirux_port = "8443"
            self.xirux_db = "xirux12"
        else:
            self.xirux_user = os.getenv("MSSQL_XIRUX_USER")
            self.xirux_password = os.getenv("MSSQL_XIRUX_PASSWORD")
            self.xirux_host = os.getenv("MSSQL_XIRUX_HOST")
            self.xirux_port = os.getenv("MSSQL_XIRUX_PORT")
            self.xirux_db = os.getenv("MSSQL_XIRUX_DB")

    def set_mssql_connection(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
            + self.xirux_host
            + ";PORT="
            + self.xirux_port
            + ";DATABASE="
            + self.xirux_db
            + ";UID="
            + self.xirux_user
            + ";PWD="
            + self.xirux_password
            + ";Encrypt=no",
        )
        self.cursor = self.conn.cursor()

    def get_results_xirux(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def business_units(self):
        query_xirux = "select * from ConTipCen"
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdTipCen = result[0]
            Nombre = result[1]
            Nemoni = result[2]
            IdUsuari = result[3]
            Operac = result[4]
            FecMod = result[5]
            # Insert into integration app
            if BusinessUnit.objects.filter(IdTipCen=IdTipCen).count() == 0:
                BusinessUnit.objects.create(
                    IdTipCen=IdTipCen,
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Business unit {IdTipCen} created")

            else:
                BusinessUnit.objects.filter(IdTipCen=IdTipCen).update(
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Business unit {IdTipCen} updated")

            # Insert into Business unit app
            if SicopBusinessUnit.objects.filter(code=IdTipCen).count() == 0:
                SicopBusinessUnit.objects.create(
                    code=IdTipCen,
                    name=Nombre,
                )
                # print(f"Business unit {IdTipCen} created")

            else:
                SicopBusinessUnit.objects.filter(code=IdTipCen).update(
                    name=Nombre,
                )
                # print(f"Business unit {IdTipCen} updated")

    def cost_centers(self):
        query_xirux = "select * from ConCenCos"
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdEmpres = result[0]
            IdSucurs = result[1]
            IdCenCos = result[2]
            Nombre = result[3]
            Nemoni = result[4]
            IdTipCen = result[5]
            IdSubcue = result[6]
            IdConGas = result[7]
            IdTipCenCos = result[8]
            NivAccDat = result[9]
            IdUsuari = result[10]
            Operac = result[11]
            FecMod = result[12]
            # Insert into integration app
            if CostCenter.objects.filter(IdCenCos=IdCenCos).count() == 0:
                CostCenter.objects.create(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    IdCenCos=IdCenCos,
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    IdTipCen=IdTipCen,
                    IdSubcue=IdSubcue,
                    IdConGas=IdConGas,
                    IdTipCenCos=IdTipCenCos,
                    NivAccDat=NivAccDat,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Cost center {IdCenCos} created")

            else:
                CostCenter.objects.filter(IdCenCos=IdCenCos).update(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    IdTipCen=IdTipCen,
                    IdSubcue=IdSubcue,
                    IdConGas=IdConGas,
                    IdTipCenCos=IdTipCenCos,
                    NivAccDat=NivAccDat,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Cost center {IdCenCos} updated")

            # Insert into Cost Center app
            if SicopCostCenter.objects.filter(cost_center_id=IdCenCos).count() == 0:
                SicopCostCenter.objects.create(
                    cost_center_id=IdCenCos,
                    name=Nombre,
                    description=Nombre,
                )
                # print(f"Cost center {IdCenCos} created")

            else:
                SicopCostCenter.objects.filter(cost_center_id=IdCenCos).update(
                    name=Nombre,
                    description=Nombre,
                )
                # print(f"Cost center {IdCenCos} updated")

    def expense_types(self):
        query_xirux = "select * from ConTipGas"
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdTipGas = result[0]
            Nombre = result[1]
            Nemoni = result[2]
            ClaseTipGas = result[3]
            IdOpeGas = result[4]
            IdUsuari = result[5]
            Operac = result[6]
            FecMod = result[7]
            # Insert into integration app
            if ExpenseType.objects.filter(IdTipGas=IdTipGas).count() == 0:
                ExpenseType.objects.create(
                    IdTipGas=IdTipGas,
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    ClaseTipGas=ClaseTipGas,
                    IdOpeGas=IdOpeGas,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Expense type {IdTipGas} created")

            else:
                ExpenseType.objects.filter(IdTipGas=IdTipGas).update(
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    ClaseTipGas=ClaseTipGas,
                    IdOpeGas=IdOpeGas,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Expense type {IdTipGas} updated")

            # Insert into Expense Type app
            if SicopExpenseType.objects.filter(code=IdTipGas).count() == 0:
                SicopExpenseType.objects.create(
                    code=IdTipGas,
                    name=Nombre,
                )
                # print(f"Expense type {IdTipGas} created")

            else:
                SicopExpenseType.objects.filter(code=IdTipGas).update(
                    name=Nombre,
                )
                # print(f"Expense type {IdTipGas} updated")

    def thirds(self):
        if Third.objects.all().count() == 0:
            query_xirux = "select * from ConTercer"
        else:
            fecha_actual = datetime.now()
            fecha_hace_seis_meses = fecha_actual - timedelta(days=5 * 3)
            fecha_formateada = fecha_hace_seis_meses.strftime("%Y-%m-%d")
            query_xirux = f"select * from ConTercer where FecMod > '{fecha_formateada}'"

        print("------------------------", query_xirux, "------------------------", sep="\n")

        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdEmpres = [0]
            IdSucurs = result[1]
            IdTercer = result[2]
            Nombre = result[3]
            Razon = result[4]
            TipoId = result[5]
            Nit = result[6]
            Direcc = result[7]
            Telefo = result[8]
            Fax = result[9]
            Ciudad = result[10]
            Pais = result[11]
            Contac = result[12]
            TelContac = result[13]
            Observ = result[14]
            IdViades = result[15]
            IdCodVen = result[16]
            IdCajBan = result[17]
            TipoCta = result[18]
            NroCuenta = result[19]
            CupoAsig = result[20]
            CupoDisp = result[21]
            FecIngreso = result[22]
            PorDesc = result[23]
            PorRecargo = result[24]
            PorTarjeta = result[25]
            PorVenta = result[26]
            PorCobro = result[27]
            ClaseA = result[28]
            ClaseB = result[29]
            ClaseC = result[30]
            ClaseD = result[31]
            ClaseE = result[32]
            Url = result[33]
            IdAgeIva = result[34]
            IdAgeIca = result[35]
            IdActIca = result[36]
            Autoreten = result[37]
            SujRetFte = result[38]
            IdVended = result[39]
            IdLisPre = result[40]
            NivAccDat = result[41]
            SujRetCREE = result[42]
            PriApell = result[43]
            SegApell = result[44]
            PriNombre = result[45]
            OtrosNom = result[46]
            IdBarrio = result[47]
            IdSector = result[48]
            IngAnuales = result[49]
            NumEmp = result[50]
            PaginaWeb = result[51]
            CanalEntrega = result[52]
            MatMercantil = result[53]
            IdRespFiscal = result[54]
            Correo2 = result[55]
            Correo3 = result[56]
            Campo20 = result[57]
            IdUsuari = result[58]
            Operac = result[59]
            FecMod = result[60]
            # Insert into integration app
            if Third.objects.filter(IdTercer=IdTercer).count() == 0:
                Third.objects.create(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    IdTercer=IdTercer,
                    Nombre=Nombre,
                    Razon=Razon,
                    TipoId=TipoId,
                    Nit=Nit,
                    Direcc=Direcc,
                    Telefo=Telefo,
                    Fax=Fax,
                    Ciudad=Ciudad,
                    Pais=Pais,
                    Contac=Contac,
                    TelContac=TelContac,
                    Observ=Observ,
                    IdViades=IdViades,
                    IdCodVen=IdCodVen,
                    IdCajBan=IdCajBan,
                    TipoCta=TipoCta,
                    NroCuenta=NroCuenta,
                    CupoAsig=CupoAsig,
                    CupoDisp=CupoDisp,
                    FecIngreso=FecIngreso,
                    PorDesc=PorDesc,
                    PorRecargo=PorRecargo,
                    PorTarjeta=PorTarjeta,
                    PorVenta=PorVenta,
                    PorCobro=PorCobro,
                    ClaseA=ClaseA,
                    ClaseB=ClaseB,
                    ClaseC=ClaseC,
                    ClaseD=ClaseD,
                    ClaseE=ClaseE,
                    Url=Url,
                    IdAgeIva=IdAgeIva,
                    IdAgeIca=IdAgeIca,
                    IdActIca=IdActIca,
                    Autoreten=Autoreten,
                    SujRetFte=SujRetFte,
                    IdVended=IdVended,
                    IdLisPre=IdLisPre,
                    NivAccDat=NivAccDat,
                    SujRetCREE=SujRetCREE,
                    PriApell=PriApell,
                    SegApell=SegApell,
                    PriNombre=PriNombre,
                    OtrosNom=OtrosNom,
                    IdBarrio=IdBarrio,
                    IdSector=IdSector,
                    IngAnuales=IngAnuales,
                    NumEmp=NumEmp,
                    PaginaWeb=PaginaWeb,
                    CanalEntrega=CanalEntrega,
                    MatMercantil=MatMercantil,
                    IdRespFiscal=IdRespFiscal,
                    Correo2=Correo2,
                    Correo3=Correo3,
                    Campo20=Campo20,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Third {IdTercer} created")

            else:
                Third.objects.filter(IdTercer=IdTercer).update(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    Nombre=Nombre,
                    Razon=Razon,
                    TipoId=TipoId,
                    Nit=Nit,
                    Direcc=Direcc,
                    Telefo=Telefo,
                    Fax=Fax,
                    Ciudad=Ciudad,
                    Pais=Pais,
                    Contac=Contac,
                    TelContac=TelContac,
                    Observ=Observ,
                    IdViades=IdViades,
                    IdCodVen=IdCodVen,
                    IdCajBan=IdCajBan,
                    TipoCta=TipoCta,
                    NroCuenta=NroCuenta,
                    CupoAsig=CupoAsig,
                    CupoDisp=CupoDisp,
                    FecIngreso=FecIngreso,
                    PorDesc=PorDesc,
                    PorRecargo=PorRecargo,
                    PorTarjeta=PorTarjeta,
                    PorVenta=PorVenta,
                    PorCobro=PorCobro,
                    ClaseA=ClaseA,
                    ClaseB=ClaseB,
                    ClaseC=ClaseC,
                    ClaseD=ClaseD,
                    ClaseE=ClaseE,
                    Url=Url,
                    IdAgeIva=IdAgeIva,
                    IdAgeIca=IdAgeIca,
                    IdActIca=IdActIca,
                    Autoreten=Autoreten,
                    SujRetFte=SujRetFte,
                    IdVended=IdVended,
                    IdLisPre=IdLisPre,
                    NivAccDat=NivAccDat,
                    SujRetCREE=SujRetCREE,
                    PriApell=PriApell,
                    SegApell=SegApell,
                    PriNombre=PriNombre,
                    OtrosNom=OtrosNom,
                    IdBarrio=IdBarrio,
                    IdSector=IdSector,
                    IngAnuales=IngAnuales,
                    NumEmp=NumEmp,
                    PaginaWeb=PaginaWeb,
                    CanalEntrega=CanalEntrega,
                    MatMercantil=MatMercantil,
                    IdRespFiscal=IdRespFiscal,
                    Correo2=Correo2,
                    Correo3=Correo3,
                    Campo20=Campo20,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Third {IdTercer} updated")

            # Insert into Third app
            if SicopContractor.objects.filter(dni=Nit).count() == 0:
                SicopContractor.objects.create(
                    name=Nombre,
                    commertial_name=Razon,
                    dni=Nit,
                    address=Direcc,
                    phone=Telefo,
                )
                # print(f"Third {IdTercer} created")

            else:
                SicopContractor.objects.filter(dni=Nit).update(
                    name=Nombre,
                    commertial_name=Razon,
                    address=Direcc,
                    phone=Telefo,
                )
                # print(f"Third {IdTercer} updated")

    def expense_concepts(self):
        query_xirux = "select * from ConConGas"
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdConGas = result[0]
            Nombre = result[1]
            Nemoni = result[2]
            TipoPresup = result[3]
            IdRetFte = result[4]
            IdTipGas = result[5]
            IdConGasDistrib = result[6]
            CtGtoCauPag = result[7]
            ECtGtoCauPag = result[8]
            IdTipIVA = result[9]
            PorIva = result[10]
            CodEquival = result[11]
            CtGastos = result[12]
            ECtGastos = result[13]
            EsBaseImpto = result[14]
            ValorBase = result[15]
            ValorMax = result[16]
            IdConMedMag = result[17]
            Campo1 = result[18]
            IdUsuari = result[19]
            Operac = result[20]
            FecMod = result[21]
            # Insert into integration app
            if ExpenseConcept.objects.filter(IdConGas=IdConGas).count() == 0:
                ExpenseConcept.objects.create(
                    IdConGas=IdConGas,
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    TipoPresup=TipoPresup,
                    IdRetFte=IdRetFte,
                    IdTipGas=IdTipGas,
                    IdConGasDistrib=IdConGasDistrib,
                    CtGtoCauPag=CtGtoCauPag,
                    ECtGtoCauPag=ECtGtoCauPag,
                    IdTipIVA=IdTipIVA,
                    PorIva=PorIva,
                    CodEquival=CodEquival,
                    CtGastos=CtGastos,
                    ECtGastos=ECtGastos,
                    EsBaseImpto=EsBaseImpto,
                    ValorBase=ValorBase,
                    ValorMax=ValorMax,
                    IdConMedMag=IdConMedMag,
                    Campo1=Campo1,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Expense concept {IdConGas} created")

            else:
                ExpenseConcept.objects.filter(IdConGas=IdConGas).update(
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    TipoPresup=TipoPresup,
                    IdRetFte=IdRetFte,
                    IdTipGas=IdTipGas,
                    IdConGasDistrib=IdConGasDistrib,
                    CtGtoCauPag=CtGtoCauPag,
                    ECtGtoCauPag=ECtGtoCauPag,
                    IdTipIVA=IdTipIVA,
                    PorIva=PorIva,
                    CodEquival=CodEquival,
                    CtGastos=CtGastos,
                    ECtGastos=ECtGastos,
                    EsBaseImpto=EsBaseImpto,
                    ValorBase=ValorBase,
                    ValorMax=ValorMax,
                    IdConMedMag=IdConMedMag,
                    Campo1=Campo1,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Expense concept {IdConGas} updated")

            # Insert into Expense Concept app
            if SicopExpenseConcept.objects.filter(code=IdConGas).count() == 0:
                SicopExpenseConcept.objects.create(
                    code=IdConGas,
                    name=Nombre,
                )
                # print(f"Expense concept {IdConGas} created")

            else:
                SicopExpenseConcept.objects.filter(code=IdConGas).update(
                    name=Nombre,
                )
                # print(f"Expense concept {IdConGas} updated")

    def contracts(self):
        query_xirux = "select * from concontra"
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdEmpres = result[0]
            IdSucurs = result[1]
            IdContrato = result[2]
            TipContrato = result[3]
            Cumplido = result[4]
            Estado = result[5]
            IdTercer = result[6]
            IdCenCos = result[7]
            IdTercer1 = result[8]
            MostrarAutori = result[9]
            FechaCon = result[10]
            FechaIni = result[11]
            FechaFin = result[12]
            Objeto = result[13]
            ValSinIVA = result[14]
            ValIVA = result[15]
            ValTot = result[16]
            Observ = result[17]
            IdCompro = result[18]
            NumCompro = result[19]
            IdConGas = result[20]
            IdUsuari = result[21]
            Operac = result[22]
            FecMod = result[23]
            # Insert into integration app
            if Contract.objects.filter(IdContrato=IdContrato).count() == 0:
                Contract.objects.create(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    IdContrato=IdContrato,
                    TipContrato=TipContrato,
                    Cumplido=Cumplido,
                    Estado=Estado,
                    IdTercer=IdTercer,
                    IdCenCos=IdCenCos,
                    IdTercer1=IdTercer1,
                    MostrarAutori=MostrarAutori,
                    FechaCon=FechaCon,
                    FechaIni=FechaIni,
                    FechaFin=FechaFin,
                    Objeto=Objeto,
                    ValSinIVA=ValSinIVA,
                    ValIVA=ValIVA,
                    ValTot=ValTot,
                    Observ=Observ,
                    IdCompro=IdCompro,
                    NumCompro=NumCompro,
                    IdConGas=IdConGas,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Contract {IdContrato} created")
            else:
                Contract.objects.filter(IdContrato=IdContrato).update(
                    IdEmpres=IdEmpres,
                    IdSucurs=IdSucurs,
                    TipContrato=TipContrato,
                    Cumplido=Cumplido,
                    Estado=Estado,
                    IdTercer=IdTercer,
                    IdCenCos=IdCenCos,
                    IdTercer1=IdTercer1,
                    MostrarAutori=MostrarAutori,
                    FechaCon=FechaCon,
                    FechaIni=FechaIni,
                    FechaFin=FechaFin,
                    Objeto=Objeto,
                    ValSinIVA=ValSinIVA,
                    ValIVA=ValIVA,
                    ValTot=ValTot,
                    Observ=Observ,
                    IdCompro=IdCompro,
                    NumCompro=NumCompro,
                    IdConGas=IdConGas,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Contract {IdContrato} updated")

        contracts = Contract.objects.all()
        for contract in contracts:
            IdContrato = contract.IdContrato
            TipContrato = contract.TipContrato
            Cumplido = contract.Cumplido
            Estado = contract.Estado
            IdTercer = contract.IdTercer
            IdCenCos = contract.IdCenCos

            FechaConString = contract.FechaCon
            fecha_objeto = datetime.strptime(FechaConString, "%Y-%m-%d %H:%M:%S")
            FechaCon = fecha_objeto.date()

            FechaIniString = contract.FechaIni
            fecha_objeto = datetime.strptime(FechaIniString, "%Y-%m-%d %H:%M:%S")
            FechaIni = fecha_objeto.date()

            FechaFinString = contract.FechaFin
            fecha_objeto = datetime.strptime(FechaFinString, "%Y-%m-%d %H:%M:%S")
            FechaFin = fecha_objeto.date()

            Objeto = contract.Objeto

            if contract.ValSinIVA is None:
                ValSinIVA = 0
            else:
                ValSinIVA = float(contract.ValSinIVA)

            if contract.ValIVA is None:
                ValIVA = 0
            else:
                ValIVA = float(contract.ValIVA)

            if contract.ValTot is None:
                ValTot = 0
            else:
                ValTot = float(contract.ValTot)

            NumCompro = contract.NumCompro
            Operac = contract.Operac

            FecModString = contract.FecMod
            FecModStringSplit = FecModString.split(".")
            fecha_objeto = datetime.strptime(FecModStringSplit[0], "%Y-%m-%d %H:%M:%S")
            FecMod = fecha_objeto.date()

            if SicopContract.objects.filter(IdContrato=IdContrato).count() == 0:
                SicopContract.objects.create(
                    IdContrato=IdContrato,
                    TipContrato=TipContrato,
                    Cumplido=Cumplido,
                    Estado=Estado,
                    IdTercer=IdTercer,
                    IdCenCos=IdCenCos,
                    FechaCon=FechaCon,
                    FechaIni=FechaIni,
                    FechaFin=FechaFin,
                    Objeto=Objeto,
                    ValSinIVA=ValSinIVA,
                    ValIVA=ValIVA,
                    ValTot=ValTot,
                    NumCompro=NumCompro,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Contract {IdContrato} created")
            else:
                SicopContract.objects.filter(IdContrato=IdContrato).update(
                    TipContrato=TipContrato,
                    Cumplido=Cumplido,
                    Estado=Estado,
                    IdTercer=IdTercer,
                    IdCenCos=IdCenCos,
                    FechaCon=FechaCon,
                    FechaIni=FechaIni,
                    FechaFin=FechaFin,
                    Objeto=Objeto,
                    ValSinIVA=ValSinIVA,
                    ValIVA=ValIVA,
                    ValTot=ValTot,
                    NumCompro=NumCompro,
                    Operac=Operac,
                    FecMod=FecMod,
                )
                # print(f"Contract {IdContrato} updated")

    def purchase_orders(self):
        if PurchaseOrder.objects.all().count() == 0:
            query_xirux = """
            SELECT IdCompro, IdOperac, Numero, Fecha, FecContab, FecVen, IdTercer, IdActICA,
                IdRetFte, VlrRetFte, FechaCruce, FactProvee, FecEntrega, CostoTtal, VrBruto, VrDesc,
                VrIva, VrReteIva, VrReteIca, VrNeto, VrBaseImp, Direccion, FecMod
            FROM ConDocume cd
            WHERE (IdCompro ='0031' OR IdCompro ='0039' OR IdCompro ='0065')
            ORDER BY FecMod DESC
            """
        else:
            fecha_actual = datetime.now()
            fecha_hace_seis_meses = fecha_actual - timedelta(days=30)
            fecha_formateada = fecha_hace_seis_meses.strftime("%Y-%m-%d")
            query_xirux = f"""
            SELECT IdCompro, IdOperac, Numero, Fecha, FecContab, FecVen, IdTercer, IdActICA,
                IdRetFte, VlrRetFte, FechaCruce, FactProvee, FecEntrega, CostoTtal, VrBruto, VrDesc,
                VrIva, VrReteIva, VrReteIca, VrNeto, VrBaseImp, Direccion, FecMod
            FROM ConDocume cd
            WHERE (IdCompro ='0031' OR IdCompro ='0039' OR IdCompro ='0065') AND FecMod > '{fecha_formateada}'
            ORDER BY FecMod DESC
            """
        print(query_xirux)
        results_xirux = self.get_results_xirux(query_xirux)
        for result in results_xirux:
            IdOperac = result[1]
            Numero = result[2]
            Fecha = result[3]
            FecContab = result[4]
            FecVen = result[5]
            IdTercer = result[6]
            IdActICA = result[7]
            IdRetFte = result[8]
            VlrRetFte = result[9]
            FechaCruce = result[10]
            FactProvee = result[11]
            FecEntrega = result[12]
            CostoTtal = result[13]
            VrBruto = result[14]
            VrDesc = result[15]
            VrIva = result[16]
            VrReteIva = result[17]
            VrReteIca = result[18]
            VrNeto = result[19]
            VrBaseImp = result[20]
            Direccion = result[21]
            FecMod = result[22]
            # Insert into integration app
            if PurchaseOrder.objects.filter(Numero=Numero).count() == 0:
                purchase = PurchaseOrder.objects.create(
                    IdOperac=IdOperac,
                    Numero=Numero,
                    Fecha=Fecha,
                    FecContab=FecContab,
                    FecVen=FecVen,
                    IdTercer=IdTercer,
                    IdActICA=IdActICA,
                    IdRetFte=IdRetFte,
                    VlrRetFte=VlrRetFte,
                    FechaCruce=FechaCruce,
                    FactProvee=FactProvee,
                    FecEntrega=FecEntrega,
                    CostoTtal=CostoTtal,
                    VrBruto=VrBruto,
                    VrDesc=VrDesc,
                    VrIva=VrIva,
                    VrReteIva=VrReteIva,
                    VrReteIca=VrReteIca,
                    VrNeto=VrNeto,
                    VrBaseImp=VrBaseImp,
                    Direccion=Direccion,
                    FecMod=FecMod,
                )
                # print(f"Purchase order {Numero} created")
            else:
                purchase = PurchaseOrder.objects.filter(Numero=Numero).update(
                    IdOperac=IdOperac,
                    Fecha=Fecha,
                    FecContab=FecContab,
                    FecVen=FecVen,
                    IdTercer=IdTercer,
                    IdActICA=IdActICA,
                    IdRetFte=IdRetFte,
                    VlrRetFte=VlrRetFte,
                    FechaCruce=FechaCruce,
                    FactProvee=FactProvee,
                    FecEntrega=FecEntrega,
                    CostoTtal=CostoTtal,
                    VrBruto=VrBruto,
                    VrDesc=VrDesc,
                    VrIva=VrIva,
                    VrReteIva=VrReteIva,
                    VrReteIca=VrReteIca,
                    VrNeto=VrNeto,
                    VrBaseImp=VrBaseImp,
                    Direccion=Direccion,
                    FecMod=FecMod,
                )
                # print(f"Purchase order {Numero} updated")
            purchase = PurchaseOrder.objects.filter(Numero=Numero).first()
            IdOperac = purchase.IdOperac
            Numero = purchase.Numero

            Fecha = purchase.Fecha
            # fecha_objeto = datetime.strptime(FechaString, "%Y-%m-%d %H:%M:%S")
            # Fecha = fecha_objeto.date()

            FecContab = purchase.FecContab
            # fecha_objeto = datetime.strptime(FecContabString, "%Y-%m-%d %H:%M:%S")
            # FecContab = fecha_objeto.date()

            FecVen = purchase.FecVen
            # fecha_objeto = datetime.strptime(FecVenString, "%Y-%m-%d %H:%M:%S")
            # FecVen = fecha_objeto.date()

            IdTercer = purchase.IdTercer
            IdActICA = purchase.IdActICA
            IdRetFte = purchase.IdRetFte

            if purchase.VlrRetFte is None:
                VlrRetFte = 0
            else:
                VlrRetFte = float(purchase.VlrRetFte)

            FechaCruce = purchase.FechaCruce
            # fecha_objeto = datetime.strptime(FechaCruceString, "%Y-%m-%d %H:%M:%S")
            # FechaCruce = fecha_objeto.date()

            FactProvee = purchase.FactProvee

            FecEntrega = purchase.FecEntrega
            # fecha_objeto = datetime.strptime(FecEntregaString, "%Y-%m-%d %H:%M:%S")
            # FecEntrega = fecha_objeto.date()

            if purchase.CostoTtal is None:
                CostoTtal = 0
            else:
                CostoTtal = float(purchase.CostoTtal)

            if purchase.VrBruto is None:
                VrBruto = 0
            else:
                VrBruto = float(purchase.VrBruto)

            if purchase.VrDesc is None:
                VrDesc = 0
            else:
                VrDesc = float(purchase.VrDesc)

            if purchase.VrIva is None:
                VrIva = 0
            else:
                VrIva = float(purchase.VrIva)

            if purchase.VrReteIva is None:
                VrReteIva
            else:
                VrReteIva = float(purchase.VrReteIva)

            if purchase.VrReteIca is None:
                VrReteIca = 0
            else:
                VrReteIca = float(purchase.VrReteIca)

            if purchase.VrNeto is None:
                VrNeto = 0
            else:
                VrNeto = float(purchase.VrNeto)

            if purchase.VrBaseImp is None:
                VrBaseImp = 0
            else:
                VrBaseImp = float(purchase.VrBaseImp)

            Direccion = purchase.Direccion

            FecMod = purchase.FecMod
            # FecModStringSplit = FecModString.split(".")
            # fecha_objeto = datetime.strptime(FecModStringSplit[0], "%Y-%m-%d %H:%M:%S")
            # FecMod = fecha_objeto.date()

            if SicopPurchaseOrder.objects.filter(Numero=Numero).count() == 0:
                SicopPurchaseOrder.objects.create(
                    IdOperac=IdOperac,
                    Numero=Numero,
                    Fecha=Fecha,
                    FecContab=FecContab,
                    FecVen=FecVen,
                    IdTercer=IdTercer,
                    IdActICA=IdActICA,
                    IdRetFte=IdRetFte,
                    VlrRetFte=VlrRetFte,
                    FechaCruce=FechaCruce,
                    FactProvee=FactProvee,
                    FecEntrega=FecEntrega,
                    CostoTtal=CostoTtal,
                    VrBruto=VrBruto,
                    VrDesc=VrDesc,
                    VrIva=VrIva,
                    VrReteIva=VrReteIva,
                    VrReteIca=VrReteIca,
                    VrNeto=VrNeto,
                    VrBaseImp=VrBaseImp,
                    Direccion=Direccion,
                    FecMod=FecMod,
                )
                # print(f"Purchase order {Numero} created")
            else:
                SicopPurchaseOrder.objects.filter(Numero=Numero).update(
                    IdOperac=IdOperac,
                    # Fecha=Fecha,
                    FecContab=FecContab,
                    FecVen=FecVen,
                    IdTercer=IdTercer,
                    IdActICA=IdActICA,
                    IdRetFte=IdRetFte,
                    VlrRetFte=VlrRetFte,
                    FechaCruce=FechaCruce,
                    FactProvee=FactProvee,
                    FecEntrega=FecEntrega,
                    CostoTtal=CostoTtal,
                    VrBruto=VrBruto,
                    VrDesc=VrDesc,
                    VrIva=VrIva,
                    VrReteIva=VrReteIva,
                    VrReteIca=VrReteIca,
                    VrNeto=VrNeto,
                    VrBaseImp=VrBaseImp,
                    Direccion=Direccion,
                    FecMod=FecMod,
                )
                # print(f"Purchase order {Numero} updated")

    def check_ping(self):
        hostname = f"{self.xirux_host}"
        response = os.system("ping -c 1 " + hostname)
        # and then check the response...
        if response == 0:
            pingstatus = True
        else:
            pingstatus = False
        return pingstatus

    def ping_ok(self) -> bool:
        sHost = f"{self.xirux_host}"
        try:
            subprocess.check_output(
                "ping -{} 1 {}".format("n" if platform.system().lower() == "windows" else "c", sHost), shell=True
            )
        except Exception:
            return False

        return True

    def relation_cost_center_and_bussiness_unit(self):
        business_units = BusinessUnit.objects.all()
        relation = {}
        for business_unit in business_units:
            cost_centers = CostCenter.objects.filter(
                IdTipCen=business_unit.IdTipCen,
            )
            relation_temp = []
            for cost_center in cost_centers:
                relation_temp.append(cost_center.IdCenCos)
            relation[business_unit.IdTipCen] = relation_temp
        for key, value in relation.items():
            business_unit_id = key
            sicop_business_unit = SicopBusinessUnit.objects.get(
                code=business_unit_id,
            )
            sicop_business_unit.cost_centers.clear()
            for cost_center_id in value:
                sicop_business_unit.cost_centers.add(
                    SicopCostCenter.objects.get(
                        cost_center_id=cost_center_id,
                    ),
                )

    def relation_expense_concept_and_expense_type(self):
        expense_types = ExpenseType.objects.all()
        relation = {}
        for expense_type in expense_types:
            expense_concepts = ExpenseConcept.objects.filter(
                IdTipGas=expense_type.IdTipGas,
            )
            relation_temp = []
            for expense_concept in expense_concepts:
                relation_temp.append(
                    expense_concept.IdConGas,
                )
            relation[expense_type.IdTipGas] = relation_temp
        for key, value in relation.items():
            expense_type_id = key
            sicop_expense_type = SicopExpenseType.objects.get(
                code=expense_type_id,
            )
            sicop_expense_type.expense_concepts.clear()
            for expense_concept_id in value:
                sicop_expense_type.expense_concepts.add(
                    SicopExpenseConcept.objects.get(
                        code=expense_concept_id,
                    ),
                )

    def run(self):
        ping_status = self.check_ping()

        if ping_status:
            self.set_mssql_connection()
            start_at = datetime.now()
            print("============== Xirux integration start ==============", "\n")
            print("============== Business units starts ================", "\n")
            self.business_units()
            print("============== Business units ends =================", "\n")
            print("============== Cost centers starts =================", "\n")
            self.cost_centers()
            print("============== Cost centers ends ===================", "\n")
            print("============== Expense types starts at =============", "\n")
            self.expense_types()
            print("============== Expense types ends ==================", "\n")
            print("============== Thirds starts =======================", "\n")
            self.thirds()
            print("============== Thirds ends =========================", "\n")
            print("============== Purchase orders starts =======================", "\n")
            self.purchase_orders()
            print("============== Purchase orders ends =========================", "\n")
            print("============== Expense concepts starts =============", "\n")
            self.expense_concepts()
            print("============== Expense concepts ends ===============", "\n")
            print("============== contracts starts ====================", "\n")
            self.contracts()
            print("============== contracts ends ======================", "\n")
            print("=============== Xirux integration ends ==============", "\n")
            print("=============== Xirux relation start ================", "\n")
            self.relation_cost_center_and_bussiness_unit()
            self.relation_expense_concept_and_expense_type()
            print("=============== Xirux relation ends =================", "\n")
            end_at = datetime.now()
            print(f"Start at {start_at}")
            print(f"End at {end_at}")
            print(f"Total time: {end_at - start_at}")
        else:
            print("VPN is down, activating the vpn")
            cmd = "sudo openfortivpn -c /etc/openfortivpn/config > /var/log/openfortivpn/openfortivpn.log 2>&1 &"
            os.system(cmd)
            print("Waiting 10 seconds for the vpn to be ready")
            time.sleep(10)
            print("Trying again...")
            self.run()
