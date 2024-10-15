"""
Utilities for calculating CO2 emissions based on changes in carbon stocks (e.g., `organicCarbonPerHa`,
`aboveGroundBiomass` and `belowGroundBiomass`).
"""

from datetime import datetime
from enum import Enum
from functools import reduce
from itertools import product
from numpy import array, random, mean
from numpy.typing import NDArray
from pydash.objects import merge
from typing import NamedTuple, Optional, Union

from hestia_earth.schema import EmissionMethodTier, MeasurementMethodClassification
from hestia_earth.utils.date import diff_in_days, YEAR
from hestia_earth.utils.tools import flatten, non_empty_list, safe_parse_date

from hestia_earth.models.log import log_as_table
from hestia_earth.models.utils import pairwise
from hestia_earth.models.utils.array_builders import correlated_normal_2d
from hestia_earth.models.utils.blank_node import (
    _gapfill_datestr, DatestrGapfillMode, group_nodes_by_year, split_node_by_dates
)
from hestia_earth.models.utils.constant import Units, get_atomic_conversion
from hestia_earth.models.utils.emission import min_emission_method_tier
from hestia_earth.models.utils.measurement import (
    group_measurements_by_method_classification, min_measurement_method_classification,
    to_measurement_method_classification
)
from hestia_earth.models.utils.time_series import (
    calc_tau, compute_time_series_correlation_matrix, exponential_decay
)

_MAX_CORRELATION = 1
_MIN_CORRELATION = 0.5
_NOMINAL_ERROR = 75
"""
carbon stock measurements without an associated `sd` should be assigned a nominal error of 75% (2*sd as a percentage of
the mean).
"""
_TRANSITION_PERIOD = 20 * YEAR  # 20 years in days
_VALID_MEASUREMENT_METHOD_CLASSIFICATIONS = [
    MeasurementMethodClassification.ON_SITE_PHYSICAL_MEASUREMENT,
    MeasurementMethodClassification.MODELLED_USING_OTHER_MEASUREMENTS,
    MeasurementMethodClassification.TIER_3_MODEL,
    MeasurementMethodClassification.TIER_2_MODEL,
    MeasurementMethodClassification.TIER_1_MODEL
]
"""
The list of `MeasurementMethodClassification`s that can be used to calculate carbon stock change emissions, ranked in
order from strongest to weakest.
"""


class _InventoryKey(Enum):
    """
    The inner keys of the annualised inventory created by the `_compile_inventory` function.

    The value of each enum member is formatted to be used as a column header in the `log_as_table` function.
    """
    CARBON_STOCK = "carbon-stock"
    CARBON_STOCK_CHANGE = "carbon-stock-change"
    CO2_EMISSION = "carbon-emission"
    SHARE_OF_EMISSION = "share-of-emissions"


CarbonStock = NamedTuple("CarbonStock", [
    ("value", NDArray),
    ("date", str),
    ("method", MeasurementMethodClassification)
])
"""
NamedTuple representing a carbon stock (e.g., `organicCarbonPerHa` or `aboveGroundBiomass`).

Attributes
----------
value : NDArray
    The value of the carbon stock measurement (kg C ha-1).
date : str
    The date of the measurement as a datestr with the format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ss`.
method: MeasurementMethodClassification
    The measurement method for the carbon stock.
"""


CarbonStockChange = NamedTuple("CarbonStockChange", [
    ("value", NDArray),
    ("start_date", str),
    ("end_date", str),
    ("method", MeasurementMethodClassification)
])
"""
NamedTuple representing a carbon stock change.

Attributes
----------
value : NDArray
    The value of the carbon stock change (kg C ha-1).
start_date : str
    The start date of the carbon stock change event as a datestr with the format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or
    `YYYY-MM-DDTHH:mm:ss`.
end_date : str
    The end date of the carbon stock change event as a datestr with the format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or
    `YYYY-MM-DDTHH:mm:ss`.
method: MeasurementMethodClassification
    The measurement method for the carbon stock change.
"""


CarbonStockChangeEmission = NamedTuple("CarbonStockChangeEmission", [
    ("value", NDArray),
    ("start_date", str),
    ("end_date", str),
    ("method", EmissionMethodTier)
])
"""
NamedTuple representing a carbon stock change emission.

Attributes
----------
value : NDArray
    The value of the carbon stock change emission (kg CO2 ha-1).
start_date : str
    The start date of the carbon stock change emission as a datestr with the format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or
    `YYYY-MM-DDTHH:mm:ss`.
end_date : str
    The end date of the carbon stock change emission as a datestr with the format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or
    `YYYY-MM-DDTHH:mm:ss`.
method: MeasurementMethodClassification
    The emission method tier.
"""


