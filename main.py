import os
from contextlib import contextmanager
from typing import List, Dict
import json

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
                                                               "advertisers_using_your_activity_or_information")["ig_custom_audiences_all_types"]


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    companies = InstagramDataAnalyzer.get_marketing_list(path_to_data)
    print(len(companies))