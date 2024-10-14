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


class AvailableNumber(object):

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'type': 'str',
        'currency': 'str',
        'availability': 'str',
        'item': 'AvailableNumberItem',
        'price': 'float',
        'monthly_fee': 'float',
        'number_of_months': 'int'
    }

    attribute_map = {
        'type': 'type',
        'currency': 'currency',
        'availability': 'availability',
        'item': 'item',
        'price': 'price',
        'monthly_fee': 'monthly_fee',
        'number_of_months': 'number_of_months'
    }

    def __init__(self, type=None, currency=None, availability=None, item=None, price=None, monthly_fee=None, number_of_months=None):  # noqa: E501
        """AvailableNumber - a model defined in Swagger

        :param str type:
        :param str currency:
        :param str availability:
        :param AvailableNumberItem item:
        :param float price:
        :param float monthly_fee:
        :param int number_of_months:
        """  # noqa: E501
        self._type = None
        self._currency = None
        self._availability = None
        self._item = None
        self._price = None
        self._monthly_fee = None
        self._number_of_months = None
        self.discriminator = None
        if type is not None:
            self.type = type
        if currency is not None:
            self.currency = currency
        if availability is not None:
            self.availability = availability
        if item is not None:
            self.item = item
        if price is not None:
            self.price = price
        if monthly_fee is not None:
            self.monthly_fee = monthly_fee
        if number_of_months is not None:
            self.number_of_months = number_of_months

    @property
    def type(self):
        """Gets the type of this AvailableNumber.  # noqa: E501


        :return: The type of this AvailableNumber.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AvailableNumber.


        :param type: The type of this AvailableNumber.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def currency(self):
        """Gets the currency of this AvailableNumber.  # noqa: E501


        :return: The currency of this AvailableNumber.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this AvailableNumber.


        :param currency: The currency of this AvailableNumber.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def availability(self):
        """Gets the availability of this AvailableNumber.  # noqa: E501


        :return: The availability of this AvailableNumber.  # noqa: E501
        :rtype: str
        """
        return self._availability

    @availability.setter
    def availability(self, availability):
        """Sets the availability of this AvailableNumber.


        :param availability: The availability of this AvailableNumber.  # noqa: E501
        :type: str
        """

        self._availability = availability

    @property
    def item(self):
        """Gets the item of this AvailableNumber.  # noqa: E501


        :return: The item of this AvailableNumber.  # noqa: E501
        :rtype: AvailableNumberItem
        """
        return self._item

    @item.setter
    def item(self, item):
        """Sets the item of this AvailableNumber.


        :param item: The item of this AvailableNumber.  # noqa: E501
        :type: AvailableNumberItem
        """

        self._item = item

    @property
    def price(self):
        """Gets the price of this AvailableNumber.  # noqa: E501


        :return: The price of this AvailableNumber.  # noqa: E501
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this AvailableNumber.


        :param price: The price of this AvailableNumber.  # noqa: E501
        :type: float
        """

        self._price = price

    @property
    def monthly_fee(self):
        """Gets the monthly_fee of this AvailableNumber.  # noqa: E501


        :return: The monthly_fee of this AvailableNumber.  # noqa: E501
        :rtype: float
        """
        return self._monthly_fee

    @monthly_fee.setter
    def monthly_fee(self, monthly_fee):
        """Sets the monthly_fee of this AvailableNumber.


        :param monthly_fee: The monthly_fee of this AvailableNumber.  # noqa: E501
        :type: float
        """

        self._monthly_fee = monthly_fee

    @property
    def number_of_months(self):
        """Gets the number_of_months of this AvailableNumber.  # noqa: E501


        :return: The number_of_months of this AvailableNumber.  # noqa: E501
        :rtype: int
        """
        return self._number_of_months

    @number_of_months.setter
    def number_of_months(self, number_of_months):
        """Sets the number_of_months of this AvailableNumber.


        :param number_of_months: The number_of_months of this AvailableNumber.  # noqa: E501
        :type: int
        """

        self._number_of_months = number_of_months

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
        if issubclass(AvailableNumber, dict):
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
        if not isinstance(other, AvailableNumber):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

