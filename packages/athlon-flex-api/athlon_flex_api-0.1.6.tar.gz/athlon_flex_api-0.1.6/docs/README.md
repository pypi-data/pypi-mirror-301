# Introduction

This is an unofficial API for the Athlon-Flex. The supported endpoints are found by checking network traffic while interacting with the web app. It will not expose all available endpoints, but mainly those to load available vehicles.

# Installation
Install this package using pip:
```python
pip install athlon-flex-api
```

# Getting Started
To use this package, you should start by instantiating the API client. 
```python
from athlon_flex_api import AthlonFlexApi
api = AthlonFlexApi(
    email="youremail@example.com" # Optional
    password="YourVeryStrongPassword", # Optional
    gross_yearly_income=100000, # Optional
    apply_loonheffingskorting=True, # Optional, Defaults to True
)
```
If you do not provide login details, all available vehicles will be loaded, irregarding of whether they fit your budget. If you do provide login details, only vehicles available for you will be shown. You can optionally provide an (approximation) of your yearly gross income, and whether you apply [loonheffingskorting](https://www.belastingdienst.nl/wps/wcm/connect/nl/jongeren/content/hoe-werkt-loonheffingskorting). These two values will be used to figured the tax percentage belonging to your income. this information is included in API calls, resulting in Athlon providing a calculated Net costs of your vehicle.

# Entity Definitions
When you open the Athlon Flex Dashboard, you are presented with a grid of available cars. These cars are internally called VehicleClusters. This name makes sense, because a car is actually a collection of car instances: Athlon often has several cars available of the same make and model. A VehicleCluster is therefor defined by its _make_ and _model_.
This is a **VehicleCluster** of the make _Mercedes-Benz_ and the model _A-Klasse_:
![VehicleCluster](./assets/showroom.png)
Currently, Athlon has 2 **Vehicles** in this cluster available:
![Vehicles](./assets/vehicles.png)

# Examples
## Load VehicleClusters
Use the following code to load all VehicleClusters:
```python
from athlon_flex_api.models.filters.vehicle_cluster_filter import AllVehicleClusters
from athlon_flex_api.models.vehicle_cluster import DetailLevel, VehicleClusters
vehicles_clusters: VehicleClusters = api.vehicle_clusters(
    filter_=AllVehicleClusters(), # Optional
    detail_level=DetailLevel.INCLUDE_VEHICLES, # Optional
)
print(vehicles_clusters)
```
### Filter
The filter parameter is optional. We distinguish the following possible values:
- `[Default]None` includes the filters as loaded from the users profile. This excludes any VehicleClusters that are not leasable with the budget of th user. This mimics the web app when _logged in_. If not logged in, equal to providing `AllVehicleClusters()`
- `AllVehicleClusters()` does not include any filter in the request. This mimics the web app when _not logged in_.
- `VehicleClusterFilter()` provides custom filter values. Take a look at the [VehicleClusterFilter](../src/athlon_flex_api/models/filters/vehicle_cluster_filter.py) class to check what filters are available.

### Detail level
The detail level is optional. It provides the possibility to define the level of details in the response. Loading more details requires more api calls, hence the function will take longer to complte. We distinguish the following possible values:
- `[Default]DetailLevel.INCLUDE_VEHICLE_DETAILS` loads all clusters and their vehicles. The vehicles will have all their detailed properties loaded.
- `DetailLevel.INCLUDE_VEHICLES` loads all clusters and their vehicles. The vehicles will have some basic properties loaded, but many are not.
- `DetailLevel.CLUSTER_ONLY` loads all clusters, but not their vehicles.

## Load Vehicles
With the `vehicle_cluster` function, all available data clusters and vehicles can be loaded. However, if you wish to load vehicles of a certain make and model manually, you can use the following code:
```python
from athlon_flex_api.models.vehicle import Vehicle
from athlon_flex_api.models.filters.vehicle_filter import NoFilter
    vehicles: list[Vehicle] = api.vehicles(
        make="Mercedes-Benz",
        model="A-Klasse",
    )
print(vehicles)
```
If logged in, all leasable vehicles will be returned. If not logged in, all available vehicles will be returned. 

Note that above function will load the vehicles _without extra details_. To load all available details, call the `vehicle_details` function for each vehicle:
```python
from athlon_flex_api.models.vehicle import Vehicle
vehicle_detailed: Vehicle = api.vehicle_details(vehicle)
print(vehicles)
```

### Tax Rates
Athlon provides a TaxRates endpoint, providing a list of TaxRate items. These include a description indicating the gross yearly income rates which belong to the TaxRate, and whether to include loonheffingskorting in the calculation of net prices. The TaxRate also includes the percentage of tax rate that must be paid with this income / loonheffingskorting combination. The Api uses this endpoint internally, to provide these details with other requests. This information causes the api to include net-price computations, like the `netCostPerMonthInEuro` in the [Vehicle](../src/athlon_flex_api/models/vehicle.py) class. 

The endpoint is also made available for use, using the following code snippet:
```python
from athlon_flex_api.models.tax_rate import TaxRates
tax_rates: TaxRates = api.tax_rates()
print(tax_rates)
```
### Profile
_This endpoint is not available when not logged in._

The Profile includes information about the users account, like the lease budget, address, and available kilometers per month. The API uses it internally, for example to filter the Vehicles that are leasable by the user. The endpoint exposes the profile using a cached property. Use the following code snippet:
```python
from athlon_flex_api.models.profile import Profile
profile: Profile = api.profile
print(profile)
```

# Load data asynchronously
The Api uses [aiohttp](https://docs.aiohttp.org/en/stable/index.html) to load data using [asyncio](https://docs.python.org/3/library/asyncio.html). Therefor, all functionality is made available through function suffixed with `async`. Every `async` method is also made available synchronously (as is shown in the examples above), by removing the suffix `_async`. If you would like to include the API in an asynchronnous context, it is advices to use the asynchronous functionality instead. For example:
```python
import asyncio
from athlon_flex_api.api import AthlonFlexApi
from athlon_flex_api.models.vehicle_cluster import DetailLevel, VehicleClusters

async def main() -> None:
    api = AthlonFlexApi(email="youremail@example.com", password="YourVeryStrongPassword")
    vehicle_clusters: VehicleClusters = await api.vehicle_clusters_async(
        detail_level=DetailLevel.CLUSTER_ONLY
    )
    print(vehicle_clusters)

if __name__ == "__main__":
    asyncio.run(main())
```