"""Cisco vManage Device Inventory API Methods.
"""

from vmanage.api.http_methods import HttpMethods
from vmanage.data.parse_methods import ParseMethods


class Device(object):
    """vManage Device Inventory API

    Responsible for DELETE, GET, POST, PUT methods against vManage
    Device Inventory.

    """
    def __init__(self, session, host, port=443):
        """Initialize Device Inventory object with session parameters.

        Args:
            session (obj): Requests Session object
            host (str): hostname or IP address of vManage
            port (int): default HTTPS 443

        """

        self.session = session
        self.host = host
        self.port = port
        self.base_url = f'https://{self.host}:{self.port}/dataservice/'

    def get_device_list(self, category):
        """Obtain a list of specified device type

        Args:
            category (str): vedges or controllers

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}system/device/{category}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def post_device_cli_mode(self, deviceId, deviceIP, deviceType):
        """Update a device to CLI mode

        Args:
            deviceId (str): uuid for device object
            deviceIP (str): system IP equivalent
            deviceType (str): vedge or controller

        """

        url = f"{self.base_url}template/config/device/mode/cli"
        devices = f"{{'deviceId':'{deviceId}','deviceIP':'{deviceIP}'}}"
        payload = f"{{'deviceType':'{deviceType}','devices':[{devices}]}}"
        response = HttpMethods(self.session, url).request('POST', payload=payload)
        result = ParseMethods.parse_status(response)
        return result

    def get_device_status_list(self):
        """Obtain a list of specified device type

        Args: None

        Returns:
            result (list): Device status
        """

        api = f"device/"
        url = self.base_url + api
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_device_status_dict(self, key_name='host-name', remove_key=False):
        """Obtain a dict of specified device type

        Args:
            category (str): vedges or controllers

        Returns:
            result (dict): Device status
        """

        result = self.get_device_status_list()

        return self.list_to_dict(result.json, key_name=key_name, remove_key=remove_key)

    def get_device_status(self, value, key='system-ip'):
        """Get the status of a specific device

        Args:
            value string: The value of the key to match
            key (string): The key on which to match (e.g. system-ip)

        Returns:
            result (dict): Device status
        """

        url = f"{self.base_url}device?{key}={value}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)

        if len(result):
            return result[0]

        return {}

    def get_device_config(self, device_type, value, key='system-ip'):
        """Get the config of a specific device

        Args:
            value string: The value of the key to match
            key (string): The key on which to match (e.g. system-ip)

        Returns:
            result (dict): Device config
        """

        url = f"{self.base_url}system/device/{device_type}?{key}={value}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)

        if len(result):
            return result[0]

        return {}

    def get_device_config_list(self, device_type):
        """Get the config status of a list of devices

        Args:
            device_type (str): vedge or controller

        Returns:
            result (list): All data associated with a response.
        """

        url = f"{self.base_url}system/device/{device_type}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result

    def get_device_config_dict(self, device_type, key_name='host-name', remove_key=False):
        """Get the config status of a list of devices as a dictionary

        Args:
            device_type (str): vedge or controller
            key_name (string): The name of the attribute to use as the dictionary key
            remove_key (boolean): remove the search key from the element

        Returns:
            result (dict): All data associated with a response.

        """
        device_list = self.get_device_config_list(device_type)

        return self.list_to_dict(device_list, key_name=key_name, remove_key=remove_key)

    def get_device_data(self, path, device_ip):
        """Get the data from a device

        Args:
            path (str): The path of the data
            device_ip (str): The IP address of the device

        Returns:
            result (dict): All data associated with a response.
        """

        url = f"{self.base_url}device/{path}?deviceId={device_ip}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result
