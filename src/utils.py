from src.Retreiving_Data import InstagramDataRetreiver
from typing import Dict
def get_time_string(interval: int = 3) -> str:
    """
    Gets a time string in the format of "%Y-%m-%d ..."
    :param interval: an integer between 0 and 3 inclusive that specifies what how detailed the time string will be
    The following is the meaning for interval values:
    0 -> year
    1 -> month
    2 -> daily
    3 -> hour
    4 -> Minute
    return: string to parse time
    """
    if interval < 0 or interval > 4:
        raise ValueError(f"'interval' argument must be one of 0, 1, 2, 3, 4."
                         f"\nThe interval meanings are as follows:"
                         "\n0 -> yearly intervals\n1 -> monthly intervals\n2 -> daily intervals\n3 -> hourly interval\n4 -> Minute intervals (may misrepresent data since a long message will create extreme spikes)"
                         f"\n\n{interval} is not a valid interval")
    times = ["%Y", "%m", "%d", "%H"]
    time_string = ""
    for i in range(min(len(times), interval + 1)): time_string += times[i] + "-"
    time_string = time_string[:-1]
    if interval == 4: time_string += ":%M"
    return time_string


def loop_through_every_message(path: str) -> Dict:
    """
    counts number of active chats per day
    :param path: path to root folder
    :return:
    """
    chats = InstagramDataRetreiver.list_chats(path)
    for conversation_name in chats:
        for message in InstagramDataRetreiver.get_messages(path, conversation_name):
            yield message