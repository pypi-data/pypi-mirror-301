import zeep
from zeep.exceptions import Fault

class NetcupWebservice:
    """
    A class to interact with the Netcup server control panel via SOAP Web Services.
    """

    def __init__(self, loginname, password):
        """
        Initialize the NetcupWebservice with login credentials.

        Args:
            loginname (str): The login name for the Netcup Webservice.
            password (str): The password for the Netcup Webservice.
        """
        self.wsdl_url = 'https://www.servercontrolpanel.de/WSEndUser?wsdl'
        self.client = zeep.Client(wsdl=self.wsdl_url)
        self.loginname = loginname
        self.password = password

    def get_vserver_nickname(self, vserver_name):
        """
        Retrieve the nickname of the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The nickname of the vServer, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name}
            result = self.client.service.getVServerNickname(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def set_vserver_nickname(self, vserver_name, nickname):
        """
        Set a new nickname for the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.
            nickname (str): The new nickname for the vServer.

        Returns:
            str: The result of the nickname update operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name, 'vservernickname': nickname}
            result = self.client.service.setVServerNickname(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_state(self, vserver_name):
        """
        Get the current state of the specified vServer (e.g., running, stopped).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The state of the vServer, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.getVServerState(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_uptime(self, vserver_name):
        """
        Get the uptime of the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The uptime of the vServer, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.getVServerUptime(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_update_notification(self, vserver_name):
        """
        Get update notifications for the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: Update notifications for the vServer, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.getVServerUpdateNotification(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def start_vserver(self, vserver_name):
        """
        Start the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the start operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerStart(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def suspend_vserver(self, vserver_name):
        """
        Suspend the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the suspend operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerSuspend(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def resume_vserver(self, vserver_name):
        """
        Resume the specified vServer from suspension.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the resume operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerResume(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def restore_vserver(self, vserver_name):
        """
        Restore the specified vServer from a backup or previous state.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the restore operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerRestore(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_stat_token(self, vserver_name):
        """
        Get a token for vServer statistics (used to access monitoring data).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The statistics token, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.getVServerStatToken(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_traffic_of_day(self, vserver_name, year, month, day):
        """
        Get the traffic usage of the specified vServer for a specific day.

        Args:
            vserver_name (str): The name of the vServer.
            year (int): The year for which to get traffic data.
            month (int): The month for which to get traffic data.
            day (int): The day for which to get traffic data.

        Returns:
            str: The traffic data for the day, or an error message in case of a SOAP fault.
        """
        try:
            params = {
                'loginName': self.loginname,
                'password': self.password,
                'vserverName': vserver_name,
                'year': year,
                'month': month,
                'day': day
            }
            result = self.client.service.getVServerTrafficOfDay(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_traffic_of_month(self, vserver_name, year, month):
        """
        Get the traffic usage of the specified vServer for a specific month.

        Args:
            vserver_name (str): The name of the vServer.
            year (int): The year for which to get traffic data.
            month (int): The month for which to get traffic data.

        Returns:
            str: The traffic data for the month, or an error message in case of a SOAP fault.
        """
        try:
            params = {
                'loginName': self.loginname,
                'password': self.password,
                'vserverName': vserver_name,
                'year': year,
                'month': month
            }
            result = self.client.service.getVServerTrafficOfMonth(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def change_user_password(self, new_password):
        """
        Change the user account's password.

        Args:
            new_password (str): The new password for the user account.

        Returns:
            str: The result of the password change operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'newPassword': new_password}
            result = self.client.service.changeUserPassword(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_information(self, vserver_name):
        """
        Retrieve detailed information about the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The vServer information, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name}
            result = self.client.service.getVServerInformation(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def stop_vserver(self, vserver_name):
        """
        Stop the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the stop operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.stopVServer(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_ips(self, vserver_name):
        """
        Retrieve the list of IP addresses assigned to the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The list of IP addresses, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.getVServerIPs(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def acpi_shutdown_vserver(self, vserver_name):
        """
        Perform an ACPI shutdown of the specified vServer (graceful shutdown).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the shutdown operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerACPIShutdown(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def acpi_reboot_vserver(self, vserver_name):
        """
        Perform an ACPI reboot of the specified vServer (graceful reboot).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the reboot operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerACPIReboot(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def reset_vserver(self, vserver_name):
        """
        Perform a hard reset of the specified vServer (immediate restart).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the reset operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerReset(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def poweroff_vserver(self, vserver_name):
        """
        Power off the specified vServer immediately (force shutdown).

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The result of the power-off operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name}
            result = self.client.service.vServerPoweroff(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def add_cloud_vlan_interface(self, vserver_name, vlan_id):
        """
        Add a VLAN interface to the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.
            vlan_id (int): The ID of the VLAN to add.

        Returns:
            str: The result of the operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name, 'vlanID': vlan_id}
            result = self.client.service.addCloudVLANInterface(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def change_ip_routing(self, vserver_name, route):
        """
        Change the IP routing configuration for the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.
            route (str): The new route configuration.

        Returns:
            str: The result of the route change operation, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vserverName': vserver_name, 'route': route}
            result = self.client.service.changeIPRouting(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vservers(self):
        """
        Retrieve the list of vServers associated with the account.

        Returns:
            str: The list of vServers, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password}
            result = self.client.service.getVServers(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_panel_settings(self):
        """
        Retrieve the current control panel settings.

        Returns:
            str: The panel settings, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password}
            result = self.client.service.getPanelSettings(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def send_password_reset_request(self):
        """
        Send a request to reset the account password.

        Returns:
            str: The result of the reset request, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password}
            result = self.client.service.sendPasswordResetRequest(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_log_entry_count(self, vserver_name):
        """
        Get the total number of log entries for the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.

        Returns:
            str: The count of log entries, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name}
            result = self.client.service.getVServerLogEntryCount(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_vserver_log_entries(self, vserver_name, start, limit):
        """
        Retrieve log entries for the specified vServer.

        Args:
            vserver_name (str): The name of the vServer.
            start (int): The start index for retrieving logs.
            limit (int): The number of log entries to retrieve.

        Returns:
            str: The list of log entries, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password, 'vservername': vserver_name, 'start': start, 'limit': limit}
            result = self.client.service.getVServerLogEntries(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def set_panel_settings(self, show_nickname):
        """
        Update the control panel settings.

        Args:
            show_nickname (bool): A boolean value indicating whether to show the vServer nickname.

        Returns:
            bool: True if the operation is successful, False otherwise, or an error message in case of a SOAP fault.
        """
        try:
            params = { 'loginName': self.loginname, 'password': self.password, 'showNickname': show_nickname }
            result = self.client.service.setPanelSettings(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_login_token(self):
        """
        Retrieve a login token for API authentication.

        Returns:
            str: The login token, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password}
            result = self.client.service.getLoginToken(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"

    def get_user_data(self):
        """
        Retrieve the account's user data (such as contact information).

        Returns:
            str: The user data, or an error message in case of a SOAP fault.
        """
        try:
            params = {'loginName': self.loginname, 'password': self.password}
            result = self.client.service.getUserData(**params)
            return result
        except Fault as e:
            return f"SOAP Fault occurred: {e.message}"
