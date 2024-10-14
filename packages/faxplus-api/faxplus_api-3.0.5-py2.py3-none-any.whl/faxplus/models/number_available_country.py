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


class NumberAvailableCountry(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'iso': 'str',
        'name': 'str',
        'is_available': 'bool'
    }

    attribute_map = {
        'iso': 'iso',
        'name': 'name',
        'is_available': 'is_available'
    }

    def __init__(self, iso=None, name=None, is_available=None):  # noqa: E501
        """NumberAvailableCountry - a model defined in Swagger

        :param str iso: Country code (ISO 3166-1 alpha-2)
        :param str name: Country name
        :param bool is_available: Is fax number available for purchase in this country
        """  # noqa: E501
        self._iso = None
        self._name = None
        self._is_available = None
        self.discriminator = None
        if iso is not None:
            self.iso = iso
        if name is not None:
            self.name = name
        if is_available is not None:
            self.is_available = is_available

    @property
    def iso(self):
        """Gets the iso of this NumberAvailableCountry.  # noqa: E501

        Country code (ISO 3166-1 alpha-2)  # noqa: E501

        :return: The iso of this NumberAvailableCountry.  # noqa: E501
        :rtype: str
        """
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the iso of this NumberAvailableCountry.

        Country code (ISO 3166-1 alpha-2)  # noqa: E501

        :param iso: The iso of this NumberAvailableCountry.  # noqa: E501
        :type: str
        """

        self._iso = iso

    @property
    def name(self):
        """Gets the name of this NumberAvailableCountry.  # noqa: E501

        Country name  # noqa: E501

        :return: The name of this NumberAvailableCountry.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NumberAvailableCountry.

        Country name  # noqa: E501

        :param name: The name of this NumberAvailableCountry.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def is_available(self):
        """Gets the is_available of this NumberAvailableCountry.  # noqa: E501

        Is fax number available for purchase in this country  # noqa: E501

        :return: The is_available of this NumberAvailableCountry.  # noqa: E501
        :rtype: bool
        """
        return self._is_available

    @is_available.setter
    def is_available(self, is_available):
        """Sets the is_available of this NumberAvailableCountry.

        Is fax number available for purchase in this country  # noqa: E501

        :param is_available: The is_available of this NumberAvailableCountry.  # noqa: E501
        :type: bool
        """

        self._is_available = is_available

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
        if issubclass(NumberAvailableCountry, dict):
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
        if not isinstance(other, NumberAvailableCountry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