def lerp_carbon_stocks(start: CarbonStock, end: CarbonStock, target_date: str) -> CarbonStock:
    """
    Estimate, using linear interpolation, a carbon stock for a specific date based on the carbon stocks of two other
    dates.

    Parameters
    ----------
    start : CarbonStock
        The `CarbonStock` at the start (kg C ha-1).
    end : CarbonStock
        The `CarbonStock` at the end (kg C ha-1).
    target_date : str
        The target date for interpolation as a datestr with format `YYYY`, `YYYY-MM`, `YYYY-MM-DD` or
    `YYYY-MM-DDTHH:mm:ss`.

    Returns
    -------
    CarbonStock
        The interpolated `CarbonStock` for the specified date (kg C ha-1).
    """
    alpha = diff_in_days(start.date, target_date) / diff_in_days(start.date, end.date)
    value = (1 - alpha) * start.value + alpha * end.value
    method = min_measurement_method_classification(start.method, end.method)
    return CarbonStock(value, target_date, method)


def calc_carbon_stock_change(start: CarbonStock, end: CarbonStock) -> CarbonStockChange:
    """
    Calculate the change in a carbon stock between two different dates.

    The method should be the weaker of the two `MeasurementMethodClassification`s.

    Parameters
    ----------
    start : CarbonStock
        The carbon stock at the start (kg C ha-1).
    end : CarbonStock
        The carbon stock at the end (kg C ha-1).

    Returns
    -------
    CarbonStockChange
        The carbon stock change (kg C ha-1).
    """
    value = end.value - start.value
    method = min_measurement_method_classification(start.method, end.method)
    return CarbonStockChange(value, start.date, end.date, method)


def calc_carbon_stock_change_emission(carbon_stock_change: CarbonStockChange) -> CarbonStockChangeEmission:
    """
    Convert a `CarbonStockChange` into a `CarbonStockChangeEmission`.

    Parameters
    ----------
    carbon_stock_change : CarbonStockChange
        The carbon stock change (kg C ha-1).

    Returns
    -------
    CarbonStockChangeEmission
        The carbon stock change emission (kg CO2 ha-1).
    """
    value = _convert_c_to_co2(carbon_stock_change.value) * -1
    method = _convert_mmc_to_emt(carbon_stock_change.method)
    return CarbonStockChangeEmission(value, carbon_stock_change.start_date, carbon_stock_change.end_date, method)


def _convert_mmc_to_emt(
    measurement_method_classification: MeasurementMethodClassification
) -> EmissionMethodTier:
    """
    Get the emission method tier based on the provided measurement method classification.

    Parameters
    ----------
    measurement_method_classification : MeasurementMethodClassification
        The measurement method classification to convert into the corresponding emission method tier.

    Returns
    -------
    EmissionMethodTier
        The corresponding emission method tier.
    """
    return _MEASUREMENT_METHOD_CLASSIFICATION_TO_EMISSION_METHOD_TIER.get(
        to_measurement_method_classification(measurement_method_classification),
        _DEFAULT_EMISSION_METHOD_TIER
    )


_DEFAULT_EMISSION_METHOD_TIER = EmissionMethodTier.TIER_1
_MEASUREMENT_METHOD_CLASSIFICATION_TO_EMISSION_METHOD_TIER = {
    MeasurementMethodClassification.TIER_2_MODEL: EmissionMethodTier.TIER_2,
    MeasurementMethodClassification.TIER_3_MODEL: EmissionMethodTier.TIER_3,
    MeasurementMethodClassification.MODELLED_USING_OTHER_MEASUREMENTS: EmissionMethodTier.MEASURED,
    MeasurementMethodClassification.ON_SITE_PHYSICAL_MEASUREMENT: EmissionMethodTier.MEASURED,
}
"""
A mapping between `MeasurementMethodClassification`s and `EmissionMethodTier`s. As carbon stock measurements can be
measured/estimated through a variety of methods, the emission model needs be able to assign an emission tier for each.
Any `MeasurementMethodClassification` not in the mapping should be assigned `DEFAULT_EMISSION_METHOD_TIER`.
"""


