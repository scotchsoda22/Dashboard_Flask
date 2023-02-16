from flask import Flask, render_template, request, url_for
import pandas as pd
import time
import scheduler
import threading
from exchanges import exchange


def update_matrix():
    global dataframe
    while True:
        dataframe = exch.combine_dataframes()
        time.sleep(5)

# start the dataframe update process as a background task
thread = threading.Thread(target=update_matrix)
thread.start()

# a new endpoint for long polling
@app.route('/poll_matrix', methods=['GET'])
def poll_matrix():
    coin = request.args.get('coin')
    df = dataframe[dataframe['symbol'] == coin]
    exchanges = df['exchange'].unique().tolist()
    matrix = pd.DataFrame(columns=exchanges, index=exchanges)
    matrix.index.name = 'Exchange'
    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            if i != j:
                rate1 = df[df['exchange'] == exchanges[i]]['askRate'].min()
                rate2 = df[df['exchange'] == exchanges[j]]['bidRate'].max()
                diff =  "{:.2f}%".format(((abs(rate1 - rate2) / ((rate1 + rate2) / 2)) * 100))
                matrix.at[exchanges[i], exchanges[j]] = diff
    if matrix.size != 0:
        return matrix.to_json()

