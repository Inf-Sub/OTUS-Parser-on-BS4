import json
import requests
import re
from bs4 import BeautifulSoup as bs


class Parser:
    def __init__(self, url: str = None, deep: int = 1) -> None:
        self.__urls = None
        self.__deep = None

        self.__cur_url = None
        self.__cur_parse_urls = None
        self.__cur_deep = None

        self.__save_file = 'result.json'
        self.__re_domain = r'https?:\/\/(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\/'

        self.set_url(url=url, urls={})
        self.set_deep(deep=deep)

    def set_url(self, url: str, urls: dict = None) -> None:
        if urls is None:
            urls = {}
        if url is not None:
            urls.update({url: {}})
            self.__urls = urls

    # ???
    def __get_url(self, urls: dict, deep: int = 0) -> None:
        if deep < self.__deep:
            deep += 1
            print(deep)
            for url in urls:
                self.__get_urls_from_page(url)
                urls[url] = self.__cur_parse_urls

                if urls[url]:
                    self.__get_url(urls=urls[url], deep=deep)

    def __get_urls_from_page(self, url: str) -> None:
        urls = {}
        # urls.update({'-1-': {}})
        # urls.update({'-2-': {}})
        # urls.update({'-2-': {}})
        # urls.update({'-3-': {}})

        response = requests.get(url)
        if response.status_code != 200:
            return

        soup = bs(response.text, 'html.parser')


        # urls.update({})

        self.__cur_parse_urls = urls

        pass

    def set_deep(self, deep: int = 1) -> None:
        self.__deep = deep

    def print_result(self) -> None:
        print(json.dumps(self.__urls, indent=4, ensure_ascii=False, sort_keys=True))

    def save_result(self, file: str = None) -> None:
        if file is None:
            file = self.__save_file
        with open(file, 'w') as json_file:
            json.dump(self.__urls, json_file, indent=4, ensure_ascii=False, sort_keys=True)

    def run(self):
        self.__get_url(urls=self.__urls, deep=0)

        # for url in urls:
        #     self.__curl = url


    # for sub_item in os.listdir(path):
    #     abs_path = os.path.join(path, sub_item)
    #
    #     if os.path.isdir(abs_path):
    #         # Если полученный элемент - директория, вызываем рекурсивно функцию, передав в нее путь к директории.
    #         await find_files(path=abs_path, pattern=pattern, dict_with_files=dict_with_files)


if __name__ == '__main__':
    start_url = r'https://www.mos.ru/'
    immersion_depth = 3

    otus_parser = Parser(url=start_url, deep=immersion_depth)

    try:
        # # otus_parser
        # otus_parser.print_result()
        # otus_parser.save_result()
        otus_parser.run()
        otus_parser.print_result()

    except (KeyboardInterrupt, SystemExit):
        print('Program was stopped by user.')