def _convert_c_to_co2(kg_c: float) -> float:
    """
    Convert mass of carbon (C) to carbon dioxide (CO2) using the atomic conversion ratio.

    n.b. `get_atomic_conversion` returns the ratio C:CO2 (~44/12).

    Parameters
    ----------
    kg_c : float
        Mass of carbon (C) to be converted to carbon dioxide (CO2) (kg C).

    Returns
    -------
    float
        Mass of carbon dioxide (CO2) resulting from the conversion (kg CO2).
    """
    return kg_c * get_atomic_conversion(Units.KG_CO2, Units.TO_C)


def rescale_carbon_stock_change_emission(
    emission: CarbonStockChangeEmission, factor: float
) -> CarbonStockChangeEmission:
    """
    Rescale a `CarbonStockChangeEmission` by a specified factor.

    Parameters
    ----------
    emission : CarbonStockChangeEmission
        A carbon stock change emission (kg CO2 ha-1).
    factor : float
        A scaling factor, representing a proportion of the total emission as a decimal. (e.g., a
        [Cycles](https://www.hestia.earth/schema/Cycle)'s share of an annual emission).

    Returns
    -------
    CarbonStockChangeEmission
        The rescaled emission.
    """
    value = emission.value * factor
    return CarbonStockChangeEmission(value, emission.start_date, emission.end_date, emission.method)


def add_carbon_stock_change_emissions(
    emission_1: CarbonStockChangeEmission, emission_2: CarbonStockChangeEmission
) -> CarbonStockChangeEmission:
    """
    Sum together multiple `CarbonStockChangeEmission`s.

    Parameters
    ----------
    emission_1 : CarbonStockChangeEmission
        A carbon stock change emission (kg CO2 ha-1).
    emission_2 : CarbonStockChangeEmission
        A carbon stock change emission (kg CO2 ha-1).

    Returns
    -------
    CarbonStockChangeEmission
        The summed emission.
    """
    value = emission_1.value + emission_2.value
    start_date = min(emission_1.start_date, emission_2.start_date)
    end_date = max(emission_1.end_date, emission_2.end_date)
    method = min_emission_method_tier(emission_1.method, emission_2.method)

    return CarbonStockChangeEmission(value, start_date, end_date, method)


def compile_inventory(
    cycle_id: str,
    cycles: list[dict],
    carbon_stock_measurements: list[dict],
    iterations: int = 10000,
    seed: Union[int, random.Generator, None] = None
) -> tuple[dict, dict]:
    """
    Compile an annual inventory of carbon stocks, changes in carbon stocks, carbon stock change emissions, and the share
    of emissions of cycles based on the provided cycles and measurement data.

    A separate inventory is compiled for each valid `MeasurementMethodClassification` present in the data, and the
    strongest available method is chosen for each relevant inventory year. These inventories are then merged into one
    final result.

    The final inventory structure is:
    ```
    {
        year (int): {
            _InventoryKey.CARBON_STOCK: value (CarbonStock),
            _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
            _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission),
            _InventoryKey.SHARE_OF_EMISSION: {
                cycle_id (str): value (float),
                ...cycle_ids
            }
        },
        ...years
    }
    ```

    Parameters
    ----------
    cycle_id : str
        The unique identifier of the cycle being processed.
    cycles : list[dict]
        A list of cycle data dictionaries, each representing land management events or cycles, grouped by years.
    carbon_stock_measurements: list[dict]
        A list of dictionaries, each representing carbon stock measurements across time and methods.
    iterations : int, optional
        The number of iterations for stochastic processing (default is 10,000).
    seed : int, random.Generator, or None, optional
        Seed for random number generation to ensure reproducibility. Default is None.


    Returns
    -------
    tuple[dict, dict]
        `(inventory, logs)`
    """
    # Process cycles and carbon stock measurements independently
    cycle_inventory = _compile_cycle_inventory(cycles)
    carbon_stock_inventory = _compile_carbon_stock_inventory(
        carbon_stock_measurements, iterations=iterations, seed=seed
    )

    # Generate logs without side-effects
    logs = _generate_logs(cycle_inventory, carbon_stock_inventory)

    # Combine the inventories functionally
    inventory = _squash_inventory(cycle_id, cycle_inventory, carbon_stock_inventory)

    return inventory, logs


