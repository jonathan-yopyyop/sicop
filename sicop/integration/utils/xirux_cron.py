# from sicop.contract.models import Contract

# from sicop.integration.models import CostCenter, Third
from sicop.integration.utils.Xirux import XiruxIntegration


def update_from_xirux():
    xirux = XiruxIntegration(develop=True)
    xirux.run()
