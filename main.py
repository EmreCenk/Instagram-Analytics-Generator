from typing import *
from src.Handling_Data import utils
from time import time
from src.Handling_Data.Data_Viz_Utils import UtilsForDataViz, BarGraphVisualizer, DataGenerator
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from collections import defaultdict



# TODO: how many people have you talked to? How many of them did you send the first dm?
# TODO: ONE SIDEDNESS GRAPH OVER TIME (PLOT RATIO OF SENT/RECEIVED OVER TIME, WITH DOTTED RED LINE STRAIGHT AT RATIO 1)

if __name__ == '__main__':
    # main()
    # exit()

    num_time_steps = 100
    num_categories = 10
    data_generator = DataGenerator(num_categories, num_time_steps)

    # Create a Visualizer and set it up
    visualizer = BarGraphVisualizer(data_generator.fluctuating_data, [0 for i in range(num_time_steps)], data_generator.category_names)
    visualizer.setup_plot()  # Set up the initial plot
    visualizer.setup_slider()  # Set up the slider for time control
    visualizer.setup_play_button()  # Set up the play button to start/stop animation
    visualizer.create_animation()  # Create the animation object

    # Show the plot with the interactive elements
    visualizer.show()

    interval = 2
    start_time = time()
    everything = []
    path = ""
   
    
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