def _compile_cycle_inventory(cycles: list[dict]) -> dict:
    """
    Calculate grouped share of emissions for cycles based on the amount they contribute the the overall land management
    of an inventory year.

    This function groups cycles by year, then calculates the share of emissions for each cycle based on the
    `fraction_of_group_duration` value. The share of emissions is normalized by the sum of cycle occupancies for the
    entire dataset to ensure the values represent a valid share.

    The returned inventory has the shape:
    ```
    {
        year (int): {
            _InventoryKey.SHARE_OF_EMISSION: {
                cycle_id (str): value (float),
                ...cycle_ids
            }
        },
        ...more years
    }
    ```

    Parameters
    ----------
    cycles : list[dict]
        List of [Cycle nodes](https://www.hestia.earth/schema/Cycle), where each cycle dictionary should contain a
        "fraction_of_group_duration" key added by the `group_nodes_by_year` function.
    iterations : int, optional
        Number of iterations for stochastic sampling when processing carbon stock values (default is 10,000).
    seed : int, random.Generator, or None, optional
        Seed for random number generation (default is None).

    Returns
    -------
    dict
        A dictionary with grouped share of emissions for each cycle based on the fraction of the year.
    """
    grouped_cycles = group_nodes_by_year(cycles)

    def calculate_emissions(cycles_in_year):
        total_fraction = sum(c.get("fraction_of_group_duration", 0) for c in cycles_in_year)
        return {
            cycle["@id"]: cycle.get("fraction_of_group_duration", 0) / total_fraction
            for cycle in cycles_in_year
        }

    return {
        year: {_InventoryKey.SHARE_OF_EMISSION: calculate_emissions(cycles_in_year)}
        for year, cycles_in_year in grouped_cycles.items()
    }


def _compile_carbon_stock_inventory(
    carbon_stock_measurements: list[dict],
    iterations: int = 10000,
    seed: Union[int, random.Generator, None] = None
) -> dict:
    """
    Compile an annual inventory of carbon stock data and pre-computed carbon stock change emissions.

    Carbon stock measurements are grouped by the method used (MeasurementMethodClassification). For each method,
    carbon stocks are processed for each year and changes between years are computed, followed by the calculation of
    CO2 emissions.

    The returned inventory has the shape:
    ```
    {
        method (MeasurementMethodClassification): {
            year (int): {
                _InventoryKey.CARBON_STOCK: value (CarbonStock),
                _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
                _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission)
            },
            ...more years
        }
        ...more methods
    }
    ```

    Parameters
    ----------
    carbon_stock_measurements : list[dict]
        List of carbon [Measurement nodes](https://www.hestia.earth/schema/Measurement) nodes.
    iterations : int, optional
        Number of iterations for stochastic sampling when processing carbon stock values (default is 10,000).
    seed : int, random.Generator, or None, optional
        Seed for random number generation (default is None).

    Returns
    -------
    dict
        The carbon stock inventory grouped by measurement method classification.
    """
    carbon_stock_measurements_by_method = group_measurements_by_method_classification(carbon_stock_measurements)

    return {
        method: _process_carbon_stock_measurements(measurements, iterations=iterations, seed=seed)
        for method, measurements in carbon_stock_measurements_by_method.items()
    }


def _process_carbon_stock_measurements(
    carbon_stock_measurements: list[dict],
    iterations: int = 10000,
    seed: Union[int, random.Generator, None] = None
) -> dict:
    """
    Process carbon stock measurements to compile an annual inventory of carbon stocks, carbon stock changes, and CO2
    emissions. The inventory is built by interpolating between measured values and calculating changes across years.

    The returned inventory has the shape:
    ```
    {
        year (int): {
            _InventoryKey.CARBON_STOCK: value (CarbonStock),
            _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
            _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission)
        },
        ...more years
    }
    ```

    Parameters
    ----------
    carbon_stock_measurements : list[dict]
        List of pre-validated carbon stock [Measurement nodes](https://www.hestia.earth/schema/Measurement).
    iterations : int, optional
        Number of iterations for stochastic sampling when processing carbon stock values (default is 10,000).
    seed : int, random.Generator, or None, optional
        Seed for random number generation (default is None).

    Returns
    -------
    dict
        The annual inventory.
    """
    carbon_stocks = _preprocess_carbon_stocks(carbon_stock_measurements, iterations, seed)

    carbon_stocks_by_year = _interpolate_carbon_stocks(carbon_stocks)
    carbon_stock_changes_by_year = _calculate_stock_changes(carbon_stocks_by_year)
    co2_emissions_by_year = _calculate_co2_emissions(carbon_stock_changes_by_year)

    return _sorted_merge(carbon_stocks_by_year, carbon_stock_changes_by_year, co2_emissions_by_year)


