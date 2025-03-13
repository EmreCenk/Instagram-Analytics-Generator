import os
import json
from typing import List, Dict

class InstagramDataRetreiver():

    @staticmethod
    def get_json_for_certain_path(root_path: str, layers: List[str], file_name: str):
        """
        Exports the json values from a given path as dictionaries
        :param root_path: path to root of the downloaded export
        :param layers: list of the directories you need to travel to in order to access file_name
        :param file_name: Name of file to open
        :return:
        """
        path_to_ads = os.path.join(root_path, *layers, file_name)
        with open(path_to_ads) as ad_file:
            data = json.load(ad_file)
        return data

    @staticmethod
    def get_personal_information(root_path: str) -> Dict:
        """
        Parses personal information json file
        :param root_path: path to root folder
        :return: A dictionary with the following format:
        {'media_map_data': {'Profile Photo': {'creation_timestamp': 1628451477,
                                              'title': '',
                                              'uri': 'media/other/233868629_532664164608070_1766641927110870425_n_17894922671249380.jpg'}},
         'string_map_data': {'Bio': {'href': '', 'timestamp': 0, 'value': "sjam '22"},
                             'Gender': {'href': '', 'timestamp': 0, 'value': 'male'},
                             'Name': {'href': '', 'timestamp': 0, 'value': 'Emre Cenk'},
                             'Phone Confirmation Method': {'href': '',
                                                           'timestamp': 0,
                                                           'value': 'Unknown'},
                             'Phone Confirmed': {'href': '',
                                                 'timestamp': 0,
                                                 'value': 'True'},
                             'Phone Number': {'href': '',
                                              'timestamp': 0,
                                              'value': '+905537360604'},
                             'Private Account': {'href': '',
                                                 'timestamp': 0,
                                                 'value': 'True'},
                             'Username': {'href': '',
                                          'timestamp': 0,
                                          'value': 'emre.cenk99'}},
         'title': 'User Information'}
        """
        return InstagramDataRetreiver.get_json_for_certain_path(root_path,
                                                                ["personal_information", "personal_information"],
                                                                "personal_information.json")["profile_user"][0]
    @staticmethod
    def get_name(root_path: str) -> str:
        """
        returns the name of the user as saved in the instagram export file.
        :param root_path: path to root file
        :return: instagram name of user
        """
        return InstagramDataRetreiver.get_personal_information(root_path)["string_map_data"]["Name"]["value" \
                                                                                                     ""]
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
        return InstagramDataRetreiver.get_json_for_certain_path(path,
                                                               ["ads_and_businesses"],
                                                               "advertisers_using_your_activity_or_information.json")["ig_custom_audiences_all_types"][0]

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
        return InstagramDataRetreiver.get_json_for_certain_path(path,
                                                               ["login_and_account_creation"],
                                                               "login_activity.json")["account_history_login_history"]

    @staticmethod
    def list_chats(root_path: str):
        """
        :param root_path: path to export root
        :return: list of chat names
        """
        return os.listdir(os.path.join(root_path, "your_instagram_activity", "messages", "inbox"))
    @staticmethod
    def get_messages(path: str, username: str) -> List[Dict]:
        """
        :param path: root path
        :param username: username of person you want to extract chats with
        :return: List of dictionaries. Each index is a separate message stored as a dictionary.
        Each entry in the list has the following format:
        {'sender_name': 'Emre Cenk',
         'timestamp_ms': 1641678929234,
         'content': "message content",
         'type': 'Generic',
         'is_unsent': False}

        """
        username_folder = None
        for folder_name in InstagramDataRetreiver.list_chats(path):

            if len(folder_name) < len(username): continue
            if folder_name[:len(username)] == username:
                username_folder = folder_name
                break
        if username_folder is None:
            raise FileNotFoundError(f"Username '{username}' was not found.\nPlease not that Instagram sometimes exports the "
                                    f"name instead of the username, so make sure to try both. "
                                    f"At the moment, there is no chat history with '{username}'")

        return InstagramDataRetreiver.get_json_for_certain_path(path,
                                                               ["your_instagram_activity", "messages", "inbox", username_folder],
                                                               "message_1.json"
                                                               )["messages"]

    @staticmethod
    def get_followers(path: str) -> List[Dict]:
        """
        Gets a list of followers from path
        :param path: root path
        :return: List of dictionaries. Each index is a separate follower stored as a dictionary.
        Each entry in the list has the following format:
        {'media_list_data': [],
         'string_list_data': [{'href': 'https://www.instagram.com/thepipernews',
                               'timestamp': 1640891412,
                               'value': 'thepipernews'}],
         'title': ''}

        """
        try:
            return InstagramDataRetreiver.get_json_for_certain_path(path, ["connections", "followers_and_following"], "followers.json")["relationships_followers"]
        except:
            return InstagramDataRetreiver.get_json_for_certain_path(path, ["connections", "followers_and_following"], "followers_1.json")

    @staticmethod
    def get_following(path: str):
        """
        Gets a list of followers from path
        :param path: root path
        :return: List of dictionaries. Each index is a separate follower stored as a dictionary.
        Each entry in the list has the following format:
        {'media_list_data': [],
         'string_list_data': [{'href': 'https://www.instagram.com/thepipernews',
                               'timestamp': 1640891412,
                               'value': 'thepipernews'}],
         'title': ''}

        """
        try:
            return InstagramDataRetreiver.get_json_for_certain_path(path, ["followers_and_following"], "following.json")["relationships_following"]
        except:
            return InstagramDataRetreiver.get_json_for_certain_path(path, ["connections", "followers_and_following"], "following.json")["relationships_following"]


if __name__ == '__main__':
    import os
    from pprint import pprint
    from dotenv import load_dotenv
    load_dotenv()
    print = pprint
    path_to_data = os.environ["path_to_instagram_export_download"]
    print(
        InstagramDataRetreiver.get_personal_information(path_to_data)
    )
