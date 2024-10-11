# `netcup-webservice` - unofficial client for Netcup's API

An unofficial Python client library for interacting with Netcup's server control panel webservice. This library allows you to manage your vServers (virtual servers) and interact with the Netcup API programmatically.

**Disclaimer**: This project is not affiliated with, endorsed, or sponsored by Netcup GmbH. It is an independent, open-source project created to simplify interaction with the Netcup API.

## Features

- Manage vServers: Start, stop, suspend, resume, and more.
- Get vServer Information: Retrieve state, uptime, nickname, traffic statistics, and other information.
- Set vServer Nickname: Easily update the nickname for your vServers.
- Change Password: Programmatically change user passwords.
- And many more methods available via Netcup's API.

## Installation

```bash
pip install netcup-webservice
```

## Usage
### Import the Library
To start using the client, simply import the NetcupWebservice class after installation:
```python
from netcup_webservice import NetcupWebservice
```
### Initialize the Client
You need your Netcup credentials (login name and password) to interact with the API.
```python
client = NetcupWebservice(loginname="your_login", password="your_password")
```
### Example: get all vServers
```python
vServers = client.get_vservers()
```

## Available Methods
- `get_vserver_nickname(vserver_name)`: Get the nickname of a vServer.
- `set_vserver_nickname(vserver_name, nickname)`: Set a new nickname for a vServer.
- `get_vserver_state(vserver_name)`: Get the state (running, stopped, etc.) of a vServer.
- `get_vserver_uptime(vserver_name)`: Get the uptime of a vServer.
- `get_vserver_update_notification(vserver_name)`: Get the update notifications for a vServer.
- `start_vserver(vserver_name)`: Start a vServer.
- `stop_vserver(vserver_name)`: Stop a vServer.
- `suspend_vserver(vserver_name)`: Suspend a vServer.
- `resume_vserver(vserver_name)`: Resume a suspended vServer.
- `restore_vserver(vserver_name)`: Restore a vServer from a backup.
- `get_vserver_stat_token(vserver_name)`: Get a statistics token for a vServer.
- `get_vserver_traffic_of_day(vserver_name)`: Get the traffic statistics for the current day.
- `get_vserver_traffic_of_month(vserver_name)`: Get the traffic statistics for the current month.
- `change_user_password(new_password)`: Change the user’s password.
- `get_vserver_information(vserver_name)`: Get detailed information about a vServer.
- `get_vserver_ips(vserver_name)`: Get the IP addresses assigned to a vServer.
- `acpi_shutdown_vserver(vserver_name)`: Perform an ACPI shutdown of a vServer.
- `acpi_reboot_vserver(vserver_name)`: Perform an ACPI reboot of a vServer.
- `reset_vserver(vserver_name)`: Perform a hard reset of a vServer.
- `poweroff_vserver(vserver_name)`: Power off a vServer.
- `add_cloud_vlan_interface(vserver_name, vlan_id)`: Add a VLAN interface to a vServer.
- `change_ip_routing(vserver_name, route)`: Change the IP routing configuration of a vServer.
- `get_vservers()`: Get a list of all vServers associated with the account.
- `get_panel_settings()`: Get the current control panel settings.
- `send_password_reset_request()`: Send a password reset request.
- `get_vserver_log_entry_count(vserver_name)`: Get the log entry count for a vServer.
- `get_vserver_log_entries(vserver_name, start, limit)`: Get log entries for a vServer.
- `set_panel_settings(panel_settings)`: Update the panel settings.

## Disclaimer
This package is not affiliated with, endorsed, or sponsored by Netcup GmbH. It is an independent project and is maintained solely by its contributors.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
