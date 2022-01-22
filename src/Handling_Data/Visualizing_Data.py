import numpy as np
from src.Handling_Data.Analyzing_Data import InstagramDataAnalyzer
from src.GUI.popups import create_popup_message
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from src.Handling_Data import utils
from src.Handling_Data.Data_Viz_Utils import UtilsForDataViz

class InstagramDataVisualizer():

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
        plt.title(f"Number of logins over time")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_message_length_over_time_in_chat(path: str,
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
        time_string = UtilsForDataViz.get_time_string(interval)


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
        plt.xlabel(UtilsForDataViz.get_x_axis_label(interval))
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
        UtilsForDataViz.pie_chart_for_word_frequency(a,
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

        UtilsForDataViz.pie_chart_for_word_frequency(sorted_mentions,
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
        time_string = UtilsForDataViz.get_time_string(interval)
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
                    date_followed = datetime.fromtimestamp(person['string_list_data'][0]['timestamp'])

                    current_followers += f"{person['string_list_data'][0]['value']}\t\t\t\t[{date_followed}]\n"
                popup_title = f"{current_follower_num} follower"
                if current_follower_num > 1: popup_title += "s"
                popup_title += f" gained in the {['year', 'month', 'day', 'hour', 'minute'][interval]} of {dates[i].strftime(time_string)}:"
                create_popup_message(
                    message = current_followers,
                    title_in_popup = popup_title,
                    window_title = "Follower information")
                break #todo: implement threads to create multiple windows when data points coincide

        fig.canvas.mpl_connect('pick_event', on_pick)

        plt.title(f"Followers Gained Over Time\nNote: Please click on the data points to see a list of followers")
        plt.xlabel(UtilsForDataViz.get_x_axis_label(interval))
        plt.ylabel("follower number")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_total_messages_sent_and_received_over_time_counting_every_chat(path: str,
                                                                                 interval: int = 1,
                                                                                 plot_sent: bool = True,
                                                                                 plot_received: bool = True):
        """
        The
        Visualizes the number of messages sent and received per day over time.
        :param path: path to root
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
        name_of_owner = InstagramDataRetreiver.get_name(path)
        received, sent = InstagramDataAnalyzer.count_number_of_messages_per_day(path, interval)
        sorted_received = sorted(received, key = lambda x: x)
        sorted_sent = sorted(sent, key = lambda x: x)

        yreceived = np.zeros((len(received), 1))
        ysent = np.zeros((len(sent), 1))

        if plot_received:
            for i in range(len(sorted_received)):
                yreceived[i] = received[sorted_received[i]]

        if plot_sent:
            for i in range(len(sorted_sent)):
                ysent[i] = sent[sorted_sent[i]]


        plt.plot(sorted_sent, ysent, label=f"number of messages sent by {name_of_owner}")
        plt.plot(sorted_received, yreceived, label=f"number of messages received by {name_of_owner}")

        plt.title(f"Number of Messages Received and Sent in Total (counting every chat)")
        plt.xlabel(UtilsForDataViz.get_x_axis_label(interval))
        plt.ylabel("number of messages")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def visualize_active_chats(path: str,
                               interval: int = 1
                               ):

        """
        Visualizes the number of active chats over time
        Very similar structure to InstagramDataVisualizer.visualize_follower_gain_over_time
        todo: check if it's worth generalizing/refactoring InstagramDataVisualizer.visualize_follower_gain_over_time and InstagramDataVisualizer.visualize_active_chats into a single function.

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
        time_string = utils.get_time_string(interval) #required to properly put titles in the annotations
        categorized_by_date = InstagramDataAnalyzer.count_number_of_active_dms(path, interval)
        sorted_dates = sorted(categorized_by_date)


        #plotting data:
        xs, ys = [], []
        names = []
        fig, ax = plt.subplots()

        for date in sorted_dates:
            xs.append(date)
            ys.append(len(categorized_by_date[date]))
            names.append("")
            for person in categorized_by_date[date]:
                names[-1] += person + "\n"

        ax.plot_date(xs, ys, picker=5)
        plt.plot(xs, ys)



        # the following is taken from InstagramDataVisualizer.visualize_follower_gain_over_time
        # (with a few adjustments)
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
                    current_followers += f"{utils.fix_username(person)}\n"

                popup_title = f"{current_follower_num} chat"
                if current_follower_num > 1: popup_title += "s"
                popup_title += f" active in the {['year', 'month', 'day', 'hour', 'minute'][interval]} of {dates[i].strftime(time_string)}:"

                create_popup_message(
                    message = current_followers,
                    title_in_popup = popup_title,
                    window_title = f"Chats That Were Active in the {['year', 'month', 'day', 'hour', 'minute'][interval]} of {dates[i].strftime(time_string)}")
                break #todo: implement threads to create multiple windows when data points coincide

        fig.canvas.mpl_connect('pick_event', on_pick)

        plt.title(f"Number of Active Chats Over Time")
        plt.xlabel(UtilsForDataViz.get_x_axis_label(interval))
        plt.ylabel("number of active chats")
        plt.legend()
        plt.grid()
        plt.show()


    @staticmethod
    def visualize_most_active_year(path: str, bar_graph: bool = True):
        """
        Creates a bar graph to visualize most active day for messages
        :param path: path to root
        :param bar_graph: True gives a bar graph, False gives a pie chart
        :return: None
        """
        UtilsForDataViz.visualize_message_activity_in_cycle(path,
                                                                    graph_type = bar_graph,
                                                                    titles = ["Characters SENT in Each Year",
                                                                    "Number of SENT Message in Each Year",
                                                                    "Characters RECEIVED in Each Year",
                                                                    "Number of RECEIVED Message in Each Year",
                                                                    ],
                                                                    xlabels = ["Year"] * 4,
                                                                    ylabels = ["Number of Characters", "Number of Messages"]*2,
                                                                    interval = 0,
                                                                    )

    @staticmethod
    def visualize_most_active_month(path: str, bar_graph: bool = True):
        """
        Creates a bar graph to visualize most active day for messages
        :param path: path to root
        :param bar_graph: True gives a bar graph, False gives a pie chart
        :return: None
        """
        UtilsForDataViz.visualize_message_activity_in_cycle(path,
                                                                    graph_type = bar_graph,
                                                                    titles = ["Characters SENT For Each Month",
                                                                    "Number of SENT Message For Each Month",
                                                                    "Characters RECEIVED For Each Month",
                                                                    "Number of RECEIVED For Each Month",
                                                                    ],
                                                                    xlabels = ["Month"] * 4,
                                                                    ylabels = ["Number of Characters", "Number of Messages"]*2,
                                                                    interval = 1)
    @staticmethod
    def visualize_most_active_day(path: str, bar_graph: bool = True):
        """
        Creates a bar graph to visualize most active day for messages
        :param path: path to root
        :param bar_graph: True gives a bar graph, False gives a pie chart
        :return: None
        """
        UtilsForDataViz.visualize_message_activity_in_cycle(path,
                                                                    graph_type = bar_graph,
                                                                    titles = ["Characters SENT On Each Day of Week",
                                                                    "Number of SENT Message On Each Day of Week",
                                                                    "Characters RECEIVED On Each Day of Week",
                                                                    "Number of RECEIVED Message On Each Day of Week",
                                                                    ],
                                                                    xlabels = ["Days of Week"] * 4,
                                                                    ylabels = ["Number of Characters", "Number of Messages"]*2,
                                                                    interval = 2,
                                                                    )

    @staticmethod
    def visualize_most_active_hours(path: str, bar_graph: bool = True):
        """
        Creates a bar graph to visualize most active day for messages
        :param path: path to root
        :param bar_graph: True gives a bar graph, False gives a pie chart
        :return: None
        """
        UtilsForDataViz.visualize_message_activity_in_cycle(path,
                                                                    graph_type=bar_graph,
                                                                    titles=["Characters SENT On Each Hour Of Day",
                                                                            "Number of SENT Message On Each Hour Of Day",
                                                                            "Characters RECEIVED On Each Hour Of Day",
                                                                            "Number of RECEIVED Message On Each Hour Of Day",
                                                                            ],
                                                                    xlabels=["Hour of Day"] * 4,
                                                                    ylabels=["Number of Characters",
                                                                             "Number of Messages"] * 2,
                                                                    interval=3,
                                                                    )

    @staticmethod
    def visualize_friendship_ranking_histogram_by_number_of_messages_sent(path: str):
        """
        Creates a histogram by looking at how many messages each friend has sent
        :param path: path to root
        :return:
        """
        rankings, person_to_message_number = InstagramDataAnalyzer.friendship_rankings_by_messages_sent_to_user(path, method = 0)
        data = [person_to_message_number[person] for person in person_to_message_number]
        plt.hist(data, bins = 10)
        plt.title("Distribution of how many messages were received for each chat")
        plt.ylabel("Number of chats")
        plt.xlabel("How many messages were sent to user")
        plt.show()

    @staticmethod
    def friendship_rankings_by_total_length_of_messages_they_sent_you(path: str, how_many_to_display: int = 20):
        sorted, mapped = InstagramDataAnalyzer.friendship_rankings_by_messages_sent_to_user(path, 1)
        for i in range(10):
            print(sorted[i], mapped[sorted[i]])
        fig, ax = plt.subplots()
        how_many = min(len(sorted), how_many_to_display)
        total_sent = [mapped[sorted[i]] for i in range(how_many)]
        names = [str(i+1) + ") "+ utils.fix_username(sorted[i]) for i in range(how_many)]
        ax.barh(names, total_sent)
        ax.invert_yaxis()
        plt.yticks([i for i in range(how_many)])
        plt.xlabel("Number of characters sent")
        plt.ylabel("Name of Chat")
        plt.title(f"Chats Ranked by How Many Characters They Have Sent You\nNote: Currently displaying top {how_many} chats out of {len(sorted)} people. Tweak settings if you want to see more or less people graphed.")
        plt.show()
if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    plt.style.use('dark_background')

    path_to_data = os.environ["path_to_instagram_export_download"]
    InstagramDataVisualizer.friendship_rankings_by_total_length_of_messages_they_sent_you(path_to_data)
    # InstagramDataVisualizer.visualize_friendship_ranking_histogram_by_number_of_messages_sent(path_to_data)
    # InstagramDataVisualizer.visualize_message_length_over_time_in_chat(path_to_data, "", interval = 4)
    # InstagramDataVisualizer.visualize_messages_sent_and_received_over_time(path_to_data, "Emre Cenk")
    #cache test:
    # InstagramDataAnalyzer.count_msgs(path_to_data, 0, "Emre Cenk")
    # InstagramDataAnalyzer.count_msgs(path_to_data, 1, "Emre Cenk")
    # InstagramDataAnalyzer.count_msgs(path_to_data, 2, "Emre Cenk")
    # InstagramDataAnalyzer.count_msgs(path_to_data, 3, "Emre Cenk")
    #
    # InstagramDataVisualizer.visualize_most_active_year(path_to_data, "Emre Cenk", bar_graph=True )
    # InstagramDataVisualizer.visualize_most_active_month(path_to_data, "Emre Cenk", bar_graph=True )
    # InstagramDataVisualizer.visualize_most_active_day(path_to_data, "Emre Cenk", bar_graph=True )
    # InstagramDataVisualizer.visualize_most_active_hours(path_to_data, "Emre Cenk", bar_graph=True )

    # print(InstagramDataAnalyzer.list_chats(path_to_data))
    # InstagramDataVisualizer.visualize_logins(path_to_data)
    # InstagramDataVisualizer.visualize_message_length_over_time(path_to_data, "thesimpsons_457uupaoka")
    # InstagramDataVisualizer.visualize_follower_gain_over_time(path_to_data,
    #                                                           interval = 2)
    # InstagramDataVisualizer.visualize_messages_sent_and_received_over_time(path_to_data,
    #                                                                                "Emre Cenk",
    #                                                                                interval = 1,
    #                                                                                )
    # InstagramDataVisualizer.visualize_active_chats(path_to_data,
    #                                                interval = 1)

    # InstagramDataVisualizer.visualize_follower_gain_over_time(path_to_data,
    #                                                interval = 0)