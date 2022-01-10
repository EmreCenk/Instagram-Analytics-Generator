import os
from contextlib import contextmanager
from typing import List, Dict
import json
from dateutil import parser

@contextmanager
def different_cwd(path: str):
    """
    :param path: Path that you want to change directory to
    """
    oldpwd=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

class InstagramDataAnalyzer():

    @staticmethod
    def get_json_for_certain_path(root_path: str, second_layer: str, third_layer: str):
        """
        :param root_path: path to root of the downloaded export
        :param second_layer: the second directory from root
        :param third_layer: Name of file to open
        :return:
        """
        path_to_ads = os.path.join(root_path, second_layer, third_layer)
        with open(path_to_ads) as ad_file:
            data = json.load(ad_file)
        return data

    @staticmethod
    def get_marketing_list(path: str) -> List[Dict]:
        """
        :param path: Path to root folder of downloaded export
        :return: list of company dictionaries.
        The entries are in the following format:
        {
        'advertiser_name': 'name',
        'has_data_file_custom_audience': True,
        'has_remarketing_custom_audience': True,
        'has_in_person_store_visit': False
        }
        """
        # Finding path to ads from root:
        return InstagramDataAnalyzer.get_json_for_certain_path(path,
                                                               "ads_and_businesses",
                                                               "advertisers_using_your_activity_or_information.json")["ig_custom_audiences_all_types"]

    @staticmethod
    def get_login(path: str) -> List[Dict]:
        """
        :param path: root path to downloaded exports
        :return: list of dictionary that includes an entry for every login
        The entries are in the following format:
        {'title': '2022-01-10T05:47:01+00:00',
         'media_map_data': {},
         'string_map_data': {'Cookie Name': {'href': '',
                                             'timestamp': 0,
                                             'value': '*************************JlO'},
                             'IP Address': {'href': '',
                                            'timestamp': 0,
                                            'value': '72.53.192.5'},
                             'Language Code': {'href': '',
                                               'timestamp': 0,
                                               'value': 'en'},
                             'Time': {'href': '', 'timestamp': 1641793621, 'value': ''},
                             'User Agent': {'href': '',
                                            'timestamp': 0,
                                            'value': 'Mozilla/5.0 (Windows NT 10.0; '
                                                     'Win64; x64) AppleWebKit/537.36 '
                                                     '(KHTML, like Gecko) '
                                                     'Chrome/96.0.4664.110 '
                                                     'Safari/537.36'}}
        }
        """
        return InstagramDataAnalyzer.get_json_for_certain_path(path,
                                                               "login_and_account_creation",
                                                               "login_activity.json")["account_history_login_history"]
    @staticmethod
    def count_year_and_months_for_login_activity(path: str):
        """
        :param path: root to export download
        :return: a dictionary that maps year-month of the activity to how many logins that year/month.
        Dictionary format:
        {'2022-1': 420,
         '2021-11': 69,
          '2021-10': 96 ...}
        """
        dates = InstagramDataAnalyzer.get_login(path)
        counts = {}
        for login_activity in dates:
            date_of_login = login_activity["title"]
            date = parser.parse(date_of_login)
            date = str(date.year) + "-" + str(date.month)
            if date not in counts: counts[date] = 1
            else: counts[date] += 1
        return counts


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    companies = InstagramDataAnalyzer.get_marketing_list(path_to_data)
    w = InstagramDataAnalyzer.count_year_and_months_for_login_activity(path_to_data)
    print(w)
