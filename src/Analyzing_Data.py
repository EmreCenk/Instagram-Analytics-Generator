import datetime
import os
from contextlib import contextmanager
from typing import List, Dict
from Retreiving_Data import InstagramDataRetreiver
from dateutil import parser
from src import utils
from datetime import datetime
from collections import defaultdict
from warnings import warn

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
    def count_number_of_messages_per_day(path: str, name_of_owner: str = "", interval: int = 2) -> (Dict[datetime.date, str], Dict[datetime.date, str]):
        """
        counts number of active chats per day
        :param path: path to root folder
        :param name_of_owner: Instagram name of owner. The messages sent by this name will be filtered out, and placed into a separate dictionary (the second one) : if 'name_of_owner' is left as an empty string, the first dictionary will contain messages sent by everyone, and the second message will be empty.
        :return: (received messages per day, sent messages per day)
        2 dictionaries that map dates to how many active chats are on that day.
        The first dictionary -> how many messages were received on each date
        Second Dictionary -> how many messages 'name_of_owner' sent on each date
        """


        time_string = utils.get_time_string(interval)

        def zero(): return 0
        received = defaultdict(zero)
        sent = defaultdict(zero)
        for message, name in utils.loop_through_every_message(path):
            #the following could be a single line, but I think it's more readable this way
            message_date = message["timestamp_ms"]
            message_date = datetime.fromtimestamp(int(message_date / 1000))
            message_date = parser.parse(message_date.strftime(time_string))

            if message["sender_name"] == name_of_owner: sent[message_date] += 1
            else: received[message_date] += 1

        if len(sent) == 0 and name_of_owner != "":
            warn(f"\nIt appears {name_of_owner} has sent 0 messages in the entire history of your account. This is probably due to a mistake in the 'name_of_owner' variable specified.\nPlease make sure '{name_of_owner}' is the correct name.")
        return received, sent

    @staticmethod
    def count_number_of_active_dms(path: str, interval: int = 2) -> Dict[datetime.date, set]:
        """
        counts number of active chats per day. Very similar to InstagramDataAnalyzer.count_active_chats_per_date

        :param path: path to root folder
        :param name_of_owner: Instagram name of owner. The messages sent by this name will be filtered out, and placed into a separate dictionary (the second one) : if 'name_of_owner' is left as an empty string, the first dictionary will contain messages sent by everyone, and the second message will be empty.
        :return: {
        date: {"name1", "name2"}
        }

        """
        time_string = utils.get_time_string(interval)
        mapped = defaultdict(set)
        for message, convo_name in utils.loop_through_every_message(path):
            #the following could be a single line, but I think it's more readable this way
            message_date = message["timestamp_ms"]
            message_date = datetime.fromtimestamp(int(message_date / 1000))
            message_date = parser.parse(message_date.strftime(time_string))

            mapped[message_date].add(convo_name)
            # todo: implement function that counts "number of people exposed to"
            # this function would add message["sender_name"] instead of convo_name

        return mapped
    #todo: implement most active hours/days/months for messaging (pie chart or bar graph)
    #todo: find rankings between friends. Who did you exchange most chats with? Who sent you most messages? Who did you send most messages to? Who did you interact with most days? etc.



if __name__ == '__main__':
    from pprint import pprint
    print = pprint
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    print(InstagramDataAnalyzer.count_number_of_active_dms(path_to_data))
    # for k in InstagramDataAnalyzer.count_active_chats_per_date(path_to_data, "Emre Cenk"):
    #     print(k)
    # print(
    #     InstagramDataAnalyzer.get_word_distribution(path_to_data, "thesimpsons_457uupaoka")
    # )
    # alpha = InstagramDataRetreiver.get_messages(path_to_data, "test")
    # print(alpha[0])




















