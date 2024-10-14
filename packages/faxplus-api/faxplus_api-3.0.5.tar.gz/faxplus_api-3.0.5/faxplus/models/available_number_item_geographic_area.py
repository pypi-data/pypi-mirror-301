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


class AvailableNumberItemGeographicArea(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'area_code': 'str',
        'geographic_area': 'str',
        'city': 'str'
    }

    attribute_map = {
        'area_code': 'area_code',
        'geographic_area': 'geographic_area',
        'city': 'city'
    }

    def __init__(self, area_code=None, geographic_area=None, city=None):  # noqa: E501
        """AvailableNumberItemGeographicArea - a model defined in Swagger

        :param str area_code:
        :param str geographic_area:
        :param str city:
        """  # noqa: E501
        self._area_code = None
        self._geographic_area = None
        self._city = None
        self.discriminator = None
        if area_code is not None:
            self.area_code = area_code
        if geographic_area is not None:
            self.geographic_area = geographic_area
        if city is not None:
            self.city = city

    @property
    def area_code(self):
        """Gets the area_code of this AvailableNumberItemGeographicArea.  # noqa: E501


        :return: The area_code of this AvailableNumberItemGeographicArea.  # noqa: E501
        :rtype: str
        """
        return self._area_code

    @area_code.setter
    def area_code(self, area_code):
        """Sets the area_code of this AvailableNumberItemGeographicArea.


        :param area_code: The area_code of this AvailableNumberItemGeographicArea.  # noqa: E501
        :type: str
        """

        self._area_code = area_code

    @property
    def geographic_area(self):
        """Gets the geographic_area of this AvailableNumberItemGeographicArea.  # noqa: E501


        :return: The geographic_area of this AvailableNumberItemGeographicArea.  # noqa: E501
        :rtype: str
        """
        return self._geographic_area

    @geographic_area.setter
    def geographic_area(self, geographic_area):
        """Sets the geographic_area of this AvailableNumberItemGeographicArea.


        :param geographic_area: The geographic_area of this AvailableNumberItemGeographicArea.  # noqa: E501
        :type: str
        """

        self._geographic_area = geographic_area

    @property
    def city(self):
        """Gets the city of this AvailableNumberItemGeographicArea.  # noqa: E501


        :return: The city of this AvailableNumberItemGeographicArea.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this AvailableNumberItemGeographicArea.


        :param city: The city of this AvailableNumberItemGeographicArea.  # noqa: E501
        :type: str
        """

        self._city = city

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
        if issubclass(AvailableNumberItemGeographicArea, dict):
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
        if not isinstance(other, AvailableNumberItemGeographicArea):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

