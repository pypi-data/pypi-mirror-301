from functools import reduce
from numpy import random

from hestia_earth.schema import (
    CycleFunctionalUnit, EmissionMethodTier, EmissionStatsDefinition, MeasurementMethodClassification, SiteSiteType
)

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.array_builders import gen_seed
from hestia_earth.models.utils.blank_node import (
    _get_datestr_format, cumulative_nodes_term_match, DatestrFormat, node_term_match
)
from hestia_earth.models.utils.descriptive_stats import calc_descriptive_stats
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.site import related_cycles

from .co2ToAirCarbonStockChange_utils import (
    _InventoryKey, add_carbon_stock_change_emissions, compile_inventory, rescale_carbon_stock_change_emission
)
from .utils import check_consecutive
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "site": {
            "measurements": [
                {
                    "@type": "Measurement",
                    "value": "",
                    "dates": "",
                    "depthUpper": "0",
                    "depthLower": "30",
                    "term.@id": " organicCarbonPerHa"
                }
            ]
        },
        "functionalUnit": "1 ha",
        "endDate": "",
        "optional": {
            "startDate": ""
        }
    }
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "",
        "depth": "30"
    }]
}
TERM_ID = 'co2ToAirSoilOrganicCarbonStockChangeManagementChange'

_DEPTH_UPPER = 0
_DEPTH_LOWER = 30
_ITERATIONS = 10000

_ORGANIC_CARBON_PER_HA_TERM_ID = 'organicCarbonPerHa'

_VALID_DATE_FORMATS = {
    DatestrFormat.YEAR,
    DatestrFormat.YEAR_MONTH,
    DatestrFormat.YEAR_MONTH_DAY,
    DatestrFormat.YEAR_MONTH_DAY_HOUR_MINUTE_SECOND
}

_VALID_MEASUREMENT_METHOD_CLASSIFICATIONS = [
    MeasurementMethodClassification.ON_SITE_PHYSICAL_MEASUREMENT,
    MeasurementMethodClassification.MODELLED_USING_OTHER_MEASUREMENTS,
    MeasurementMethodClassification.TIER_3_MODEL,
    MeasurementMethodClassification.TIER_2_MODEL,
    MeasurementMethodClassification.TIER_1_MODEL
]
"""
The list of `MeasurementMethodClassification`s that can be used to calculate SOC stock change emissions, ranked in
order from strongest to weakest.
"""

_SITE_TYPE_SYSTEMS_MAPPING = {
    SiteSiteType.GLASS_OR_HIGH_ACCESSIBLE_COVER.value: [
        "protectedCroppingSystemSoilBased",
        "protectedCroppingSystemSoilAndSubstrateBased"
    ]
}


def _emission(
    *,
    value: list[float],
    method_tier: EmissionMethodTier,
    sd: list[float] = None,
    min: list[float] = None,
    max: list[float] = None,
    statsDefinition: str = None,
    observations: list[int] = None
) -> dict:
    """
    Create an emission node based on the provided value and method tier.

    See [Emission schema](https://www.hestia.earth/schema/Emission) for more information.

    Parameters
    ----------
    value : float
        The emission value (kg CO2 ha-1).
    sd : float
        The standard deviation (kg CO2 ha-1).
    method_tier : EmissionMethodTier
        The emission method tier.

    Returns
    -------
    dict
        The emission dictionary with keys 'depth', 'value', and 'methodTier'.
    """
    update_dict = {
        "value": value,
        "sd": sd,
        "min": min,
        "max": max,
        "statsDefinition": statsDefinition,
        "observations": observations,
        "methodTier": method_tier.value,
        "depth": _DEPTH_LOWER
    }
    emission = _new_emission(TERM_ID, MODEL) | {
        key: value for key, value in update_dict.items() if value
    }
    return emission