def _preprocess_carbon_stocks(
    carbon_stock_measurements: list[dict],
    iterations: int = 10000,
    seed: Union[int, random.Generator, None] = None
) -> list[CarbonStock]:
    """
    Pre-process a list of carbon stock measurements by normalizing and sorting them by date. The measurements are used
    to create correlated samples using stochastic sampling methods.

    The carbon stock measurements are processed to fill in any gaps in data (e.g., missing standard deviations), and
    correlated samples are drawn to handle measurement uncertainty.

    Parameters
    ----------
    carbon_stock_measurements : list[dict]
        List of pre-validated carbon stock [Measurement nodes](https://www.hestia.earth/schema/Measurement).
    iterations : int, optional
        Number of iterations for stochastic sampling when processing carbon stock values (default is 10,000).
    seed : int, random.Generator, or None, optional
        Seed for random number generation (default is None).

    Returns
    -------
    list[CarbonStock]
        A list of carbon stocks sorted by date.
    """
    sorted_measurements = sorted(
        flatten([split_node_by_dates(m) for m in carbon_stock_measurements]),
        key=lambda node: _gapfill_datestr(node["dates"][0], DatestrGapfillMode.END)
    )

    values = flatten(node["value"] for node in sorted_measurements)

    sds = flatten(
        node.get("sd", []) or [_calc_nominal_sd(v, _NOMINAL_ERROR) for v in node["value"]]
        for node in sorted_measurements
    )

    dates = flatten(
        [_gapfill_datestr(datestr, DatestrGapfillMode.END) for datestr in node["dates"]]
        for node in sorted_measurements
    )

    methods = flatten(
        [MeasurementMethodClassification(node.get("methodClassification")) for _ in node["value"]]
        for node in sorted_measurements
    )

    correlation_matrix = compute_time_series_correlation_matrix(
        dates,
        decay_fn=lambda dt: exponential_decay(
            dt,
            tau=calc_tau(_TRANSITION_PERIOD),
            initial_value=_MAX_CORRELATION,
            final_value=_MIN_CORRELATION
        )
    )

    correlated_samples = correlated_normal_2d(
        iterations,
        array(values),
        array(sds),
        correlation_matrix,
        seed=seed
    )

    return [
        CarbonStock(value=sample, date=date, method=method)
        for sample, date, method in zip(correlated_samples, dates, methods)
    ]


def _calc_nominal_sd(value: float, error: float) -> float:
    """
    Calculate a nominal SD for a carbon stock measurement. Can be used to gap fill SD when information not present in
    measurement node.
    """
    return value * error / 200


def _interpolate_carbon_stocks(carbon_stocks: list[CarbonStock]) -> dict:
    """
    Interpolate between carbon stock measurements to estimate annual carbon stocks.

    The function takes a list of carbon stock measurements and interpolates between pairs of consecutive measurements
    to estimate the carbon stock values for each year in between.

    The returned dictionary has the format:
    ```
    {
        year (int): {
            _InventoryKey.CARBON_STOCK: value (CarbonStock),
        },
        ...more years
    }
    ```
    """
    def interpolate_between(result: dict, carbon_stock_pair: tuple[CarbonStock, CarbonStock]) -> dict:
        start, end = carbon_stock_pair[0], carbon_stock_pair[1]

        start_date = safe_parse_date(start.date, datetime.min)
        end_date = safe_parse_date(end.date, datetime.min)

        should_run = (
            datetime.min != start_date != end_date
            and end_date > start_date
        )

        update = {
            year: {_InventoryKey.CARBON_STOCK: lerp_carbon_stocks(
                start,
                end,
                f"{year}-12-31T23:59:59"
            )} for year in range(start_date.year, end_date.year+1)
        } if should_run else {}

        return result | update

    return reduce(interpolate_between, pairwise(carbon_stocks), dict())


