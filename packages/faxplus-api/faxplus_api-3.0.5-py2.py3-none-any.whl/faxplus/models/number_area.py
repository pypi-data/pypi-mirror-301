# coding: utf-8

"""
    Fax.Plus REST API

    Visit https://apidoc.fax.plus for more information.

    © Alohi SA (Geneva, Switzerland)

    https://www.alohi.com
    Contact: info@fax.plus
"""

import pprint
import re  # noqa: F401

import six
from faxplus.models import *


class NumberArea(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'calling_code': 'str',
        'city': 'str',
        'state': 'str'
    }

    attribute_map = {
        'calling_code': 'calling_code',
        'city': 'city',
        'state': 'state'
    }

    def __init__(self, calling_code=None, city=None, state=None):  # noqa: E501
        """NumberArea - a model defined in Swagger

        :param str calling_code: Calling code (required)
        :param str city: City name (required)
        :param str state: State name (required)
        """  # noqa: E501
        self._calling_code = None
        self._city = None
        self._state = None
        self.discriminator = None
        self.calling_code = calling_code
        self.city = city
        self.state = state

    @property
    def calling_code(self):
        """Gets the calling_code of this NumberArea.  # noqa: E501

        Calling code  # noqa: E501

        :return: The calling_code of this NumberArea.  # noqa: E501
        :rtype: str
        """
        return self._calling_code

    @calling_code.setter
    def calling_code(self, calling_code):
        """Sets the calling_code of this NumberArea.

        Calling code  # noqa: E501

        :param calling_code: The calling_code of this NumberArea.  # noqa: E501
        :type: str
        """
        if calling_code is None:
            raise ValueError("Invalid value for `calling_code`, must not be `None`")  # noqa: E501

        self._calling_code = calling_code

    @property
    def city(self):
        """Gets the city of this NumberArea.  # noqa: E501

        City name  # noqa: E501

        :return: The city of this NumberArea.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this NumberArea.

        City name  # noqa: E501

        :param city: The city of this NumberArea.  # noqa: E501
        :type: str
        """
        if city is None:
            raise ValueError("Invalid value for `city`, must not be `None`")  # noqa: E501

        self._city = city

    @property
    def state(self):
        """Gets the state of this NumberArea.  # noqa: E501

        State name  # noqa: E501

        :return: The state of this NumberArea.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this NumberArea.

        State name  # noqa: E501

        :param state: The state of this NumberArea.  # noqa: E501
        :type: str
        """
        if state is None:
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(NumberArea, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, NumberArea):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

