import numpy as np
import pandas as pd


def format_training_messages(user_id, messages):
    prev_messages = []
    dataframe_index = 0
    data = [["id", "timestamp", "author_id", "content"]]
    i = 0
    while i < len(messages):
        ms = []
        author = messages[i].author_id
        while i < len(messages) and messages[i].author_id == author:
            ms.append(messages[i])
            i += 1
        if author != user_id:
            prev_messages = ms

        else:
            #     add all previous messages, and then add this message to the dataframe.
            for message in prev_messages + ms:
                data.append([message.message_id, message.timestamp, message.author_id, message.content])
                dataframe_index += 1
        if i == 0:
            continue
        # print(i / len(messages))
        # print(m.channel_id, m.timestamp)
    df = pd.DataFrame(data)
    print(df)
    return df
