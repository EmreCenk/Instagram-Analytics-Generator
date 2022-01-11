from Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser

class InstagramDataVisualizer:

    @staticmethod
    def visualize_logins(path: str):
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
    def vizualize_message_length_over_time(path: str, chat_name: str):
        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)
        for username in to_plot:


            dates, lengths = to_plot[username][1], to_plot[username][0]
            for i in range(len(dates)):
                dates[i] = datetime.fromtimestamp(int(dates[i])/1000)

            plt.plot(dates, lengths, label=username)

        plt.title(f"Message length over time in groupchat '{chat_name}'")
        plt.xlabel("date (year-month)")
        plt.ylabel("length of message")
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def vizualize_message_count_over_time(path: str, chat_name: str):
        from collections import defaultdict
        #todo: move import to top


        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)


        for username in to_plot:
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

            plt.plot(x_axis, y_axis, label=username)

        plt.title(f"Number of messages over time in {chat_name}")
        plt.xlabel("date (year-month)")
        plt.ylabel("number of messages")
        plt.legend()
        plt.grid()
        plt.show()
if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    # InstagramDataVisualizer.visualize_logins(path_to_data)
    InstagramDataVisualizer.vizualize_message_count_over_time(path_to_data, "")