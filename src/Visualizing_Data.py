from src.Analyzing_Data import InstagramDataAnalyzer
from src.popups import create_popup_message
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from typing import Dict
from src.Retreiving_Data import InstagramDataRetreiver
from collections import defaultdict
from src import utils

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
    def get_x_axis_label(interval: int) -> str:
        """
        Gets a corresponding x axis title according to the interval value passed into InstagramDataVisualizer.get_time_string
        :param interval:
        :return: a title specifying the date intervals
        """

        a = defaultdict(str)
        a[0] = "(Yearly Intervals)"
        a[1] = "(Monthly Intervals)"
        a[2] = "(Daily Intervals)"
        a[3] = "(Hour Intervals)"
        a[4] = "(Minute Intervals)"
        return "date \n" + a[interval]
    @staticmethod
    def get_time_string(interval: int = 3) -> str:
        """
        Wrapper function for utils.get_time_string
        Originally, the function was written under the InstagramDataVisualizer class, but was then moved to utils.
        Instead of changing every occurrence, I just converted this to a wrapper.
        """
        return utils.get_time_string(interval)
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
        time_string = InstagramDataVisualizer.get_time_string(interval)


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

        #todo: implement time strings to customize plot intervals on x axis
        colors = ['red', 'blue', 'darkkhaki', 'green', 'orange', 'purple', 'brown', 'pink', 'teal', 'maroon', 'cyan', 'magenta', 'navy', 'lime', 'olive', 'lavender', 'mauve', 'umber', 'murk', 'black', 'gray']



        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)
        for user_index, username in enumerate(to_plot):
            #note: we need to keep track of the user_index because this function changes colors dynamically using the 'colors' list
            days = {}
            timestamps, messages = to_plot[username][1], to_plot[username][0]
            for i in range(len(timestamps)):

                #converting epoch timestamp to datetime object:
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

    @staticmethod
    def visualize_follower_gain_over_time(path: str, interval: int = 1):
        """
        Visualizes follower gain over time
        :param path: path to root
        :param interval: an integer between 0 and 3 inclusive that specifies what interval the messages will be plotted in.
        See InstagramDataRetreiver.get_time_string for more information
        interval values:
        0 -> yearly intervals
        1 -> monthly intervals
        2 -> daily intervals
        3 -> hourly interval
        4 -> Minute intervals (may misrepresent data since a long message will create extreme spikes)
        :return: None

        """
        time_string = InstagramDataVisualizer.get_time_string(interval)
        followers = InstagramDataRetreiver.get_followers(path)

        followers = sorted(followers, key = lambda person: person["string_list_data"][0]["timestamp"])

        categorized_by_date = {}
        for person in followers:
            # timestamps[i] = datetime.fromtimestamp(int(timestamps[i]) / 1000)
            # cache = parser.parse(timestamps[i].strftime(time_string))
            follow_date = datetime.fromtimestamp(int(person["string_list_data"][0]["timestamp"]))
            follow_date = parser.parse(follow_date.strftime(time_string))
            if follow_date in categorized_by_date: categorized_by_date[follow_date].append(person)
            else: categorized_by_date[follow_date] = [person]


        #plotting data:
        xs, ys = [], []
        names = []
        fig, ax = plt.subplots()

        for date in categorized_by_date:
            xs.append(date)
            ys.append(len(categorized_by_date[date]))
            names.append("")
            for person in categorized_by_date[date]:

                names[-1] += person["string_list_data"][0]["value"] + "\n"

        ax.plot_date(xs, ys, picker=5)
        plt.plot(xs, ys)




        def on_pick(event):
            line = event.artist
            xdata, ydata = line.get_data()
            ind = event.ind
            how_many = ydata[ind]
            dates = xdata[ind]

            for i in range(len(how_many)):
                current_follower_num = how_many[i]
                current_followers = ""

                for person in categorized_by_date[dates[i]]:
                    # print(person)
                    date_followed = datetime.fromtimestamp(person['string_list_data'][0]['timestamp'])
                    cache = parser.parse(date_followed.strftime("%m/%d/%Y, %H:%M:%S"))

                    current_followers += f"{person['string_list_data'][0]['value']}\t\t\t\t[{date_followed}]\n"
                popup_title = f"{current_follower_num} follower"
                if current_follower_num > 1: popup_title += "s"
                popup_title += f" gained on\n{dates[i]}:"
                create_popup_message(
                    message = current_followers,
                    title_in_popup = popup_title,
                    window_title = "Follower information")
                break #todo: implement threads to create multiple windows when data points coincide

        fig.canvas.mpl_connect('pick_event', on_pick)

        plt.title(f"Followers gained")
        plt.xlabel(InstagramDataVisualizer.get_x_axis_label(interval))
        plt.ylabel("follower number")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_messages_sent_and_received_per_day_over_time(path: str,
                                                               name_of_owner: str,
                                                               interval: int = 1,
                                                               plot_sent: bool = True,
                                                               plot_received: bool = True):
        """
        Visualizes the number of messages sent and received per day over time.
        :param path: path to root
        :param name_of_owner: Instagram name of owner. The messages sent by this name will be plotted with a different name
        :param interval: an integer between 0 and 3 inclusive that specifies what interval the messages will be plotted in.
        See InstagramDataRetreiver.get_time_string for more information
        interval values:
        0 -> yearly intervals
        1 -> monthly intervals
        2 -> daily intervals
        3 -> hourly interval
        4 -> Minute intervals (may misrepresent data since a long message will create extreme spikes)
        :param plot_sent: if true, the number of messages sent is plotted.
        :param plot_received: if true, the number of messages received is plotted.
        :return: None
        """
        received, sent = InstagramDataAnalyzer.count_active_chats_per_day(path, name_of_owner)
        sorted_received = sorted(received, key = lambda x: x)
        sorted_sent = sorted(sent, key = lambda x: x)

        xreceived, yreceived = [], []
        xsent, ysent = [], []

        if plot_received:
            for day in sorted_received:
                xreceived.append(day)
                yreceived.append(received[day])

        if plot_sent:
            for day in sorted_sent:
                xsent.append(day)
                ysent.append(sent[day])


        plt.plot(xsent, ysent, label=f"number of messages sent by {name_of_owner}")
        plt.plot(xreceived, yreceived, label=f"number of messages received by {name_of_owner}")

        plt.title(f"Number of Messages Received and Sent")
        plt.xlabel(InstagramDataVisualizer.get_x_axis_label(interval))
        plt.ylabel("number of messages")
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    # print(InstagramDataAnalyzer.list_chats(path_to_data))
    # InstagramDataVisualizer.visualize_logins(path_to_data)
    # InstagramDataVisualizer.visualize_message_length_over_time(path_to_data, "thesimpsons_457uupaoka")
    # InstagramDataVisualizer.visualize_follower_gain_over_time(path_to_data,
    #                                                           interval = 2)
    InstagramDataVisualizer.visualize_messages_sent_and_received_per_day_over_time(path_to_data,
                                                                                   "Emre Cenk",
                                                                                   interval = 3,
                                                                                   plot_sent=False,)