def _calculate_stock_changes(carbon_stocks_by_year: dict) -> dict:
    """
    Calculate the change in carbon stock between consecutive years.

    The function takes a dictionary of carbon stock values keyed by year and computes the difference between the
    carbon stock for each year and the previous year. The result is stored as a `CarbonStockChange` object.

    The returned dictionary has the format:
    ```
    {
        year (int): {
            _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
        },
        ...more years
    }
    ```
    """
    return {
        year: {
            _InventoryKey.CARBON_STOCK_CHANGE: calc_carbon_stock_change(
                start_group[_InventoryKey.CARBON_STOCK],
                end_group[_InventoryKey.CARBON_STOCK]
            )
        } for (_, start_group), (year, end_group) in pairwise(carbon_stocks_by_year.items())
    }


def _calculate_co2_emissions(carbon_stock_changes_by_year: dict) -> dict:
    """
    Calculate CO2 emissions from changes in carbon stock between consecutive years.

    The function takes a dictionary of carbon stock changes and calculates the corresponding CO2 emissions for each
    year using a predefined emission factor.

    The returned dictionary has the format:
    ```
    {
        year (int): {
            _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission),
        },
        ...more years
    }
    ```
    """
    return {
        year: {
            _InventoryKey.CO2_EMISSION: calc_carbon_stock_change_emission(
                group[_InventoryKey.CARBON_STOCK_CHANGE]
            )
        } for year, group in carbon_stock_changes_by_year.items()
    }


def _sorted_merge(*sources: Union[dict, list[dict]]) -> dict:
    """
    Merge one or more dictionaries into a single dictionary, ensuring that the keys are sorted in temporal order.

    Parameters
    ----------
    *sources : dict | list[dict]
        One or more dictionaries or lists of dictionaries to be merged.

    Returns
    -------
    dict
        A new dictionary containing the merged key-value pairs, with keys sorted.
    """

    _sources = non_empty_list(
        flatten([arg if isinstance(arg, list) else [arg] for arg in sources])
    )

    merged = reduce(merge, _sources, {})
    return dict(sorted(merged.items()))


def _squash_inventory(cycle_id: str, cycle_inventory: dict, carbon_stock_inventory: dict) -> dict:
    """
    Combine the `cycle_inventory` and `carbon_stock_inventory` into a single inventory by merging data for each year
    using the strongest available `MeasurementMethodClassification`. Any years not relevant to the cycle identified
    by `cycle_id` are excluded.

    Parameters
    ----------
    cycle_id : str
        The unique identifier of the cycle being processed.
    cycle_inventory : dict
        A dictionary representing the share of emissions for each cycle, grouped by year.
        Format:
        ```
        {
            year (int): {
                _InventoryKey.SHARE_OF_EMISSION: {
                    cycle_id (str): value (float),
                    ...other cycle_ids
                }
            },
            ...more years
        }
        ```
    carbon_stock_inventory : dict
        A dictionary representing carbon stock and emissions data grouped by measurement method and year.
        Format:
        ```
        {
            method (MeasurementMethodClassification): {
                year (int): {
                    _InventoryKey.CARBON_STOCK: value (CarbonStock),
                    _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
                    _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission)
                },
                ...more years
            },
            ...more methods
        }
        ```

    Returns
    -------
    dict
        A combined inventory that merges cycle and carbon stock inventories for relevant years and cycles.
        The resulting structure is:
        ```
        {
            year (int): {
                _InventoryKey.CARBON_STOCK: value (CarbonStock),
                _InventoryKey.CARBON_STOCK_CHANGE: value (CarbonStockChange),
                _InventoryKey.CO2_EMISSION: value (CarbonStockChangeEmission),
                _InventoryKey.SHARE_OF_EMISSION: {
                    cycle_id (str): value (float),
                    ...other cycle_ids
                }
            },
            ...more years
        }
        ```
    """
    inventory_years = sorted(set(non_empty_list(
        flatten(list(years) for years in carbon_stock_inventory.values())
        + list(cycle_inventory.keys())
    )))

    def should_run_group(method: MeasurementMethodClassification, year: int) -> bool:
        carbon_stock_inventory_group = carbon_stock_inventory.get(method, {}).get(year, {})
        share_of_emissions_group = cycle_inventory.get(year, {})

        has_emission = _InventoryKey.CO2_EMISSION in carbon_stock_inventory_group.keys()
        is_relevant_for_cycle = cycle_id in share_of_emissions_group.get(_InventoryKey.SHARE_OF_EMISSION, {}).keys()
        return all([has_emission, is_relevant_for_cycle])

    def squash(result: dict, year: int) -> dict:
        update_dict = next(
            (
                {year: reduce(merge, [carbon_stock_inventory[method][year], cycle_inventory[year]], dict())}
                for method in _VALID_MEASUREMENT_METHOD_CLASSIFICATIONS if should_run_group(method, year)
            ),
            {}
        )
        return result | update_dict

    return reduce(squash, inventory_years, dict())


