from src.Handling_Data.Analyzing_Data import InstagramDataAnalyzer
import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, List, Callable
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from collections import defaultdict
from src.Handling_Data import utils
from src.GUI.popups import create_popup_message
from datetime import datetime
from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from typing import *

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

        for i in range(len(sizes)):
            print(f"{i}) {sizes[i]} -- {labels[i]}")
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(title)
        plt.xlabel(x_axis_title)
        plt.ylabel(y_axis_title)
        plt.show(block=False)

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
        plt.show(block=False)

    @staticmethod
    def visualize_gains(path: str,
                        func_to_get_data: Callable,
                        interval: int = 1,
                        what_gained: str = "followers",
                        ):
        """
        Visualizes follower or following gain over time
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
        followers = func_to_get_data(path)

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
        prev_total = 0
        for date in categorized_by_date:
            xs.append(date)
            prev_total += len(categorized_by_date[date])
            ys.append(prev_total)
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
                if ind == 0: current_follower_num = ydata[ind]
                else: current_follower_num = ydata[ind] - ydata[ind - 1]
                current_followers = ""

                for person in categorized_by_date[dates[i]]:
                    date_followed = datetime.fromtimestamp(person['string_list_data'][0]['timestamp'])

                    current_followers += f"{person['string_list_data'][0]['value']}\t\t\t\t[{date_followed}]\n"
                popup_title = f"{current_follower_num} {what_gained}"
                if current_follower_num > 1: popup_title += "s"
                popup_title += f" in the {['year', 'month', 'day', 'hour', 'minute'][interval]} of {dates[i].strftime(time_string)}:"
                create_popup_message(
                    message = current_followers,
                    title_in_popup = popup_title,
                    window_title = f"{what_gained} information")
                break #todo: implement threads to create multiple windows when data points coincide

        fig.canvas.mpl_connect('pick_event', on_pick)

        plt.title(f"{what_gained} Increase Over Time\nNote: Please click on the data points to see a list of {what_gained} at that specific date")
        plt.xlabel(UtilsForDataViz.get_x_axis_label(interval))
        plt.ylabel(f"Number of {what_gained}")
        plt.legend()
        plt.grid()
        plt.show(block=False)



# Class to handle data generation and modifications
class DataGenerator:
    def __init__(self, num_categories, num_time_steps, data=None, names=None):
        """
        Initialize the DataGenerator with the number of categories and time steps.
        This class handles data generation and modification for the visualization.
        
        Parameters:
        - num_categories (int): The number of categories (bars) to visualize.
        - num_time_steps (int): The number of time steps for the animation.
        """

        self.fluctuating_data = np.zeros((num_time_steps, num_categories))  # Data container
        self.category_names = [f'Category {i}' for i in range(1, num_categories + 1)]  # Default names
        self.num_time_steps = num_time_steps
        self.num_categories = num_categories
        data = np.linspace(0, 1, self.num_time_steps)  # Linear base for all categories
        for i in range(self.num_categories):
            growth_rate = np.random.uniform(0.01, 0.05)  # Random growth rates for each category
            fluctuation = np.sin(np.linspace(0, 10 * np.pi, self.num_time_steps))  # Sine-wave fluctuations
            self.fluctuating_data[:, i] = np.clip(data * growth_rate * (i + 1) + 0.2 * fluctuation, 0, 1)

        self.fluctuating_data[:, 0] = np.linspace(1, 0, self.num_time_steps)  # Decrease linearly


# Class to handle plotting and animation of the bar graph
class BarGraphVisualizer:
    def __init__(self, _data: Iterable[Iterable[int]],
                      _dates: List[datetime],
                      category_labels: List[str],
                      how_many_to_display: int = 10,
                      format_date_func: Callable = lambda d: str(d),
                      ):
        """
        Creates a bar graph that races stuff over time

        Args:
            _data (Iterable[Iterable[int]]): 
                Say you have 3 countries you want to animate in a bar graph. Your data could look something like:
                [
                    [0, 0, 0]
                    [1, 0, 0]
                    [3, 2, 1]
                ]
                In this case, country 0 goes from 0->1>3
                country 1 goes through 0->0->2
                country 2 goes through 0->0->1 
                
            category_labels (List[str]): 
                Labels of the things you're plotting. Again according to the previous example, if you passed in ["Spain", "England", "Wales"]:
                "Spain" goes from 0->1>3
                "England" goes through 0->0->2
                "Wales" goes through 0->0->1 

            _dates (List[datetime]):
                If "Spain" goes through 0->1->3, and our _dates was [1/1/2000, 1/1/2001, 1/1/2002], then:
                On 1/1/2000: "Spain" was 0
                On 1/1/2001: "Spain" was 1
                On 1/1/2002: "Spain" was 3

                Basically _data[i] happened on _dates[i].
            
            how_many_to_display (int):
                If there are 200 categories, display the top "how_many_to_display"
        """
        self.data = _data 
        self.dates = _dates
        self.num_categories = len(self.data[0])
        self.num_time_steps = len(self.dates) # note: len(self.dates) == len(self.data)
        self.category_names = category_labels
        self.how_many_to_display = how_many_to_display
        self.format_date_func = format_date_func

        # Create a figure and axis for the plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.bars = None  # Placeholder for bar objects
        self.slider = None  # Placeholder for the slider
        self.play_button = None  # Placeholder for the play button
        self.ani = None  # Placeholder for the animation object
        self.is_playing = False  # State of the animation (whether it's playing or paused)
        self.frame = 0  # Current frame (time step)

    def get_colours(self):
        # return plt.cm.get_cmap('tab10', self.num_categories)
        # from matplotlib import colormaps
        # return colormaps["tab10"]
        # colours = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFBD33', '#33D4FF',
        #   '#8E44AD', '#F39C12', '#2ECC71', '#E74C3C']
        colours = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
        return colours

    def setup_plot(self):
        """
        Sets up the initial plot, including bar heights and colors.
        """
        # Generate a unique color map for each category
        colors = self.get_colours()
        # Create bars for the initial time step (all bars at time step 0)
        self.bars = self.ax.barh(range(self.how_many_to_display),
                                 [0]*self.how_many_to_display, 
                                 color=colors)
        # Set consistent Y-axis limits for all frames
        self.ax.set_ylabel('Categories')
        self.ax.set_xlabel('Values')
        self.ax.set_yticks(range(self.how_many_to_display))
        self.ax.set_yticklabels(self.category_names[:self.how_many_to_display])
        self.label = self.ax.text(0.5, 0.95, '', transform=self.ax.transAxes, ha='center', va='center')


    def setup_slider(self):
        """
        Sets up the slider widget to control the current time step with more fine-grained control.
        """
        ax_slider = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        
        # Set valstep to a smaller number to allow more granular control (like 0.1 or even smaller)
        self.slider = Slider(ax_slider, 'Time', 0, self.num_time_steps - 1, valinit=0, valstep=0.1)
        self.slider.on_changed(self.update)  # Attach the update function to the slider


    def setup_play_button(self):
        ax_button = plt.axes([0.85, 0.02, 0.1, 0.04])
        self.play_button = Button(ax_button, 'Play')
        self.play_button.on_clicked(self.play)  # Attach the play function to the button

    def update(self, val):
        """
        Updates the plot with the current time step selected by the slider.
        
        Parameters:
        - val: The new value from the slider (current time step).
        """
        self.frame = int(self.slider.val)
        # self.frame = val
        sorted_indices = np.argsort(self.data[self.frame])  # Sort in ascending order
        # Update the bar heights, reorder the colors, and set category names
        colours = self.get_colours()
        max_value = 0 
        names_y_axis = []
        for i, bar in enumerate(self.bars):
            index_of_ith_highest = sorted_indices[-(i+1)]
            value = self.data[self.frame][index_of_ith_highest]
            bar.set_width(value)
            bar.set_color(colours[index_of_ith_highest%len(colours)])  # Reassign color based on the sorted index
            names_y_axis.append(self.category_names[index_of_ith_highest])
            max_value = max(max_value, value)  # Update max_value for y-limits
        self.ax.set_xlim(0, max_value * 1.1)
        self.ax.set_yticklabels(names_y_axis)
        self.fig.canvas.draw_idle()  # Redraw the figure to reflect changes
        self.label.set_text(f"Slider Value: {self.format_date_func(self.dates[self.frame])}")    


    def play(self, event):
        """
        Toggles the play/pause state of the animation.
        """
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.ani.event_source.start()  # Start the animation if it's not playing
        else:
            self.ani.event_source.stop()  # Stop the animation if it's playing

    def animate(self, i):
        if self.is_playing:
            self.slider.set_val(self.slider.val)  # Update slider value based on the current frame
            self.update(self.slider.val)  # Update the plot for the current frame
            self.slider.val = min(len(self.data)-1, self.slider.val+1)


    def create_animation(self):
        self.ani = FuncAnimation(self.fig, self.animate, frames=range(self.num_time_steps), 
                                 interval=100, repeat=False)

    def show(self):
        plt.show()














