import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility
import numpy as np

u = htm.ureg

GOLD_MOLAR_VOLUME = 1.02e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/gold

# TODO fit it ourselves  https://www.degruyter.com/document/doi/10.1515/zna-1962-0415/html
eichenauer_diffusivity = Diffusivity(
    D_0=5.60e-8 * u.m**2 * u.s**-1,
    E_D=23.6 * u.kJ * u.mol**-1,
    range=(773 * u.K, 1273 * u.K),
    source="eichenauer_messung_1962",
    isotope="H",
)


shimada_solubility = Solubility(
    S_0=7.8e1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=99.4 * u.kJ * u.mol**-1,
    range=(773 * u.K, 873 * u.K),
    source="shimada_608_2020",
    isotope="H",
    note="this was computed from the permeability of Caskey and Derrick and the diffusivity of Eichenauer",
)

data_T_mclellan = (
    np.array(
        [
            1050.0,
            997.0,
            948.0,
            939.0,
            910.0,
            878.0,
            838.0,
            805.0,
            793.0,
            777.0,
            735.0,
            693.0,
        ]
    )
    * u.degC
)  # degC Table1

data_y_mclellan = (
    np.array([2.86, 2.51, 2.23, 1.93, 1.96, 1.96, 1.66, 1.66, 1.66, 1.30, 1.27, 1.06])
    * 1e-6
)  # in at.fr. Table 1
data_y_mclellan *= 1 / GOLD_MOLAR_VOLUME * u.mol * u.m**-3 * u.Pa**-0.5

mclellan_solubility = Solubility(
    data_T=data_T_mclellan,
    data_y=data_y_mclellan,
    source="mclellan_solid_1973",
    isotope="H",
)


properties = [eichenauer_diffusivity, shimada_solubility, mclellan_solubility]

for prop in properties:
    prop.material = htm.GOLD

htm.database += properties
