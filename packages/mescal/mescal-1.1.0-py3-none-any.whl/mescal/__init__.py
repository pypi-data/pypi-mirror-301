"""mescal."""

__all__ = (
    "__version__",
    # Add functions and variables you want exposed in `mescal.` namespace here

    # esm.py
    "ESM",

    # database.py
    "Database",
    "Dataset",

    # utils.py
    "random_code",
    "ecoinvent_unit_convention",
    "change_mapping_year",

    # change_ecoinvent.py
    "change_ecoinvent_version_mapping",
    "update_unit_conversion_file",

    # modify_inventory.py
    "change_dac_biogenic_carbon_flow",
    "change_fossil_carbon_flows_of_biofuels",
    "remove_quebec_flow_in_global_heat_market",
    "change_direct_carbon_emissions_by_factor",
    "add_carbon_dioxide_flow",
)

__version__ = "1.1.0"

from .database import Database, Dataset
from .esm import ESM
from .utils import *
from .change_ecoinvent import *
from .modify_inventory import *
