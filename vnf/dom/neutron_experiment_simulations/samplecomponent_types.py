typenames = [
    'neutron_experiment_simulations.neutron_components.VanadiumPlate.VanadiumPlate',
    ]


def getTypes():
    from vnf.dom import importType
    return map(importType, typenames)