def _should_run(cycle: dict) -> tuple[bool, str, dict]:
    """
    Determine if calculations should run for a given [Cycle](https://www.hestia.earth/schema/Cycle) based on SOC stock
    and emissions data.

    Parameters
    ----------
    cycle : dict
        The cycle dictionary for which the calculations will be evaluated.

    Returns
    -------
    tuple[bool, str, dict]
        `(should_run, cycle_id, inventory)`
    """
    cycle_id = cycle.get("@id")
    site = _get_site(cycle)
    soc_measurements = [node for node in site.get("measurements", []) if _validate_soc_measurement(node)]
    cycles = related_cycles(site)

    seed = gen_seed(site)  # All cycles linked to the same site should be consistent
    rng = random.default_rng(seed)

    site_type = site.get("siteType")
    has_soil = site_type not in _SITE_TYPE_SYSTEMS_MAPPING or all(
        cumulative_nodes_term_match(
            cycle.get("practices", []),
            target_term_ids=_SITE_TYPE_SYSTEMS_MAPPING[site_type],
            cumulative_threshold=0
        ) for cycle in cycles
    )

    has_soc_measurements = len(soc_measurements) > 0
    has_cycles = len(cycles) > 0
    has_functional_unit_1_ha = all(cycle.get('functionalUnit') == CycleFunctionalUnit._1_HA.value for cycle in cycles)

    should_compile_inventory = all([
        has_soil,
        has_cycles,
        has_functional_unit_1_ha,
        has_soc_measurements,
    ])

    inventory, logs = (
        compile_inventory(
            cycle_id,
            cycles,
            soc_measurements,
            iterations=_ITERATIONS,
            seed=rng
        ) if should_compile_inventory else ({}, {})
    )

    has_valid_inventory = len(inventory) > 0
    has_consecutive_years = check_consecutive(inventory.keys())

    logRequirements(
        cycle, model=MODEL, term=TERM_ID,
        site_type=site_type,
        seed=seed,
        has_soil=has_soil,
        has_soc_measurements=has_soc_measurements,
        has_cycles=has_cycles,
        has_functional_unit_1_ha=has_functional_unit_1_ha,
        has_valid_inventory=has_valid_inventory,
        has_consecutive_years=has_consecutive_years,
        **logs
    )

    should_run = all([has_valid_inventory, has_consecutive_years])

    logShouldRun(cycle, MODEL, TERM_ID, should_run)

    return should_run, cycle_id, inventory


def _get_site(cycle: dict) -> dict:
    """
    Get the [Site](https://www.hestia.earth/schema/Site) data from a [Cycle](https://www.hestia.earth/schema/Cycle).

    Parameters
    ----------
    cycle : dict

    Returns
    -------
    str
    """
    return cycle.get("site", {})


def _validate_soc_measurement(node: dict) -> bool:
    """
    Validate a [Measurement](https://www.hestia.earth/schema/Measurement) to determine whether it is a valid
    `organicCarbonPerHa` node.

    Parameters
    ----------
    node : dict
        The node to be validated.

    Returns
    -------
    bool
        `True` if the node passes all validation criteria, `False` otherwise.
    """
    value = node.get("value", [])
    sd = node.get("sd", [])
    dates = node.get("dates", [])
    return all([
        node_term_match(node, _ORGANIC_CARBON_PER_HA_TERM_ID),
        node.get("depthUpper") == _DEPTH_UPPER,
        node.get("depthLower") == _DEPTH_LOWER,
        node.get("methodClassification") in (m.value for m in _VALID_MEASUREMENT_METHOD_CLASSIFICATIONS),
        len(value) > 0,
        len(value) == len(dates),
        len(sd) == 0 or len(sd) == len(value),
        all(_get_datestr_format(datestr) in _VALID_DATE_FORMATS for datestr in dates)
    ])


def _run(cycle_id: str, inventory: dict) -> list[dict]:
    """
    Calculate emissions for a specific cycle using grouped SOC stock change and share of emissions data.

    The emission method tier based on the minimum measurement method tier among the SOC stock change data in the
    grouped data.

    Parameters
    ----------
    cycle_id : str
        The "@id" field of the [Cycle node](https://www.hestia.earth/schema/Cycle).
    grouped_data : dict
        A dictionary containing grouped SOC stock change and share of emissions data.

    Returns
    -------
    list[dict]
        A list containing emission data calculated for the specified cycle.
    """
    rescaled_emissions = [
        rescale_carbon_stock_change_emission(
            group[_InventoryKey.CO2_EMISSION], group[_InventoryKey.SHARE_OF_EMISSION][cycle_id]
        ) for group in inventory.values()
    ]
    total_emission = reduce(add_carbon_stock_change_emissions, rescaled_emissions)

    descriptive_stats = calc_descriptive_stats(
        total_emission.value,
        EmissionStatsDefinition.SIMULATED,
        decimals=6
    )

    method_tier = total_emission.method
    return [_emission(method_tier=method_tier, **descriptive_stats)]


def run(cycle: dict) -> list[dict]:
    should_run, *args = _should_run(cycle)
    return _run(*args) if should_run else []
