# coding: utf-8

"""
    Fax.Plus REST API

    Visit https://apidoc.fax.plus for more information.

    © Alohi SA (Geneva, Switzerland)

    https://www.alohi.com
    Contact: info@fax.plus
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from faxplus.api_client import ApiClient
from faxplus.models import *
from multiprocessing.pool import ApplyResult
from urllib3._collections import HTTPHeaderDict


class ShopApi(object):
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_balance(self, **kwargs):  # noqa: E501
        """Get account balance  # noqa: E501

        Get your account balance. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().get_balance()

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().get_balance(async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :return: Balance
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Balance | ApplyResult[Balance]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_balance_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_balance_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_balance_with_http_info(self, **kwargs):  # noqa: E501
        """Get account balance  # noqa: E501

        The difference between this method and `get_balance` is that this method may return not only the data,
        but also HTTP status and headers.

        Get your account balance. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().get_balance_with_http_info()

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().get_balance_with_http_info(async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :return: Balance
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Balance | tuple[Balance, int, HTTPHeaderDict] | ApplyResult[Balance] | ApplyResult[tuple[Balance, int, HTTPHeaderDict]]
        """

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2', 'personal_access_token']  # noqa: E501

        return self.api_client.call_api(
            '/shop/balance', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Balance',  # noqa: E501
            auth_settings=auth_settings,
            async_req=kwargs.get('async_req'),
            _return_http_data_only=kwargs.get('_return_http_data_only'),
            _preload_content=kwargs.get('_preload_content', True),
            _request_timeout=kwargs.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_areas(self, country_code, **kwargs):  # noqa: E501
        """List areas  # noqa: E501

        Get a list of areas where you can purchase fax numbers for a specific country. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_areas(country_code, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_areas(country_code, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param str country_code: Country code (ISO 3166-1 alpha-2) (required)
        :return: NumberAreaList
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NumberAreaList | ApplyResult[NumberAreaList]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_areas_with_http_info(country_code, **kwargs)  # noqa: E501
        else:
            (data) = self.list_areas_with_http_info(country_code, **kwargs)  # noqa: E501
            return data

    def list_areas_with_http_info(self, country_code, **kwargs):  # noqa: E501
        """List areas  # noqa: E501

        The difference between this method and `list_areas` is that this method may return not only the data,
        but also HTTP status and headers.

        Get a list of areas where you can purchase fax numbers for a specific country. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_areas_with_http_info(country_code, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_areas_with_http_info(country_code, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param str country_code: Country code (ISO 3166-1 alpha-2) (required)
        :return: NumberAreaList
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NumberAreaList | tuple[NumberAreaList, int, HTTPHeaderDict] | ApplyResult[NumberAreaList] | ApplyResult[tuple[NumberAreaList, int, HTTPHeaderDict]]
        """
        # verify the required parameter 'country_code' is set
        if country_code is None:
            raise ValueError("Missing the required parameter `country_code` when calling `list_areas`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if country_code is not None:
            path_params['country_code'] = country_code  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2', 'personal_access_token']  # noqa: E501

        return self.api_client.call_api(
            '/shop/numbers/countries/{country_code}/areas', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NumberAreaList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=kwargs.get('async_req'),
            _return_http_data_only=kwargs.get('_return_http_data_only'),
            _preload_content=kwargs.get('_preload_content', True),
            _request_timeout=kwargs.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_countries(self, **kwargs):  # noqa: E501
        """List countries  # noqa: E501

        Get a list of countries where you can purchase fax numbers. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_countries()

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_countries(async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :return: NumbersAvailableCountries
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NumbersAvailableCountries | ApplyResult[NumbersAvailableCountries]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_countries_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_countries_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_countries_with_http_info(self, **kwargs):  # noqa: E501
        """List countries  # noqa: E501

        The difference between this method and `list_countries` is that this method may return not only the data,
        but also HTTP status and headers.

        Get a list of countries where you can purchase fax numbers. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_countries_with_http_info()

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_countries_with_http_info(async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :return: NumbersAvailableCountries
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NumbersAvailableCountries | tuple[NumbersAvailableCountries, int, HTTPHeaderDict] | ApplyResult[NumbersAvailableCountries] | ApplyResult[tuple[NumbersAvailableCountries, int, HTTPHeaderDict]]
        """

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2', 'personal_access_token']  # noqa: E501

        return self.api_client.call_api(
            '/shop/numbers/countries', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='NumbersAvailableCountries',  # noqa: E501
            auth_settings=auth_settings,
            async_req=kwargs.get('async_req'),
            _return_http_data_only=kwargs.get('_return_http_data_only'),
            _preload_content=kwargs.get('_preload_content', True),
            _request_timeout=kwargs.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_shop_numbers(self, country_code, calling_code, channel=None, contains=None, **kwargs):  # noqa: E501
        """List available numbers  # noqa: E501

        Get a list of available fax numbers for a specific area. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_shop_numbers(country_code, calling_code, channel, contains, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_shop_numbers(country_code, calling_code, channel, contains, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param str country_code: Country code (ISO 3166-1 alpha-2) (required)
        :param str calling_code: Area code (required)
        :param str channel: Channel to specify whether numbers should be 'random' or 'custom'.
        :param str contains: If 'custom' is selected as the channel, this field allows specifying numbers that should appear in the phone number.
        :return: AvailableNumberList
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AvailableNumberList | ApplyResult[AvailableNumberList]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_shop_numbers_with_http_info(country_code, calling_code, channel, contains, **kwargs)  # noqa: E501
        else:
            (data) = self.list_shop_numbers_with_http_info(country_code, calling_code, channel, contains, **kwargs)  # noqa: E501
            return data

    def list_shop_numbers_with_http_info(self, country_code, calling_code, channel=None, contains=None, **kwargs):  # noqa: E501
        """List available numbers  # noqa: E501

        The difference between this method and `list_shop_numbers` is that this method may return not only the data,
        but also HTTP status and headers.

        Get a list of available fax numbers for a specific area. (Permitted scopes: **fax:all:read**, **fax:shop:read**)  # noqa: E501
        >>> result = ShopApi().list_shop_numbers_with_http_info(country_code, calling_code, channel, contains, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().list_shop_numbers_with_http_info(country_code, calling_code, channel, contains, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param str country_code: Country code (ISO 3166-1 alpha-2) (required)
        :param str calling_code: Area code (required)
        :param str channel: Channel to specify whether numbers should be 'random' or 'custom'.
        :param str contains: If 'custom' is selected as the channel, this field allows specifying numbers that should appear in the phone number.
        :return: AvailableNumberList
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: AvailableNumberList | tuple[AvailableNumberList, int, HTTPHeaderDict] | ApplyResult[AvailableNumberList] | ApplyResult[tuple[AvailableNumberList, int, HTTPHeaderDict]]
        """
        # verify the required parameter 'country_code' is set
        if country_code is None:
            raise ValueError("Missing the required parameter `country_code` when calling `list_shop_numbers`")  # noqa: E501
        # verify the required parameter 'calling_code' is set
        if calling_code is None:
            raise ValueError("Missing the required parameter `calling_code` when calling `list_shop_numbers`")  # noqa: E501

        if contains is not None and not re.search(r'^[0-9]*$', contains):  # noqa: E501
            raise ValueError("Invalid value for parameter `contains` when calling `list_shop_numbers`, must conform to the pattern `/^[0-9]*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if country_code is not None:
            path_params['country_code'] = country_code  # noqa: E501
        if calling_code is not None:
            path_params['calling_code'] = calling_code  # noqa: E501

        query_params = []
        if channel is not None:
            query_params.append(('channel', channel))  # noqa: E501
        if contains is not None:
            query_params.append(('contains', contains))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2', 'personal_access_token']  # noqa: E501

        return self.api_client.call_api(
            '/shop/numbers/countries/{country_code}/areas/{calling_code}/numbers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AvailableNumberList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=kwargs.get('async_req'),
            _return_http_data_only=kwargs.get('_return_http_data_only'),
            _preload_content=kwargs.get('_preload_content', True),
            _request_timeout=kwargs.get('_request_timeout'),
            collection_formats=collection_formats)

    def purchase_number(self, body=None, **kwargs):  # noqa: E501
        """Purchase a number  # noqa: E501

        Purchase an available fax number. (Permitted scopes: **fax:all:edit**, **fax:shop:edit**)  # noqa: E501
        >>> result = ShopApi().purchase_number(body, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().purchase_number(body, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param PurchaseNumberRequest body: Request to purchase a fax number
        :return: PurchasedNumber
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PurchasedNumber | ApplyResult[PurchasedNumber]
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.purchase_number_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.purchase_number_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def purchase_number_with_http_info(self, body=None, **kwargs):  # noqa: E501
        """Purchase a number  # noqa: E501

        The difference between this method and `purchase_number` is that this method may return not only the data,
        but also HTTP status and headers.

        Purchase an available fax number. (Permitted scopes: **fax:all:edit**, **fax:shop:edit**)  # noqa: E501
        >>> result = ShopApi().purchase_number_with_http_info(body, )

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = ShopApi().purchase_number_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :keyword async_req bool: Run the request asynchronously
        :param PurchaseNumberRequest body: Request to purchase a fax number
        :return: PurchasedNumber
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PurchasedNumber | tuple[PurchasedNumber, int, HTTPHeaderDict] | ApplyResult[PurchasedNumber] | ApplyResult[tuple[PurchasedNumber, int, HTTPHeaderDict]]
        """

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if body is not None:
            body_params = body
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['oauth2', 'personal_access_token']  # noqa: E501

        return self.api_client.call_api(
            '/shop/numbers/purchase', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PurchasedNumber',  # noqa: E501
            auth_settings=auth_settings,
            async_req=kwargs.get('async_req'),
            _return_http_data_only=kwargs.get('_return_http_data_only'),
            _preload_content=kwargs.get('_preload_content', True),
            _request_timeout=kwargs.get('_request_timeout'),
            collection_formats=collection_formats)
