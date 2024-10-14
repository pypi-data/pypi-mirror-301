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


class PurchaseNumberRequest(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'item_id': 'str'
    }

    attribute_map = {
        'item_id': 'item_id'
    }

    def __init__(self, item_id=None):  # noqa: E501
        """PurchaseNumberRequest - a model defined in Swagger

        :param str item_id: The fax number item_id to purchase (required)
        """  # noqa: E501
        self._item_id = None
        self.discriminator = None
        self.item_id = item_id

    @property
    def item_id(self):
        """Gets the item_id of this PurchaseNumberRequest.  # noqa: E501

        The fax number item_id to purchase  # noqa: E501

        :return: The item_id of this PurchaseNumberRequest.  # noqa: E501
        :rtype: str
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this PurchaseNumberRequest.

        The fax number item_id to purchase  # noqa: E501

        :param item_id: The item_id of this PurchaseNumberRequest.  # noqa: E501
        :type: str
        """
        if item_id is None:
            raise ValueError("Invalid value for `item_id`, must not be `None`")  # noqa: E501

        self._item_id = item_id

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
        if issubclass(PurchaseNumberRequest, dict):
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
        if not isinstance(other, PurchaseNumberRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

