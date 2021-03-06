"""Cisco vManage Policy Definitions API Methods.
"""

import json

from vmanage.api.http_methods import HttpMethods
from vmanage.api.policy_lists import PolicyLists
from vmanage.data.parse_methods import ParseMethods
from vmanage.utils import list_to_dict


class PolicyDefinitions(object):
    """vManage Policy Definitions API

    Responsible for DELETE, GET, POST, PUT methods against vManage
    Policy Definitions used in Centralized, Localized, and Security Policy.

    """
    def __init__(self, session, host, port=443):
        """Initialize Policy Lists object with session parameters.

        Args:
            session (obj): Requests Session object
            host (str): hostname or IP address of vManage
            port (int): default HTTPS 443

        """

        self.session = session
        self.host = host
        self.port = port
        self.base_url = f'https://{self.host}:{self.port}/dataservice/'
        self.policy_lists = PolicyLists(self.session, self.host, self.port)

    def delete_policy_definition(self, definition_type, definition_id):
        """Delete a Policy Definition from vManage.

        Args:
            definition_type (str): The defintion type of the requested policy definition
            definition_id (str): The defintion ID of the requested policy definition

        Returns:
            result (dict): All data associated with a response.

        """

        url = f"{self.base_url}template/policy/definition/{definition_type.lower()}/{definition_id}"
        HttpMethods(self.session, url).request('DELETE')

    def add_policy_definition(self, policy_definition):
        """Delete a Policy Definition from vManage.

        Args:
            definition_type (str): The defintion type of the requested policy definition
            definition_id (str): The defintion ID of the requested policy definition

        Returns:
            result (dict): All data associated with a response.

        """

        url = f"{self.base_url}template/policy/definition/{policy_definition['type'].lower()}"
        HttpMethods(self.session, url).request('POST', payload=json.dumps(policy_definition))

    def update_policy_definition(self, policy_definition, policy_definition_id):
        """Update a Policy Definition from vManage.

        Args:
            definition_type (str): The defintion type of the requested policy definition
            definition_id (str): The defintion ID of the requested policy definition

        Returns:
            result (dict): All data associated with a response.

        """

        url = f"{self.base_url}template/policy/definition/{policy_definition['type'].lower()}/{policy_definition_id}"
        HttpMethods(self.session, url).request('PUT', payload=json.dumps(policy_definition))

    def get_policy_definition(self, definition_type, definition_id):
        """Get a Policy Definition from vManage.

        Args:
            definition_type (str): The defintion type of the requested policy definition
            definition_id (str): The defintion ID of the requested policy definition

        Returns:
            result (dict): All data associated with a response.

        """

        url = f"{self.base_url}template/policy/definition/{definition_type.lower()}/{definition_id}"
        response = HttpMethods(self.session, url).request('GET')

        policy_definition = response["json"]
        return policy_definition

    def get_policy_definition_list(self, definition_type='all'):
        """Get all Policy Definition Lists from vManage.

        Args:
            definition_type (string): The type of Definition List to retreive

        Returns:
            response (dict): A list of all definition lists currently
                in vManage.

        """

        if definition_type == 'all':
            # Get a list of hub-and-spoke because it tells us the other definition types
            # known by this server (hopefully) in the header section
            all_definitions_list = []
            definition_list_types = []
            api = "template/policy/definition/hubandspoke"
            url = self.base_url + api
            response = HttpMethods(self.session, url).request('GET')

            try:
                definition_type_titles = response['json']['header']['columns'][1]['keyvalue']
            except:
                raise Exception('Could not retrieve definition types')
            for def_type in definition_type_titles:
                definition_list_types.append(def_type['key'].lower())
            for def_type in definition_list_types:
                definition_list = self.get_policy_definition_list(def_type)
                if definition_list:
                    all_definitions_list.extend(definition_list)
            return all_definitions_list

        definition_list = []

        url = f"{self.base_url}template/policy/definition/{definition_type.lower()}"
        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        for definition in result:
            definition_detail = self.get_policy_definition(definition_type, definition['definitionId'])
            if definition_detail:
                definition_list.append(definition_detail)
        return definition_list

    def get_policy_definition_dict(self, definition_type, key_name='name', remove_key=False):
        """Get all Policy Definition Lists from vManage.

        Args:
            definition_type (str): Policy definition type
            key_name (string): The name of the attribute to use as the dictionary key
            remove_key (boolean): Remove the search key from the element

        Returns:
            result (dict): All data associated with a response.

        """

        policy_definition_list = self.get_policy_definition_list(definition_type)
        return list_to_dict(policy_definition_list, key_name, remove_key=remove_key)
