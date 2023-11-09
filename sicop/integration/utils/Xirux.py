import os
import platform
import subprocess
import time
from datetime import datetime

import pyodbc

from sicop.business_unit.models import BusinessUnit as SicopBusinessUnit
from sicop.contractor.models import Contractor as SicopContractor
from sicop.cost_center.models import CostCenter as SicopCostCenter
from sicop.expense_concept.models import ExpenseConcept as SicopExpenseConcept
from sicop.expense_type.models import ExpenseType as SicopExpenseType
from sicop.integration.models import BusinessUnit, CostCenter, ExpenseConcept, ExpenseType, Third


class XiruxIntegration:
    def __init__(self):
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

            else:
                BusinessUnit.objects.filter(IdTipCen=IdTipCen).update(
                    Nombre=Nombre,
                    Nemoni=Nemoni,
                    IdUsuari=IdUsuari,
                    Operac=Operac,
                    FecMod=FecMod,
                )

            # Insert into Business unit app
            if SicopBusinessUnit.objects.filter(code=IdTipCen).count() == 0:
                SicopBusinessUnit.objects.create(
                    code=IdTipCen,
                    name=Nombre,
                )

            else:
                SicopBusinessUnit.objects.filter(code=IdTipCen).update(
                    name=Nombre,
                )

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

            # Insert into Cost Center app
            if SicopCostCenter.objects.filter(cost_center_id=IdCenCos).count() == 0:
                SicopCostCenter.objects.create(
                    cost_center_id=IdCenCos,
                    name=Nombre,
                    description=Nombre,
                )

            else:
                SicopCostCenter.objects.filter(cost_center_id=IdCenCos).update(
                    name=Nombre,
                    description=Nombre,
                )

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

            # Insert into Expense Type app
            if SicopExpenseType.objects.filter(code=IdTipGas).count() == 0:
                SicopExpenseType.objects.create(
                    code=IdTipGas,
                    name=Nombre,
                )

            else:
                SicopExpenseType.objects.filter(code=IdTipGas).update(
                    name=Nombre,
                )

    def thirds(self):
        query_xirux = "select * from ConTercer"
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

            # Insert into Third app
            if SicopContractor.objects.filter(dni=Nit).count() == 0:
                SicopContractor.objects.create(
                    name=Nombre,
                    commertial_name=Razon,
                    dni=Nit,
                    address=Direcc,
                    phone=Telefo,
                )

            else:
                SicopContractor.objects.filter(dni=Nit).update(
                    name=Nombre,
                    commertial_name=Razon,
                    address=Direcc,
                    phone=Telefo,
                )

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

            # Insert into Expense Concept app
            if SicopExpenseConcept.objects.filter(code=IdConGas).count() == 0:
                SicopExpenseConcept.objects.create(
                    code=IdConGas,
                    name=Nombre,
                )

            else:
                SicopExpenseConcept.objects.filter(code=IdConGas).update(
                    name=Nombre,
                )

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
            print("============== Xirux integration start ==============")
            print("=====================================")
            print(f"== Business units starts at {datetime.now()} ==")
            self.business_units()
            print(f"== Business units ends at {datetime.now()} ==")
            print("=====================================")
            print(f"== Cost centers starts at {datetime.now()} ==")
            self.cost_centers()
            print(f"== Cost centers ends at {datetime.now()} ==")
            print("=====================================")
            print(f"== Expense types starts at {datetime.now()} ==")
            self.expense_types()
            print(f"== Expense types ends at {datetime.now()} ==")
            print("=====================================")
            print(f"== Thirds starts at {datetime.now()} ==")
            self.thirds()
            print(f"== Thirds ends at {datetime.now()} ==")
            print("=====================================")
            print(f"== Expense concepts starts at {datetime.now()} ==")
            self.expense_concepts()
            print(f"== Expense concepts ends at {datetime.now()} ==")
            print("============== Xirux integration ends ==============")

            print("============== Xirux relation start ==============")
            self.relation_cost_center_and_bussiness_unit()
            self.relation_expense_concept_and_expense_type()
            print("============== Xirux relation ends ==============")
        else:
            print("VPN is down, activating the vpn")
            cmd = "sudo openfortivpn -c /etc/openfortivpn/config > /var/log/openfortivpn/openfortivpn.log 2>&1 &"
            os.system(cmd)
            print("Waiting 10 seconds for the vpn to be ready")
            time.sleep(10)
            print("Trying again...")
            self.run()
