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


class NumbersAvailableCountries(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'countries': 'list[NumberAvailableCountry]'
    }

    attribute_map = {
        'countries': 'countries'
    }

    def __init__(self, countries=None):  # noqa: E501
        """NumbersAvailableCountries - a model defined in Swagger

        :param list[NumberAvailableCountry] countries: List of countries (required)
        """  # noqa: E501
        self._countries = None
        self.discriminator = None
        self.countries = countries

    @property
    def countries(self):
        """Gets the countries of this NumbersAvailableCountries.  # noqa: E501

        List of countries  # noqa: E501

        :return: The countries of this NumbersAvailableCountries.  # noqa: E501
        :rtype: list[NumberAvailableCountry]
        """
        return self._countries

    @countries.setter
    def countries(self, countries):
        """Sets the countries of this NumbersAvailableCountries.

        List of countries  # noqa: E501

        :param countries: The countries of this NumbersAvailableCountries.  # noqa: E501
        :type: list[NumberAvailableCountry]
        """
        if countries is None:
            raise ValueError("Invalid value for `countries`, must not be `None`")  # noqa: E501

        self._countries = countries

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
        if issubclass(NumbersAvailableCountries, dict):
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
        if not isinstance(other, NumbersAvailableCountries):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

