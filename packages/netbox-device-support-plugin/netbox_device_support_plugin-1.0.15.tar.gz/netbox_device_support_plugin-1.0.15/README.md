![Header-Image](docs/header.png)

# NetBox Cisco Support Plugin
----
</br>

This `README.md` documentation contains the following sections:

* [Plugin Overview](#plugin-overview)
    * [Cisco](#cisco)
    * [Fortinet](#fortinet)
    * [Pure Storage](#pure-storage)
* [Compatibility](#compatibility)
* [Installation](#installation)
* [Enable the Plugin](#enable-the-plugin)
* [Configure the Plugin](#configure-the-plugin)
    * [Mandatory Settings](#mandatory-settings)
    * [Optional Settings](#optional-settings)
* [Rebuild and Restart NetBox-Docker](#rebuild-and-restart-netbox-docker)
* [Run Database Migrations](#run-database-migrations)
* [Sync the Device Support Data](#sync-the-device-support-data)
    * [Cisco](#cisco-1)
    * [Fortinet](#fortinet-1)
    * [Pure Storage](#pure-storage-1)
* [How it works](#how-it-works)
* [Plugin Screenshots](#plugin-screenshots)
* [Languages and Tools](#languages-and-tools)

# Plugin Overview
----
</br>

## Cisco
----
</br>

This [NetBox](https://github.com/netbox-community/netbox) tracks with the data from the Cisco support APIs
the device support status, the device type EoX status as well as the recommended software release. Each
Cisco device and Cisco device type have a detail view with all data. There is also a list view with filter
options for all devices or device types. All data can also be received and updated over the NetBox REST API.

There is a Python script calles `sync_cisco_support_data` which can be used as below to update all fields
which contains data from the Cisco support APIs. This script can be executed for example inside a Azure
DevOps Build Pipeline once a day as these data don't change that often.

The Python script `sync_cisco_support_data` will do requests to the Cisco support APIs to update the following fields:

Model `CiscoDeviceTypeSupport`:
> :warning: **Verbose model field names listed**
>
> Model properties are not documented as they can't be edited
* Name *:warning:
* PID *:warning:
* Has EoX Error
* EoX Error
* EoX Announcement Date
* End of Sale Date
* End of Sw-Maint. Date
* End of Sec-Vul. Date
* End of Routine-Fail. Analysis Date
* End of Service Cont. Renewal
* End of Svc-Attach. Date
* Last Date of Support

> *:warning: *Overwritten by custom model save() function*

Model `CiscoDeviceSupport`:
> :warning: **Verbose model field names listed**
>
> Model properties are not documented as they can't be edited
* Name *:warning:
* Serial *:warning:
* PID *:warning:
* API Status *:warning:
* Is Covered
* Serial Owner
* Coverage End Date
* Service Contract Number
* Service Line Description
* Warranty Type
* Warranty End Date
* Recommended Release
* Has EoX Error *:warning:
* EoX Error *:warning:
* EoX Announcement Date *:warning:
* End of Sale Date *:warning:
* End of Sw-Maint. Date *:warning:
* End of Sec-Vul. Date *:warning:
* End of Routine-Fail. Analysis Date *:warning:
* End of Service Cont. Renewal *:warning:
* End of Svc-Attach. Date *:warning:
* Last Date of Support *:warning:

> *:warning: *Overwritten by custom model save() function*

There are some view fields which provide additional information which can't be updated directly with the help
of the Cisco support APIs. These fields should be updated with a external script over the NetBox REST API
(for example with a Azure DevOps Build Pipeline).

The following fields can't be updated directly by the Python script `sync_cisco_support_data`.

Model `CiscoDeviceSupport`:
> :warning: **Verbose model field names listed**
>
> Model properties are not documented as they can't be edited
* Contract Supplier *:warning:
* Partner Contract Status
* Partner Service Level
* Partner Customer Number
* Partner Coverage End Date
* Desired Release
* Desired Release Status *:warning:
* Current Release
* Current Release Status *:warning:

> *:warning: *Overwritten by custom model save() function*

> **No Edit Views**
>
> Manual edit of fields only in the NetBox Django admin portal
> At the moment there are no edit views to edit field of any data model of this plugin. The because the
> idea of this plugin is not to change fields manually (only automated by Python or REST API). If you want
> to change field manually, at the moment this can only be done in the NetBox Django admin portal.

## Fortinet
----
</br>

> **In Development**
>
> The device support coverage of Fortinet is in development

## Pure Storage
----
</br>

> **In Development**
>
> The device support coverage of Pure Storage is in development

# Compatibility
----
</br>

> :warning: **NetBox 4.0**: The latest release of this plugin is for NetBox 4.0

This plugin is compatible with [NetBox](https://netbox.readthedocs.org/) 3.5.0 and later.

| NetBox Version | Plugin Version |
|----------------|----------------|
|      3.5       |      0.0.1     |
|      4.0       |      1.0.3     |


# Installation
----
</br>

The installation and configuration steps are for the [NetBox-Docker](https://github.com/netbox-community/netbox-docker)
installation. To install this plugin make sure you followed the prerequisites for using NetBox plugins with
NetBox-Docker: [Using Netbox Plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins)

The plugin is available as a Python package in pypi and can be installed with pip.

```bash
pip install netbox_device_support_plugin
```

Add the plugin to the `plugin_requirements.txt` or `requirements.txt` of your NetBox-Docker project.

```bash
# Netbox Cisco Support Plugin
netbox-device-support-plugin
```

# Enable the Plugin
----
</br>

Enable the `netbox-device-support-plugin` plugin in `/netbox-docker/configuration/plugins.py` and add the
plugin configuration also in the same file.

```python
# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = [
    "netbox_device_support_plugin",
]
```

# Configure the Plugin
----
</br>

> **Fortinet and Pure Storage in Development**
>
> The section plugin configuration describes only the vendor Cisco as Fortinet and Pure Storage are still
> in development

## Mandatory Settings
----
</br>

In order to get valid API response data, several requirements must be fulfilled:

1. A [Cisco API ID and secret](https://apiconsole.cisco.com/) (with access to the APIs "EoX V5 API",
"Serial Number to Information API Version 2" and "Software Suggestion") must have been created and
configured inside `plugins.py`

    The following plugin configuration options are mandatory for the Cisco support API.
    * `CISCO_SUPPORT_API_CLIENT_ID`: String - Client ID of your plugin installation.
    Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)
    * `CISCO_SUPPORT_API_CLIENT_SECRET`: String - Client Secret of your plugin installation.
    Generate it inside [Cisco API Console](https://apiconsole.cisco.com/)

    Add the `netbox-device-support-plugin` plugin configuration in `/netbox-docker/configuration/plugins.py`.

    ```python
    # Plugins configuration settings. These settings are used by various plugins that the user may have installed.
    # Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
    PLUGINS_CONFIG = {
        "netbox_device_support_plugin": {
            "CISCO_SUPPORT_API_CLIENT_ID": environ.get("CISCO_SUPPORT_API_CLIENT_ID", ""),
            "CISCO_SUPPORT_API_CLIENT_SECRET": environ.get("CISCO_SUPPORT_API_CLIENT_SECRET", ""),
        },
    }
    ```

## Optional Settings
----
</br>

1. A manufacturer called `Cisco`, must have been configured inside NetBox. If your manufacturer is named
differently, change it inside the plugin configuration in `plugins.py`:

    ```python
    PLUGINS_CONFIG = {
        "netbox_device_support_plugin": {
            ...,
            "MANUFACTURER": "Cisco Systems" # Optional setting for definiing the manufacturer
        }
    }
    ```

2. Optional the `TEMPLATE_EXTENSION_PLACEMENT` can be changed inside the plugin configuration in `plugins.py`:

    ```python
    PLUGINS_CONFIG = {
        "netbox_device_support_plugin": {
            ...,
            "TEMPLATE_EXTENSION_PLACEMENT": "left" # Optional setting render the content on the left or right side
        }
    }
    ```

# Rebuild and Restart NetBox-Docker
----
</br>

Delete the NetBox-Docker project completly.

```bash
docker compose down -v
```

Rebuild the NetBox-Docker project to install the new added plugin.

```bash
docker compose build --no-cache
docker compose up -d
```

# Run Database Migrations
----
</br>

Restore the database and run the Django database migration to your existing NetBox database.

```bash
python3 manage.py migrate
```

# Sync the Device Support Data
----
</br>

## Cisco
----
</br>

In order that `sync_cisco_support_data` works correctly, several requirements must be fulfilled:

1. All devices types for manufacturer Cisco must have filled the optional `Part number` field inside NetBox
with the correct Base PID for that Cisco product.

2. All devices with devices types from manufacturer Cisco must have filled the `Serial Number` field inside
NetBox with a valid Cisco serial number for that Cisco product.

3. If you want full visibility, the support contracts for all your devices needs to be associated with the
CCO ID which has been used for created the API ID and secret. Otherwise you will only get a coverage
true/false answer, but no detailed information regarding end of support contract coverage.

Run the previously described Python script the first time to sync all Cisco support API data.

```bash
python3 manage.py sync_cisco_support_data.py
```

Execute a Azure DevOps Build Pipeline which runs `sync_cisco_support_data.py` to periodically refresh the
data or create a cronjob which to the same a bit more old school.

### How it works
----
</br>

1. Calling the `sync_cisco_support_data` method will catch all device types for the configured manufacturer.

2. Each device types `Part number` will be send to Cisco EoX API. API answer will be saved inside a
`CiscoDeviceTypeSupport` model. One `CiscoDeviceTypeSupport` per device type.

3. Afterwards all devices for the configured manufacturer will be gathered.

4. Each devices `Serial number` will be send to Cisco SN2Info coverage API. API answer will be saved inside
a `CiscoDeviceSupport` model. One `CiscoDeviceSupport` per device.

5. The device type template will be extended to display this data. Information will be shown, if a
`CiscoDeviceTypeSupport` object for that device type exists.

6. The device template will be exteneded to display device and device type information. Information will be
shown, if a `CiscoDeviceSupport` object for that device exists. Additionally device type information will be
shown, if a `CiscoDeviceTypeSupport` object for the parent device type exists.

7. Field Coloring: Expired timestamps or no data will be colored red, timestamps which will expire in the next
calendar year will be colored yellow for planning or forecast reasons.

8. Progress Bar: The progress bars will visualize the timestamps duration to the expiration date. The
progress bar color will be green until the timestamp will expire in the next calendar year. Then the color
will change to yellow. The color will finally change to red when the timestamp expire within 60 days.

## Fortinet
----
</br>

> **In Development**
>
> The device support coverage of Fortinet is in development

## Pure Storage
----
</br>

> **In Development**
>
> The device support coverage of Fortinet is in development

# Plugin Screenshots
----
</br>

## Device Detail View
![Device Detail View](docs/device_detail_view.png)

## Device Type Detail View
![Device Type Detail View](docs/device_type_detail_view.png)

## Device List View
![Device List View](docs/device_list_view.png)

## Device Type List View
![Device Type List View](docs/device_type_list_view.png)

# Languages and Tools
----
</br>

<p align="center">
  <img width="8.4%" src="https://user-images.githubusercontent.com/70367776/177972422-da6933d5-310e-4cdb-9433-89f2dc6ebb7a.png" alt="Python" />
  <img width="10.2%" src="https://user-images.githubusercontent.com/70367776/177969859-476bd542-2c0e-41a9-82f2-3e4919a61d4e.png" alt="YAML" />
  <img width="10.2%" src="https://user-images.githubusercontent.com/70367776/183678800-403cf0ea-3c8a-47bb-b52a-2caa0cedc195.png" alt="Makefile" />
  <img width="10.5%" src="https://user-images.githubusercontent.com/70367776/183679432-2b89f00c-f5b1-4d47-9c68-ad7fa332de01.png" alt="Prospector" />
  <img width="9%" src="https://user-images.githubusercontent.com/70367776/183680151-62d5c625-0430-4c90-adfc-1ebb47fce4a9.png" alt="Bandit" />
  <img width="9.4%" src="https://user-images.githubusercontent.com/70367776/177972703-3be3c4c3-aa9a-4468-97a6-e7760d536b89.png" alt="Git" />
  <img width="11.5%" src="https://user-images.githubusercontent.com/70367776/232078456-8aee2fda-1289-4cd9-b7f3-9b34fcb4d7c7.png" alt="Docker" />
  <img width="9.4%" src="https://user-images.githubusercontent.com/70367776/231501139-a449202e-6a81-4364-a4ea-1e42906e846e.png" alt="Azure Pipeline" />
  <img width="33.2%" src="https://user-images.githubusercontent.com/70367776/231500048-77eeff9a-166b-4bd7-a0cc-3c5fc58be368.png" alt="NetBox" />
</p>

<br>

<h3 align="center">APIs can also be amusing to provide a programming joke ...</h3>
<p align="center"><img src="https://readme-jokes.vercel.app/api?hideBorder&theme=calm" /></p>
<h3 align="center">... or an interesting quote.</h3>
<p align="center"><img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dracula" /></p>
