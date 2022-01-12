from src.Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from typing import Dict

class InstagramDataVisualizer:

    @staticmethod
    def visualize_logins(path: str) -> None:
        """
        Visualizes number of logins over time
        :param path: path to root for user
        :return: None
        """
        counted = InstagramDataAnalyzer.count_year_and_months_for_login_activity(path)
        xs, ys = [], []
        for c in counted:
            xs.append(c)
            ys.append(counted[c])

        xs.reverse()
        ys.reverse()
        plt.plot(xs, ys, label="login number")
        plt.xlabel("date (year-month)")
        plt.ylabel("number of logins")
        plt.title(f"Number of logins over time'")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_message_length_over_time(path: str,
                                           chat_name: str,
                                           interval: int = 3) -> None:
        """
        Visualizes message length over time for any given chat. Each user is plotted separately.
        :param path: path to root of download
        :param chat_name: name of group chat (according to the download)
        :param interval: an integer between 0 and 3 inclusive that specifies what interval the messages will be plotted in.
        The following is the meaning for interval values:
        0 -> yearly intervals
        1 -> monthly intervals
        2 -> daily intervals
        3 -> hourly interval
        4 -> Minute intervals (may misrepresent data since a long message will create extreme spikes)
        NOTE: Hourly intervals for chats that span a long period of time is not recommended.
        :return: None
        """

        if interval < 0 or interval > 4:
            raise ValueError(f"'interval' argument must be one of 0, 1, 2, 3, 4."
                             f"\nThe interval meanings are as follows:"
                             "\n0 -> yearly intervals\n1 -> monthly intervals\n2 -> daily intervals\n3 -> hourly interval\n4 -> Minute intervals (may misrepresent data since a long message will create extreme spikes)"
                             f"\n\n{interval} is not a valid interval")
        times = ["%Y", "%m", "%d", "%H"]
        time_string = ""
        for i in range(min(len(times), interval + 1)): time_string += times[i] + "-"
        time_string = time_string[:-1]
        if interval == 4: time_string += ":%M"

        colors = ['red', 'blue', 'darkkhaki', 'green', 'orange', 'purple', 'brown', 'pink', 'teal', 'maroon', 'cyan', 'magenta', 'navy', 'lime', 'olive', 'lavender', 'mauve', 'umber', 'murk', 'black', 'gray']
        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)
        for user_index, username in enumerate(to_plot):
            days = {}
            timestamps, messages = to_plot[username][1], to_plot[username][0]
            for i in range(len(timestamps)):
                timestamps[i] = datetime.fromtimestamp(int(timestamps[i])/1000)
                cache = parser.parse(timestamps[i].strftime(time_string))

                if cache in days: days[cache] += messages[i]
                else: days[cache] = messages[i]
            x_axis, y_axis = [], []

            for date in days:
                x_axis.append(date)
                y_axis.append(days[date])

            plt.plot(x_axis, y_axis, label=username, color = colors[user_index%len(colors)])

        plt.title(f"Message length over time with '{chat_name}'")
        plt.xlabel("date (year-month)")
        plt.ylabel("length of message")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_message_count_over_time(path: str, chat_name: str) -> None:
        """
        Vizualizes message count over time for a given chat.
        :param path: path to root
        :param chat_name: name of chat
        :return: None
        """
        colors = ['red', 'blue', 'darkkhaki', 'green', 'orange', 'purple', 'brown', 'pink', 'teal', 'maroon', 'cyan', 'magenta', 'navy', 'lime', 'olive', 'lavender', 'mauve', 'umber', 'murk', 'black', 'gray']



        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)
        for user_index, username in enumerate(to_plot):
            days = {}
            timestamps, messages = to_plot[username][1], to_plot[username][0]
            for i in range(len(timestamps)):
                timestamps[i] = datetime.fromtimestamp(int(timestamps[i])/1000)
                cache = parser.parse(timestamps[i].strftime('%Y-%m-%d'))

                if cache in days: days[cache] += 1
                else: days[cache] = 1
            x_axis, y_axis = [], []

            for date in days:
                x_axis.append(date)
                y_axis.append(days[date])

            plt.plot(x_axis, y_axis, label=username, color = colors[user_index%len(colors)])

        plt.title(f"Number of messages over time with {chat_name}")
        plt.xlabel("date (year-month)")
        plt.ylabel("number of messages")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def pie_chart_for_word_frequency(word_dict: Dict[str, int],
                                     word_limit_in_pie: int,
                                     total: int = None,
                                     title: str = "",
                                     x_axis_title: str = "",
                                     y_axis_title: str = ""):
        if total is None:
            total = 0
            for word in word_dict: total += word_dict[word]

        i = 0
        labels = []
        sizes = []
        in_pie = 0
        for word in word_dict:
            if i > word_limit_in_pie: break
            sizes.append(100 * word_dict[word] / total)
            l = word + f" ({word_dict[word]} mention"
            if word_dict[word] > 1: l+="s"
            l+=")"
            labels.append(l)
            in_pie += 100 * word_dict[word] / total
            i += 1
        if 100 - in_pie > 0.01:
            labels.append("other")
            sizes.append(100 - in_pie)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(title)
        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)
        plt.show()
    @staticmethod
    def visualize_unique_words(path: str, chat_name: str, word_limit_in_pie: int = 10):
        """
        Vizualizes word count for  given chat
        :param path: path to root
        :param chat_name: name of chat
        :param word_limit_in_pie: number of top used words to go into pie. for instance, word_limit_in_pie = 10 would mean
        the pie would only include the top 10 most used words in chat
        :return: None
        """
        words = InstagramDataAnalyzer.get_word_distribution(path, chat_name)
        total = 0
        a = {}
        for word, v in sorted(words.items(), key=lambda item: item[1], reverse = True):
            a[word] = v
            total += v
        InstagramDataVisualizer.pie_chart_for_word_frequency(a,
                                                             word_limit_in_pie,
                                                             total,
                                                             title = f"Word Usage in {chat_name}")


    @staticmethod
    def visualize_mention_number_in_chat(path: str, chat_name: str):
        """
        Visualizes how many times each person is mentioned in a chat
        :param path: path to root
        :param chat_name: name of chat
        :return: None
        """
        words = InstagramDataAnalyzer.get_word_distribution(path, chat_name)
        mentions = {}
        for word in words:
            if "@" == word[0]:
                mentions[word] =  words[word]
        sorted_mentions = {k: v for k, v in sorted(mentions.items(), key=lambda item: item[1], reverse = True)}

        InstagramDataVisualizer.pie_chart_for_word_frequency(sorted_mentions,
                                                             len(sorted_mentions),
                                                             title = f"Number of mentions with {chat_name}")




if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    # print(InstagramDataAnalyzer.list_chats(path_to_data))
    # InstagramDataVisualizer.visualize_logins(path_to_data)
    InstagramDataVisualizer.visualize_mention_number_in_chat(path_to_data, "thesimpsons_457uupaoka")