def _generate_logs(cycle_inventory: dict, carbon_stock_inventory: dict) -> dict:
    """
    Generate logs for the compiled inventory, providing details about cycle and carbon inventories.

    Parameters
    ----------
    cycle_inventory : dict
        The compiled cycle inventory.
    carbon_stock_inventory : dict
        The compiled carbon stock inventory.

    Returns
    -------
    dict
        A dictionary containing formatted log entries for cycle and carbon inventories.
    """
    logs = {
        "cycle_inventory": _format_cycle_inventory(cycle_inventory),
        "carbon_stock_inventory": _format_carbon_stock_inventory(carbon_stock_inventory),
    }
    return logs


def _format_cycle_inventory(cycle_inventory: dict) -> str:
    """
    Format the cycle inventory for logging as a table. Rows represent inventory years, columns represent the share of
    emission for each cycle present in the inventory. If the inventory is invalid, return `"None"` as a string.
    """
    KEY = _InventoryKey.SHARE_OF_EMISSION

    unique_cycles = sorted(
        set(non_empty_list(flatten(list(group[KEY]) for group in cycle_inventory.values()))),
        key=lambda id: next((year, id) for year in cycle_inventory if id in cycle_inventory[year][KEY])
    )

    should_run = cycle_inventory and len(unique_cycles) > 0

    return log_as_table(
        {
            "year": year,
            **{
                id: _format_number(group.get(KEY, {}).get(id, 0)) for id in unique_cycles
            }
        } for year, group in cycle_inventory.items()
    ) if should_run else "None"


def _format_carbon_stock_inventory(carbon_stock_inventory: dict) -> str:
    """
    Format the carbon stock inventory for logging as a table. Rows represent inventory years, columns represent carbon
    stock change data for each measurement method classification present in inventory. If the inventory is invalid,
    return `"None"` as a string.
    """
    KEYS = [
        _InventoryKey.CARBON_STOCK,
        _InventoryKey.CARBON_STOCK_CHANGE,
        _InventoryKey.CO2_EMISSION
    ]

    methods = carbon_stock_inventory.keys()
    method_columns = list(product(methods, KEYS))
    inventory_years = sorted(set(non_empty_list(flatten(list(years) for years in carbon_stock_inventory.values()))))

    should_run = carbon_stock_inventory and len(inventory_years) > 0

    return log_as_table(
        {
            "year": year,
            **{
                _format_column_header(method, key): _format_named_tuple(
                    carbon_stock_inventory.get(method, {}).get(year, {}).get(key, {})
                ) for method, key in method_columns
            }
        } for year in inventory_years
    ) if should_run else "None"


def _format_number(value: Optional[float]) -> str:
    """Format a float for logging in a table. If the value is invalid, return `"None"` as a string."""
    return f"{value:.1f}" if isinstance(value, (float, int)) else "None"


def _format_column_header(method: MeasurementMethodClassification, inventory_key: _InventoryKey) -> str:
    """
    Format a measurement method classification and inventory key for logging in a table as a column header. Replace any
    whitespaces in the method value with dashes and concatenate it with the inventory key value, which already has the
    correct format.
    """
    return "-".join([
        method.value.replace(" ", "-"),
        inventory_key.value
    ])


def _format_named_tuple(value: Optional[Union[CarbonStock, CarbonStockChange, CarbonStockChangeEmission]]) -> str:
    """
    Format a named tuple (`CarbonStock`, `CarbonStockChange` or `CarbonStockChangeEmission`) for logging in a table.
    Extract and format just the value and discard the other data. If the value is invalid, return `"None"` as a string.
    """
    return (
        _format_number(mean(value.value))
        if isinstance(value, (CarbonStock, CarbonStockChange, CarbonStockChangeEmission))
        else "None"
    )
