from typing import *
from src.Handling_Data import utils
from time import time
from datetime import datetime, timedelta
from src.Handling_Data.Data_Viz_Utils import UtilsForDataViz
from src.Handling_Data.Retreiving_Data import InstagramDataRetreiver
from collections import defaultdict



# TODO: how many people have you talked to? How many of them did you send the first dm?
# TODO: ONE SIDEDNESS GRAPH OVER TIME (PLOT RATIO OF SENT/RECEIVED OVER TIME, WITH DOTTED RED LINE STRAIGHT AT RATIO 1)

if __name__ == '__main__':
    # main()
    # exit()


    
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