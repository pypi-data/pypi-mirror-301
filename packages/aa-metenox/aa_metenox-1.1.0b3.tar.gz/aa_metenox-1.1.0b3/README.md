# Metenox

AA module for Metenox management.

[![release](https://img.shields.io/pypi/v/aa-metenox?label=release)](https://pypi.org/project/aa-metenox/)
[![python](https://img.shields.io/pypi/pyversions/aa-metenox)](https://pypi.org/project/aa-metenox/)
[![django](https://img.shields.io/pypi/djversions/aa-metenox?label=django)](https://pypi.org/project/aa-metenox/)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/r0kym/aa-metenox/-/blob/master/LICENSE)

## Features:

- Imports moon scans from the [aa-moonmining](https://gitlab.com/ErikKalkoken/aa-moonmining) application
- Import Metenoxes from a corporation
  - Displays remaining fuel
  - Displays currently stored moon materials
- Manager overview of corporation displaying their number of Metenoxes and profit

### TODO:

- [ ] Setup notifications when the fuel/reagent levels are low

### What this app won't do:
- Estimate moon price for athanor.
  Use [aa-moonmining](https://gitlab.com/ErikKalkoken/aa-moonmining)
- Ping when metenox are being reffed
  Use [aa-structures](https://gitlab.com/ErikKalkoken/aa-structures)

This module aims to be specific for Metenox management.

### Screenshots

![moon details](images/moon_details.png)
![metenox window](images/metenox_window.png)
![metenox details](images/metenox_details.png)
![corporation window](images/corporation_window.png)

## Installation

### Step 1 - Check prerequisites

1. Metenox is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

2. Metenox requires the Alliance Auth module [aa-moonmining](https://gitlab.com/ErikKalkoken/aa-moonmining) to function.
  The moon database and other utilities are imported from this module.

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-metenox
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'metenox'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
CELERYBEAT_SCHEDULE['metenox_update_prices'] = {
    'task': 'metenox.tasks.update_prices',
    'schedule': crontab(minute='0', hour='*/12'),
}
CELERYBEAT_SCHEDULE['metenox_update_moons_from_moonmining'] = {
    'task': 'metenox.tasks.update_moons_from_moonmining',
    'schedule': crontab(minute='*/20'),
}

CELERYBEAT_SCHEDULE['metenox_update_all_holdings'] = {
    'task': 'metenox.tasks.update_all_holdings',
    'schedule': crontab(minute='0', hour='*/1')
}
```

Note: if you know you won't have moons added in the moonmining application often you can increase the delay of the `metenox_update_moons_from_moonmining` task.
You can even not use it at all and only update moon scans with the `metenox_update_moons_from_moonmining` [command](#commands).

Optional: Alter the application settings.
The list can be found in [Settings](#settings)

### Step 4 - Finalize App installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Restart your supervisor services for Auth.

### Setp 5 - Load Goo from ESI

Run the following management command to load all moon materials from ESI.
This only has to be run once.

```bash
python manage.py metenox_load_eve
```

Wait until the command is finished before continuing.

### Step 5 - Load data

First load the data from the moonmining module using
```bash
python manage.py metenox_update_moons_from_moonmining
```

Once it's done update their prices with

```bash
python manage.py metenox_update_all_prices
```

## Permissions

Permissions overview.

| Name                  | Description                                                                                              |
|-----------------------|----------------------------------------------------------------------------------------------------------|
| `view_moons`          | This permissions allow to see all scanned moons of the database                                          |
| `view_metenoxes`      | This permissions allow to add owners and see all metenoxes from the owners corporations                  |
| `corporation_manager` | This permission allows to add webhooks to corporations and edit when a corporation should get fuel pings |
| `auditor`             | This permission allows to see all metenoxes regardless of having an owner in the corporation             |

For the permissions `corporation_manager` and `auditor` to work properly the user needs to also have the `view_metenoxes` permission.

## Settings

List of settings that can be modified for the application.
You can alter them by adding them in your `local.py` file.

| Name                                 | Description                                                                                                                                        | Default |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `METENOX_ADMIN_NOTIFICATIONS_ENABLE` | Whether admins will get notifications about important events like when someone adds a new owner.                                                   | True    |
| `METENOX_MOON_MATERIAL_BAY_CAPACITY` | Volume of the Metenox's Moon material Output Bay. Used to calculate how long a metenox takes before being full.<br/>This value shouldn't be edited | 500_000 |
| `METENOX_HOURLY_HARVEST_VOLUME`      | Hourly volume in m3 that a metenox will harvest.<br/>This value shouldn't be edited                                                                | 30_000  |
| `METENOX_HARVEST_REPROCESS_YIELD`    | Yield at which the metenox reprocess the harvested materials.<br/>This value shouldn't be edited                                                   | 0.40    |
| `METENOX_FUEL_BLOCKS_PER_HOUR`       | How many fuel blocks a running Metenox consumes every hours.<br/>This value shouldn't be edited                                                    | 5       |
| `METENOX_MAGMATIC_GASES_PER_HOUR`    | How many magmatic gases a running Metenox consumes every hours.<br/>This value shouldn't be edited                                                 | 88      |


## Commands

The following commands can be used when running the module:

| Name                                   | Description                                                                   |
|----------------------------------------|-------------------------------------------------------------------------------|
| `metenox_load_eve`                     | Loads up the data from `eveuniverse` this command should only be ran once     |
| `metenox_update_all_holdings`          | Fetches all holdings in the database and updates their metenoxes with the ESI |
| `metenox_update_all_prices`            | Fetches new prices from fuzzwork and update the price of all known moons      |
| `metenox_update_moons_from_moonmining` | Checks the moonmining application and adds all missing moons                  |
