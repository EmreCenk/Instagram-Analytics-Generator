from Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
import numpy as np
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
        plt.plot(xs, ys, label="login number", )
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()


    path_to_data = os.environ["path_to_instagram_export_download"]
    InstagramDataVisualizer.visualize_logins(path_to_data)