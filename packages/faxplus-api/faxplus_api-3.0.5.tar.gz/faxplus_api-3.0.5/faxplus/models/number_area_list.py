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


class NumberAreaList(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'areas': 'list[NumberArea]'
    }

    attribute_map = {
        'areas': 'areas'
    }

    def __init__(self, areas=None):  # noqa: E501
        """NumberAreaList - a model defined in Swagger

        :param list[NumberArea] areas: (required)
        """  # noqa: E501
        self._areas = None
        self.discriminator = None
        self.areas = areas

    @property
    def areas(self):
        """Gets the areas of this NumberAreaList.  # noqa: E501


        :return: The areas of this NumberAreaList.  # noqa: E501
        :rtype: list[NumberArea]
        """
        return self._areas

    @areas.setter
    def areas(self, areas):
        """Sets the areas of this NumberAreaList.


        :param areas: The areas of this NumberAreaList.  # noqa: E501
        :type: list[NumberArea]
        """
        if areas is None:
            raise ValueError("Invalid value for `areas`, must not be `None`")  # noqa: E501

        self._areas = areas

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
        if issubclass(NumberAreaList, dict):
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
        if not isinstance(other, NumberAreaList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

