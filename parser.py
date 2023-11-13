import json
import requests
import re
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import time


start_time = time.time()


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Parser:
    def __init__(self, url: str = None, deep: int = 1) -> None:
        self.__urls = None
        self.__deep = None

        self.__cur_url = None
        self.__cur_parse_urls = None
        self.__cur_deep = None
        self.__cur_domain = None
        self.__cur_check_url = None
        self.__https = 'https://'

        self.__count = 0

        self.__save_file = 'result.json'
        self.__re_domain = \
            r'https?:\/\/((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])\/.*'

        self.set_url(url=url)
        self.set_deep(deep=deep)

    def set_url(self, url: str) -> None:
        urls = {}
        if url is not None:
            url = url if self.__check_domain(url) else f'{self.__https}{url}'
            urls.update({url: {}})
            self.__urls = urls

    def set_deep(self, deep: int = 1) -> None:
        self.__deep = deep

    def print_result(self) -> None:
        print(json.dumps(self.__urls, indent=4, ensure_ascii=False, sort_keys=True))

    def save_result(self, file: str = None) -> None:
        if file is None:
            file = self.__save_file
        with open(file, 'w') as json_file:
            json.dump(self.__urls, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    def __get_url(self, urls: dict, deep: int = 0) -> None:
        if deep < self.__deep:
            deep += 1

            for url in urls:
                self.__count += 1
                print(f'count: {self.__count}\t| deep: {deep}\t| url: {url}')

                self.__get_urls_from_page(url)
                urls[url] = self.__cur_parse_urls

                if urls[url]:
                    self.__get_url(urls=urls[url], deep=deep)

    def __check_domain(self, url: str) -> str:
        match = re.fullmatch(self.__re_domain, url)
        return match[1] if match and match[1] else ''

    def __get_domain_from_url(self, url: str) -> bool:
        self.__cur_domain = self.__check_domain(url)
        return True if self.__cur_domain else False

    def __check_external_url(self, url: str) -> bool:
        domain = self.__check_domain(url)
        return True if domain and domain != self.__cur_domain else False

    def __get_urls_from_page(self, url: str) -> None:
        urls = {}
        ua = UserAgent(browsers=['edge', 'firefox', 'chrome'])

        headers = {'User-Agent': ua.chrome}

        if not self.__get_domain_from_url(url):
            print(f'{Bcolors.WARNING}Warning: Domain URL "{url}" is invalid.{Bcolors.ENDC}')
            return

        try:
            response = requests.get(url, headers=headers)
            # response = grequests.get(url, headers=headers)
        except:
            print(f'{Bcolors.WARNING}Warning: requests.get({url}){Bcolors.ENDC}')
            return

        if response.status_code != 200:
            print(f'{Bcolors.WARNING}Warning: Response Status Code: {response}\tURL: {url}{Bcolors.ENDC}')
            return

        soup = bs(response.text, 'html.parser')

        for link in soup.find_all('a'):
            if link.get('href') is not None:
                if self.__check_external_url(link.get('href')):
                    urls.update({link.get('href'): {}})

        self.__cur_parse_urls = urls

    def run(self):
        self.__get_url(urls=self.__urls, deep=0)


if __name__ == '__main__':
    start_url = r'https://www.google.com/search?q=requests'
    immersion_depth = 2

    otus_parser = Parser(url=start_url, deep=immersion_depth)

    try:
        otus_parser.run()
        print("--- %s seconds ---" % (time.time() - start_time))

        otus_parser.print_result()

        otus_parser.save_result()

    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')
