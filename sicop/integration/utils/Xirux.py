from sicop.business_unit.models import BusinessUnit as SicopBusinessUnit
from sicop.cost_center.models import CostCenter as SicopCostCenter
from sicop.expense_type.models import ExpenseType as SicopExpenseType
from sicop.integration.models import BusinessUnit, CostCenter, ExpenseType


class XiruxIntegration:
    def migrate_business_unit(self):
        busniness_unit = BusinessUnit.objects.all()
        for bu in busniness_unit:
            if SicopBusinessUnit.objects.filter(code=bu.IdTipCen).count() == 0:
                SicopBusinessUnit.objects.create(
                    code=bu.IdTipCen,
                    name=bu.Nombre,
                )
                print("Business Unit created")
            else:
                SicopBusinessUnit.objects.filter(code=bu.IdTipCen).update(
                    name=bu.Nombre,
                )
                print("Business Unit updated")

    def migrate_cost_center(self):
        cost_center = CostCenter.objects.all()
        for cc in cost_center:
            if SicopCostCenter.objects.filter(cost_center_id=cc.IdCenCos).count() == 0:
                SicopCostCenter.objects.create(
                    cost_center_id=cc.IdCenCos,
                    name=cc.Nombre,
                )
                print("Cost Center created")
            else:
                SicopCostCenter.objects.filter(cost_center_id=cc.IdCenCos).update(
                    name=cc.Nombre,
                )
                print("Cost Center updated")

    def migrate_expense_type(self):
        expense_type = ExpenseType.objects.all()
        for et in expense_type:
            if SicopExpenseType.objects.filter(code=et.IdTipGas).count() == 0:
                SicopExpenseType.objects.create(
                    code=et.IdTipGas,
                    name=et.Nombre,
                )
                print("Expense Type created")
            else:
                SicopExpenseType.objects.filter(code=et.IdTipGas).update(
                    name=et.Nombre,
                )
                print("Expense Type updated")
