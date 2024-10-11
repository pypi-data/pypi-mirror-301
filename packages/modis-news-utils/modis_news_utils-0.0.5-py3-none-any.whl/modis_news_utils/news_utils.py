from typing import Optional
from urllib.parse import urljoin

import jmespath
import requests
from requests import RequestException, Response, JSONDecodeError

from .custom_types import (URL, UtilName, UtilsInfo, AvailableMethods, UtilMethodName, HTML, NewsAttributes,
                           LanguageCode, SectionItem)


class NewsUtils:
    """
    Class for working with the news utils service.

    :param server_url: Base URL of news utils service (URL)
    :param settings: Settings for news utils service (Optional[dict], default: None)
    """
    _instance: Optional['NewsUtils'] = None

    def __new__(cls, server_url: URL, settings: Optional[dict] = None) -> 'NewsUtils':
        """
        Ensures that only one instance of NewsUtils is created, implementing the singleton pattern.
        """
        if not cls._instance:
            cls._instance = super(NewsUtils, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, server_url: URL, settings: Optional[dict] = None) -> None:
        """
        Initializes a NewsUtils instance.

        :param server_url: Base URL of news utils service (URL)
        :param settings: Settings for news utils service (Optional[dict], default: None)
        :return: None
        """
        if self._initialized:
            return
        self._health_check(server_url)

        utils_urls = self._get_utils_urls(server_url)
        self._utils_info = self._get_utils_info(utils_urls)

        self._settings = None
        self.set_settings(settings)
        self._initialized = True

    @staticmethod
    def _health_check(server_url: URL) -> None:
        """
        Checks if the news utils service is available.

        :param server_url: Base URL of the service (URL)
        :raises RequestException: If the service is not available or the response is incorrect
        :return: None
        """
        try:
            response = requests.get(server_url)
            response.raise_for_status()
        except requests.RequestException as error:
            raise requests.RequestException(f'News utils service is not available. {error}')
        try:
            assert response.json() == "News utils service is running"
        except (JSONDecodeError, AssertionError):
            raise RequestException(
                'News utils service is responding incorrectly, please check the server URL.'
            )

    @staticmethod
    def _get_utils_urls(server_url: URL) -> dict[UtilName, URL]:
        """
        Gets URLs of news utils.

        :param server_url: Base URL of the service (URL)
        :return: A dictionary mapping utility names to their endpoint URLs (dict[UtilName, URL])
        """
        utils_urls = {
            'news_attributes_extractors': urljoin(server_url, '/get_news_attributes/'),
            'news_classifiers': urljoin(server_url, '/is_news_article/'),
            'news_template_removers': urljoin(server_url, '/get_news_with_removed_template/'),
            'section_items_extractors': urljoin(server_url, '/get_section_items/')
        }

        return utils_urls

    @staticmethod
    def _get_utils_info(utils_urls: dict[UtilName, URL]) -> UtilsInfo:
        """
        Gets an information dictionary about news utils.

        :param utils_urls: A dictionary mapping utility names to their URLs (dict[UtilName, URL])
        :return: A dictionary mapping utility names to their URLs and available methods (UtilsInfo)
        """
        utils_info = {}
        for util, util_url in utils_urls.items():
            response = requests.get(util_url)
            if response.status_code != 200:
                raise RequestException(f'{util} is not available: {response.text}')
            available_methods = response.json()
            utils_info[util] = {
                'util_url': util_url,
                'available_methods': available_methods,
            }
        return utils_info

    def get_available_methods(self) -> AvailableMethods:
        """
        Gets available methods for each news util.

        :return: A dictionary mapping utility names to their available methods (AvailableMethods)
        """
        return {util: info['available_methods'] for util, info in self._utils_info.items()}

    def set_settings(self, settings: Optional[dict] = None) -> None:
        """
        Sets the settings for the news utils service.

        :param settings: Dictionary containing settings for the service (Optional[dict], default: None)
        :return: None
        """
        self._settings = settings if settings else {}

    def extract_news_attributes(self, method: UtilMethodName, html: HTML) -> NewsAttributes:
        """
        Extracts news attributes from the page.

        :param method: Method name (UtilMethodName)
        :param html: Page HTML (HTML)
        :return: Extracted news attributes (NewsAttributes)
        :raises NotImplementedError: If the method is not implemented
        """
        util = 'news_attributes_extractors'
        if method not in self._utils_info[util]['available_methods']:
            raise NotImplementedError(f'News attributes extractor method is not implemented: {method}')
        args = {'html': html}
        method_settings = jmespath.search(f'{util.upper()}.{method}', self._settings) or {}
        return self._request_util(util=util, method=method, args=args, settings=method_settings).json()

    def is_news_article(self, method: UtilMethodName, html: HTML, url: Optional[URL] = None) -> bool:
        """
        Checks if the page is a news page.

        :param method: Method name (UtilMethodName)
        :param html: Page HTML (HTML)
        :param url: Page URL (Optional[URL], default: None)
        :return: Whether the page is news (bool)
        :raises NotImplementedError: If the method is not implemented
        """
        util = 'news_classifiers'
        if method not in self._utils_info[util]['available_methods']:
            raise NotImplementedError(f'News classifier method is not implemented: {method}')
        args = {'html': html, 'url': url}
        method_settings = jmespath.search(f'{util.upper()}.{method}', self._settings) or {}
        return self._request_util(util=util, method=method, args=args, settings=method_settings).json()

    def remove_template_from_news(self, method: UtilMethodName, url: URL) -> HTML:
        """
        Returns the news page with removed template.

        :param method: Method name (UtilMethodName)
        :param url: Page URL (URL)
        :return: News page with removed template (HTML)
        :raises NotImplementedError: If the method is not implemented
        """
        util = 'news_template_removers'
        if method not in self._utils_info[util]['available_methods']:
            raise NotImplementedError(f'News template remover is not implemented: {method}')
        args = {'url': url}
        method_settings = jmespath.search(f'{util.upper()}.{method}', self._settings) or {}
        return self._request_util(util=util, method=method, args=args, settings=method_settings).json()

    def extract_section_items(self, method: UtilMethodName, html: HTML, from_code: LanguageCode) -> list[SectionItem]:
        """
        Extracts items from the section page.

        :param method: Method name (UtilMethodName)
        :param html: Page HTML (HTML)
        :param from_code: Two-letter page language code (ISO 639-1, LanguageCode)
        :return: List of section items (list[SectionItem])
        :raises NotImplementedError: If the method is not implemented
        """
        util = 'section_items_extractors'
        if method not in self._utils_info[util]['available_methods']:
            raise NotImplementedError(f'Section items extractor method is not implemented: {method}')
        args = {'html': html, 'from_code': from_code}
        return self._request_util(util=util, method=method, args=args).json()

    def _request_util(self, util: UtilName, method: UtilMethodName,
                      args: dict, settings: Optional[dict] = None) -> Response:
        """
        Makes a POST request to the specified news util method with the provided arguments and settings.

        :param util: Utility name (UtilName)
        :param method: Method name (UtilMethodName)
        :param args: Arguments to pass to the method as JSON (dict)
        :param settings: Settings to pass to the method as JSON (Optional[dict], default: None)
        :return: The response from the server (Response)
        """
        util_url = self._utils_info[util]['util_url']
        if settings is None:
            response = requests.post(urljoin(util_url, method), json={'args': args})
        else:
            response = requests.post(urljoin(util_url, method), json={'args': args, 'settings': settings})
        if response.status_code != 200:
            self._parse_error(response, util, method)
        return response

    @staticmethod
    def _parse_error(error_response: Response, util: UtilName, method: UtilMethodName) -> None:
        """
        Parses the error response from the service.

        :param error_response: Error response (Response)
        :param util: Name of the utility (UtilName)
        :param method: Name of the method (UtilMethodName)
        :raises RequestException: If the error response status code is not 200 and not 422
        :raises ValueError: If the error response status code is 422 and the error type is 'value_error'
        :raises TypeError: If the error response status code is 422 and the error type is 'type_error'
        """
        method_path = f'Error in {util}.{method}'
        if error_response.status_code == 500:
            raise RequestException(f'{method_path}: {error_response.text}, '
                                   f'try to check the correctness of the arguments')

        if error_response.status_code == 422:
            if error_detail := jmespath.search('detail[0]', error_response.json()):
                locate = error_detail['loc']
                len_locate = len(locate)
                message = error_detail['msg']
                error_type = error_detail['type']

                if len_locate == 3:
                    error_location = f'{method_path} in {locate[1]}. {locate[2]}'
                elif len_locate == 2:
                    error_location = f'{method_path} in {locate[1]}'
                else:
                    error_location = f'{method_path}'

                if 'value_error' in error_type:
                    raise ValueError(f'{error_location}: {message}')

                if 'type_error' in error_type:
                    raise TypeError(f'{error_location}: {message}')

                raise ValueError(f'{error_location}. Unexpected error type: {error_type}. Message: {message}')

            if error_detail := jmespath.search('detail', error_response.json()):
                if isinstance(error_detail, str):
                    raise ValueError(f'{method_path}: {error_detail}')

        raise RequestException(f'{method_path}: {error_response.text}')
