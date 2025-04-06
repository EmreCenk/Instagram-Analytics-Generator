import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from typing import *
from src.Handling_Data import utils
from time import time
from datetime import datetime, timedelta
from src.Handling_Data.Data_Viz_Utils import UtilsForDataViz
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from dateutil import parser
from collections import defaultdict

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
            self.slider.set_val(i)  # Update slider value based on the current frame
            self.update(i)  # Update the plot for the current frame

    def create_animation(self):
        self.ani = FuncAnimation(self.fig, self.animate, frames=range(self.num_time_steps), 
                                 interval=100, repeat=False)

    def show(self):
        plt.show()

def main():
    """
    Main function that sets up and runs the visualization with sample data.
    This is where you can modify or replace data generation and visualization.
    """
    # Create a DataGenerator with your own parameters (number of categories and time steps)
    num_categories = 10
    num_time_steps = 100
    data_generator = DataGenerator(num_categories, num_time_steps)

    # Create a Visualizer and set it up
    visualizer = BarGraphVisualizer(data_generator)
    visualizer.setup_plot()  # Set up the initial plot
    visualizer.setup_slider()  # Set up the slider for time control
    visualizer.setup_play_button()  # Set up the play button to start/stop animation
    visualizer.create_animation()  # Create the animation object

    # Show the plot with the interactive elements
    visualizer.show()
# TODO: how many people have you talked to? How many of them did you send the first dm?
# TODO: ONE SIDEDNESS GRAPH OVER TIME (PLOT RATIO OF SENT/RECEIVED OVER TIME, WITH DOTTED RED LINE STRAIGHT AT RATIO 1)

if __name__ == '__main__':
    # main()
    # exit()


    
    interval = 2
    start_time = time()
    everything = []
    path = ""
                
    ignore_groupchats = True
    time_string = UtilsForDataViz.get_time_string(interval)
    chats = InstagramDataRetreiver.list_chats(path)
    # chats = chats[200:230]
    date_to_msg = defaultdict(list)
    earliest_msg = datetime.max
    latest_msg = datetime.min
    members_of_chat = defaultdict(set)
    
    # for message, convo_name in utils.loop_through_every_message(path):
    for convo_name in chats:
        for message in InstagramDataRetreiver.get_messages(path, convo_name):
            members_of_chat[convo_name].add(message["sender_name"])
            message_date = datetime.fromtimestamp(message["timestamp_ms"] / 1000)
            message_date_str = message_date.strftime(time_string)
            date_to_msg[message_date_str].append((convo_name, message))
            earliest_msg = min(earliest_msg, message_date)
            latest_msg = max(latest_msg, message_date)

    blacklist = []
    if ignore_groupchats:
        for convo_name in chats:
            if len(members_of_chat[convo_name]) <= 2: continue # back to standard definition we are (it turns out even with 4 people some gc's get very convoluted)
            blacklist.append(convo_name)
    print(f"took: {time()-start_time} seconds")
    
    data_points = []
    delta_time = utils.get_timedelta_from_time_string(time_string)
    current_date = earliest_msg
    dates = []
    while current_date < latest_msg:
        dates.append(current_date)        
        current_date += delta_time

    situation_current = [0 for i in range(len(chats))]
    get_username_index = {chats[i]: i for i in range(len(chats))}
    data_points = []
    for i in range(len(dates)):
        d = dates[i]
        cache = d.strftime(time_string)
        for convo_name, message in date_to_msg[cache]:
            if convo_name in blacklist: continue
            if "content" not in message: continue
            situation_current[get_username_index[convo_name]] += len(message["content"])  

        data_points.append([k for k in situation_current])
    num_categories = len(chats)
    num_time_steps = len(dates)
    # data_generator = DataGenerator(num_categories, num_time_steps, data_points, [utils.fix_username(c) for c in chats])

    # Create a Visualizer and set it up
    visualizer = BarGraphVisualizer(data_points, dates, [utils.fix_username(c) for c in chats],
                                    format_date_func = lambda d: d.strftime(time_string))
    visualizer.setup_plot()  # Set up the initial plot
    visualizer.setup_slider()  # Set up the slider for time control
    visualizer.setup_play_button()  # Set up the play button to start/stop animation
    visualizer.create_animation()  # Create the animation object

    # Show the plot with the interactive elements
    visualizer.show()
    
    # for i in range(len(dates)):
        # nums_on_day = []
        # for j in range(len(chats)):
            # nums_on_day
        # data_points.append([])
        





    # from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
    # followers = [f["string_list_data"][0]["value"] for f in InstagramDataRetreiver.get_followers(PATH)]
    # following = [f["string_list_data"][0]["value"] for f in InstagramDataRetreiver.get_following(PATH)]
    
    # traitors = []
    # for f in following:
    #     if f not in followers:
    #         traitors.append(f)
    #         print(f"https://instagram.com/{f}")
    # print(len(traitors))