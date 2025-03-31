import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

# Class to handle data generation and modifications
class DataGenerator:
    def __init__(self, num_categories, num_time_steps):
        """
        Initialize the DataGenerator with the number of categories and time steps.
        This class handles data generation and modification for the visualization.
        
        Parameters:
        - num_categories (int): The number of categories (bars) to visualize.
        - num_time_steps (int): The number of time steps for the animation.
        """
        self.num_categories = num_categories
        self.num_time_steps = num_time_steps
        self.fluctuating_data = np.zeros((num_time_steps, num_categories))  # Data container
        self.category_names = [f'Category {i}' for i in range(1, num_categories + 1)]  # Default names

        data = np.linspace(0, 1, self.num_time_steps)  # Linear base for all categories
        for i in range(self.num_categories):
            growth_rate = np.random.uniform(0.01, 0.05)  # Random growth rates for each category
            fluctuation = np.sin(np.linspace(0, 10 * np.pi, self.num_time_steps))  # Sine-wave fluctuations
            self.fluctuating_data[:, i] = np.clip(data * growth_rate * (i + 1) + 0.2 * fluctuation, 0, 1)

        self.fluctuating_data[:, 0] = np.linspace(1, 0, self.num_time_steps)  # Decrease linearly

    def set_custom_data(self, custom_data):
        """
        Allows you to set your own dataset for visualization. The data should be in a shape of [time_steps, num_categories].
        
        Parameters:
        - custom_data (ndarray): A 2D array of shape [num_time_steps, num_categories].
        """
        self.fluctuating_data = custom_data

# Class to handle plotting and animation of the bar graph
class BarGraphVisualizer:
    def __init__(self, data_generator):
        """
        Initializes the visualizer with a DataGenerator instance.
        
        Parameters:
        - data_generator (DataGenerator): The DataGenerator object that contains the data to visualize.
        """
        self.data_generator = data_generator  # Stores the DataGenerator instance
        self.num_categories = data_generator.num_categories
        self.num_time_steps = data_generator.num_time_steps
        self.category_names = data_generator.category_names

        # Create a figure and axis for the plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.bars = None  # Placeholder for bar objects
        self.slider = None  # Placeholder for the slider
        self.play_button = None  # Placeholder for the play button
        self.ani = None  # Placeholder for the animation object
        self.is_playing = False  # State of the animation (whether it's playing or paused)
        self.frame = 0  # Current frame (time step)

    def setup_plot(self):
        """
        Sets up the initial plot, including bar heights and colors.
        """
        # Generate a unique color map for each category
        colors = plt.cm.get_cmap('tab10', self.num_categories)
        # Create bars for the initial time step (all bars at time step 0)
        self.bars = self.ax.bar(range(self.num_categories), self.data_generator.fluctuating_data[0], 
                                color=colors(range(self.num_categories)))
        # Set consistent Y-axis limits for all frames
        self.ax.set_ylim(0, 1)  
        self.ax.set_xlabel('Categories')
        self.ax.set_ylabel('Values')
        self.ax.set_xticks(range(self.num_categories))
        self.ax.set_xticklabels(self.category_names)

    def setup_slider(self):
        """
        Sets up the slider widget to control the current time step with more fine-grained control.
        """
        ax_slider = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        
        # Set valstep to a smaller number to allow more granular control (like 0.1 or even smaller)
        self.slider = Slider(ax_slider, 'Time', 0, self.num_time_steps - 1, valinit=0, valstep=0.1)
        self.slider.on_changed(self.update)  # Attach the update function to the slider


    def setup_play_button(self):
        """
        Sets up the play button to control the animation.
        """
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
        print("slider val:", self.slider.val)
        sorted_indices = np.argsort(self.data_generator.fluctuating_data[self.frame])[::-1]  # Sort in descending order

        # Update the bar heights, reorder the colors, and set category names
        colors = plt.cm.get_cmap('tab10', self.num_categories)
        for i, bar in enumerate(self.bars):
            bar.set_height(self.data_generator.fluctuating_data[self.frame, sorted_indices[i]])
            bar.set_color(colors(sorted_indices[i]))  # Reassign color based on the sorted index
        self.ax.set_xticklabels([self.category_names[i] for i in sorted_indices])  # Update category names
        self.fig.canvas.draw_idle()  # Redraw the figure to reflect changes

    def play(self, event):
        """
        Toggles the play/pause state of the animation.
        
        Parameters:
        - event: The event triggered by clicking the play button.
        """
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.ani.event_source.start()  # Start the animation if it's not playing
        else:
            self.ani.event_source.stop()  # Stop the animation if it's playing

    def animate(self, i):
        """
        Updates the animation and slider on each frame.

        Parameters:
        - i: The current frame index.
        """
        if self.is_playing:
            self.slider.set_val(i)  # Update slider value based on the current frame
            self.update(i)  # Update the plot for the current frame

    def create_animation(self):
        """
        Creates the animation object that updates the plot over time.
        """
        self.ani = FuncAnimation(self.fig, self.animate, frames=range(self.num_time_steps), 
                                 interval=100, repeat=False)

    def show(self):
        """
        Displays the plot with the interactive elements (slider, play button, etc.).
        """
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

if __name__ == '__main__':
    main()
    # exit()

    # from src.Handling_Data import utils
    # from time import time
    # from datetime import datetime
    # from src.Handling_Data.Data_Viz_Utils import UtilsForDataViz
    # from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
    # from dateutil import parser
    
    # interval = 1
    # start_time = time()
    # everything = []
    # total = 0
    # path = ""

    # time_string = UtilsForDataViz.get_time_string(interval)
    # every_message_ever = []
    # chats = InstagramDataRetreiver.list_chats(path)
    # for message, convo_name in utils.loop_through_every_message(path):
    #     # message_date = message["timestamp_ms"]
    #     # message_date = datetime.fromtimestamp(int(message_date / 1000))
    #     # message_date = parser.parse(message_date.strftime(time_string))
    #     every_message_ever.append((message, convo_name))
    #     if "content" not in message: continue # message includes image
    #     total += 1
    #     LIM=40000
    #     # LIM=100
    #     if total == LIM: break
    # # sorted_messages =     
    # print(f"took: {time()-start_time} seconds")
    # print(len(chats))

    
    # print("Hi")
    # main()
    # from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
    # followers = [f["string_list_data"][0]["value"] for f in InstagramDataRetreiver.get_followers(PATH)]
    # following = [f["string_list_data"][0]["value"] for f in InstagramDataRetreiver.get_following(PATH)]
    
    # traitors = []
    # for f in following:
    #     if f not in followers:
    #         traitors.append(f)
    #         print(f"https://instagram.com/{f}")
    # print(len(traitors))