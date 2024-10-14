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


class AvailableNumberItem(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'country': 'str',
        'number': 'str',
        'country_code': 'str',
        'geographic_area': 'AvailableNumberItemGeographicArea'
    }

    attribute_map = {
        'id': 'id',
        'country': 'country',
        'number': 'number',
        'country_code': 'country_code',
        'geographic_area': 'geographic_area'
    }

    def __init__(self, id=None, country=None, number=None, country_code=None, geographic_area=None):  # noqa: E501
        """AvailableNumberItem - a model defined in Swagger

        :param str id:
        :param str country:
        :param str number:
        :param str country_code:
        :param AvailableNumberItemGeographicArea geographic_area:
        """  # noqa: E501
        self._id = None
        self._country = None
        self._number = None
        self._country_code = None
        self._geographic_area = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if country is not None:
            self.country = country
        if number is not None:
            self.number = number
        if country_code is not None:
            self.country_code = country_code
        if geographic_area is not None:
            self.geographic_area = geographic_area

    @property
    def id(self):
        """Gets the id of this AvailableNumberItem.  # noqa: E501


        :return: The id of this AvailableNumberItem.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AvailableNumberItem.


        :param id: The id of this AvailableNumberItem.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def country(self):
        """Gets the country of this AvailableNumberItem.  # noqa: E501


        :return: The country of this AvailableNumberItem.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this AvailableNumberItem.


        :param country: The country of this AvailableNumberItem.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def number(self):
        """Gets the number of this AvailableNumberItem.  # noqa: E501


        :return: The number of this AvailableNumberItem.  # noqa: E501
        :rtype: str
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this AvailableNumberItem.


        :param number: The number of this AvailableNumberItem.  # noqa: E501
        :type: str
        """

        self._number = number

    @property
    def country_code(self):
        """Gets the country_code of this AvailableNumberItem.  # noqa: E501


        :return: The country_code of this AvailableNumberItem.  # noqa: E501
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """Sets the country_code of this AvailableNumberItem.


        :param country_code: The country_code of this AvailableNumberItem.  # noqa: E501
        :type: str
        """

        self._country_code = country_code

    @property
    def geographic_area(self):
        """Gets the geographic_area of this AvailableNumberItem.  # noqa: E501


        :return: The geographic_area of this AvailableNumberItem.  # noqa: E501
        :rtype: AvailableNumberItemGeographicArea
        """
        return self._geographic_area

    @geographic_area.setter
    def geographic_area(self, geographic_area):
        """Sets the geographic_area of this AvailableNumberItem.


        :param geographic_area: The geographic_area of this AvailableNumberItem.  # noqa: E501
        :type: AvailableNumberItemGeographicArea
        """

        self._geographic_area = geographic_area

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
        if issubclass(AvailableNumberItem, dict):
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
        if not isinstance(other, AvailableNumberItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

