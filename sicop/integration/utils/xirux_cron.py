from sicop.contract.models import Contract
from sicop.integration.models import CostCenter, Third
from sicop.integration.utils.Xirux import XiruxIntegration


def update_from_xirux():
    xirux = XiruxIntegration(develop=True)
    xirux.run()
    contracts = Contract.objects.all()
    for contract in contracts:
        print(contract.IdTercer)
        third = Third.objects.filter(IdTercer=contract.IdTercer).first()
        print(third)
        cost_center = CostCenter.objects.filter(IdCenCos=contract.IdCenCos).first()
        print(cost_center)
        contract.third = third
        contract.cost_center = cost_center
        contract.save()
