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
    def get_json_for_certain_path(root_path: str, layers: List[str], file_name: str):
        """
        :param root_path: path to root of the downloaded export
        :param layers: list of the directories you need to travel to in order to acces file_name
        :param file_name: Name of file to open
        :return:
        """
        path_to_ads = os.path.join(root_path, *layers, file_name)
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
                                                               ["ads_and_businesses"],
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
                                                               ["login_and_account_creation"],
                                                               "login_activity.json")["account_history_login_history"]

    @staticmethod
    def get_messages(path: str, username: str) -> List[dict]:
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
        for folder_name in os.listdir(os.path.join(path, "messages", "inbox")):

            if len(folder_name) < len(username): continue
            if folder_name[:len(username)] == username:
                username_folder = folder_name
                break
        if username_folder is None:
            raise FileNotFoundError(f"Username '{username}' was not found.\nPlease not that Instagram sometimes exports the "
                                    f"name instead of the username, so make sure to try both."
                                    f"At the moment, there is no chat history with '{username}'")

        return InstagramDataAnalyzer.get_json_for_certain_path(path,
                                                               ["messages", "inbox", username_folder],
                                                               "message_1.json"
                                                               )["messages"]
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
            date = date.replace(minute=1, hour=1, second=1, day=1)
            if date not in counts: counts[date] = 1
            else: counts[date] += 1
        return counts

    @staticmethod
    def get_message_length_over_time(path: str, chat_name: str) -> Dict[str, List[List[int]]]:
        """
        :param path: root to download export
        :param chat_name: name of chat history to count
        :return:
        A dictionary that maps usernames to lists that contain the lengths of their messages and the timestamps of said messages
        {"Name1": [ [message1, message2 ... messageN], [timestamp1, timestamp2 ... timestampN] ],
         "Name2": ...}
        """
        messages = InstagramDataAnalyzer.get_messages(path, chat_name)

        senders = {} # senders = {"Name": [ [message1, message2 ... messageN], [timestamp1, timestamp2 ... timestampN] ] }

        #we loop in reverse because the messages are ordered from most recent to oldest
        for i in range(len(messages) - 1, -1, -1):
            if "content" not in messages[i]: continue #it's a message that contains an image
            sender = messages[i]["sender_name"]
            timestamp = messages[i]["timestamp_ms"]
            value = messages[i]["content"]

            if sender not in senders: senders[sender] = [[len(value)], [timestamp]]
            else:
                senders[sender][0].append(len(value))
                senders[sender][1].append(timestamp)
        return senders
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    alpha = InstagramDataAnalyzer.get_messages(path_to_data, "test")
    print(alpha[0])