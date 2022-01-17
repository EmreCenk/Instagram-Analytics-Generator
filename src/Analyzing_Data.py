import datetime
import os
from contextlib import contextmanager
from typing import List, Dict
from Retreiving_Data import InstagramDataRetreiver
from dateutil import parser
from src import utils
from datetime import datetime
from collections import defaultdict
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
    def count_year_and_months_for_login_activity(path: str):
        """
        :param path: root to export download
        :return: a dictionary that maps year-month of the activity to how many logins that year/month.
        Dictionary format:
        {'2022-1': 420,
         '2021-11': 69,
          '2021-10': 96 ...}
        """
        dates = InstagramDataRetreiver.get_login(path)
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
        messages = InstagramDataRetreiver.get_messages(path, chat_name)

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

    @staticmethod
    def get_word_distribution(path: str, chat_name: str) -> Dict[str, int]:
        """
        :param path: root to download export
        :param chat_name: name of chat history to count
        :return:
        A dictionary that maps words to how many times they were used in the chat.
        {"Word1": value, "word2": 123 ...}
        """
        counting = {}
        messages = InstagramDataRetreiver.get_messages(path, chat_name)
        for i in range(len(messages) - 1, -1, -1):
            if "content" not in messages[i]: continue #it's a message that contains an image
            value = messages[i]["content"].lower().replace(",", "")
            if "reacted â¤ï¸ to your message" in value: continue #Reacting to messages contaminate the word count
            for word in value.split(" "):
                if word == "": continue
                if word not in counting: counting[word] = 1
                else: counting[word] += 1
        return counting

    @staticmethod
    def count_active_chats_per_day(path: str, username: str) -> (Dict[datetime.date, str], Dict[datetime.date, str]):
        """
        counts number of active chats per day
        :param path: path to root folder
        :param username: Username of the owner of the folder.
        todo: add functionality to infer who the owner is by finding the intersection of usernames from 2 dms.

        :return: (received messages per day, sent messages per day)
        2 dictionaries that map dates to how many active chats are on that day.
        The first dictionary -> how many messages were received on each date
        Second Dictionary -> how many messages the user sent on each date
        """

        chats = InstagramDataRetreiver.list_chats(path)
        time_string = utils.get_time_string(interval=2)

        def zero(): return 0
        received = defaultdict(zero)
        sent = defaultdict(zero)
        for conversation_name in chats:
            convo = InstagramDataRetreiver.get_messages(path, conversation_name)
            for message in convo:
                message_date = message["timestamp_ms"]
                message_date = datetime.fromtimestamp(int(message_date / 1000))
                message_date = parser.parse(message_date.strftime(time_string))
                if message["sender_name"] == username: sent[message_date] += 1
                else: received[message_date] += 1

        return received, sent
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    for k in InstagramDataAnalyzer.count_active_chats_per_day(path_to_data, "emre.cenk99"):
        print(k)
    # print(
    #     InstagramDataAnalyzer.get_word_distribution(path_to_data, "thesimpsons_457uupaoka")
    # )
    # alpha = InstagramDataRetreiver.get_messages(path_to_data, "test")
    # print(alpha[0])