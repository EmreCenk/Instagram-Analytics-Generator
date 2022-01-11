from Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
from datetime import datetime

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
        plt.legend()
        plt.grid()
        plt.show()

    @staticmethod
    def vizualize_message_length_over_time(path: str, chat_name: str):
        to_plot = InstagramDataAnalyzer.get_message_length_over_time(path, chat_name)
        for username in to_plot:
            asdf = username
        xs, ys = to_plot[asdf][1], to_plot[asdf][0]
        print(xs)
        print(ys)
        xs.reverse()
        ys.reverse()
        plt.plot(xs, ys, label="login number")
        plt.xlabel("date (year-month)")
        plt.ylabel("number of logins")
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    # InstagramDataVisualizer.visualize_logins(path_to_data)
    InstagramDataVisualizer.vizualize_message_length_over_time(path_to_data, "")