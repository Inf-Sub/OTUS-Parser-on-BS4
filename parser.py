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
    def __init__(self, url: str = None, deep: int = None) -> None:
        self._urls = None
        self._deep = None

        self._cur_url = None
        self._cur_parse_urls = None
        self._cur_deep = None
        self._cur_domain = None
        self._cur_check_url = None
        self._https = 'https://'

        self._count = 0

        self._save_file = 'result.json'
        self._re_domain = \
            r'https?:\/\/((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])\/.*'

        self.set_url(url=url)
        self.set_deep(deep=deep)

    def set_url(self, url: str) -> None:
        urls = {}
        if url is not None:
            url = url if self._check_domain(url) else f'{self._https}{url}'
            urls.update({url: {}})
            self._urls = urls

    def set_deep(self, deep: int = 1) -> None:
        self._deep = deep

    def print_result(self) -> None:
        print(json.dumps(self._urls, indent=4, ensure_ascii=False, sort_keys=True))

    def save_result(self, file: str = None) -> None:
        if file is None:
            file = self._save_file
        with open(file, 'w') as json_file:
            json.dump(self._urls, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    def _get_url(self, urls: dict, deep: int = 0) -> None:
        if deep < self._deep:
            deep += 1

            for url in urls:
                self._count += 1
                print(f'count: {self._count}\t| deep: {deep}\t| url: {url}')

                self._get_urls_from_page(url)
                urls[url] = self._cur_parse_urls

                if urls[url]:
                    self._get_url(urls=urls[url], deep=deep)

    def _check_domain(self, url: str) -> str:
        match = re.fullmatch(self._re_domain, url)
        return match[1] if match and match[1] else ''

    def _get_domain_from_url(self, url: str) -> bool:
        self._cur_domain = self._check_domain(url)
        return True if self._cur_domain else False

    def _check_external_url(self, url: str) -> bool:
        domain = self._check_domain(url)
        return True if domain and domain != self._cur_domain else False

    def _get_urls_from_page(self, url: str) -> None:
        urls = {}
        ua = UserAgent(browsers=['edge', 'firefox', 'chrome'])

        headers = {'User-Agent': ua.chrome}

        if not self._get_domain_from_url(url):
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
                if self._check_external_url(link.get('href')):
                    urls.update({link.get('href'): {}})

        self._cur_parse_urls = urls

    def run(self):
        self._get_url(urls=self._urls, deep=0)


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
