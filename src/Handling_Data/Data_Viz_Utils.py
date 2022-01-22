from src.Handling_Data.Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from collections import defaultdict
from src.Handling_Data import utils

class UtilsForDataViz():


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
    def visualize_message_activity_in_cycle(path: str,
                                            titles: List[str],
                                            xlabels: List[str],
                                            ylabels: List[str],
                                            graph_type: int = 0,
                                            interval: int = 0,
                                            ):

        """
        Do not call directly. Use one of the wrapper functions.
        :param path: path to root
        :param index: 0, 1, 2, 3 depending on which one you wanna visualize. See InstagramDataAnalyzer.most_active_days_of_week to see which integer corresponds to which visualization
        0 -> pie chart
        any other number -> bar graph
        :param titles:  list of titles to place in plots
        :param xlabels: list of x axis labels to place in plots
        :param ylabels: list of y axis labels to place in plots
        :param graph_type: which type of graph you want (0 means pie chart, any other number means bar graph)
        :param interval: one of 0,1,2,3
        0 -> most active year
        1 -> most active month
        2 -> most active day of week
        3 -> hour
        :return:
        """
        if not (0 <= interval <= 3): raise ValueError(f"Interval value must be between 0 and 3. {interval} is not a valid value")

        days = [
            [],
            ['', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'],
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            [],
        ][interval]
        data_func = [InstagramDataAnalyzer.most_active_years,
                     InstagramDataAnalyzer.most_active_months,
                     InstagramDataAnalyzer.most_active_days_of_week,
                     InstagramDataAnalyzer.most_active_hours,][interval]


        fig1, ax1 = plt.subplots(2, 2)

        location = ((0,0), (0,1), (1,0), (1,1))
        data = data_func(path)
        for index in range(4):
            labels, sizes = [], []
            for d in sorted(data[index]):
                if interval in {0, 3}: labels.append(d) #either a year or a ready string
                else: labels.append(days[d])
                sizes.append(data[index][d])


            if graph_type == 0:
                ax1[location[index][0],location[index][1]].pie(sizes, labels=labels, autopct='%1.1f%%',
                        shadow=False)
                ax1[location[index][0],location[index][1]].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            else:
                # print(labels, sizes)
                # print()
                # print(titles[index])
                ax1[location[index][0], location[index][1]].bar(labels, sizes)
                ax1[location[index][0], location[index][1]].get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


            ax1[location[index][0],location[index][1]].set_title(titles[index])
            ax1[location[index][0],location[index][1]].set_xlabel(xlabels[index])
            ax1[location[index][0],location[index][1]].set_ylabel(ylabels[index])
        plt.show()
