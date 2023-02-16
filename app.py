from flask import Flask, render_template, request, url_for
import pandas as pd
import time
import scheduler
import threading
from exchanges import exchange
# from dashboard_1 import update_matrix, poll_matrix
# import warnings
# warnings.filterwarnings("ignore", message="The frame.append method is deprecated")


app = Flask(__name__)

exch = exchange()
dataframe = exch.combine_dataframes()

@app.route("/")
def dashboard1():
    print( url_for('dashboard1'))
    symbols = dataframe['symbol'].unique().tolist()
    return render_template('dashboard1.html', symbols=symbols)


@app.route("/dashboard2")
def dashboard2():
    print( url_for('dashboard2'))
    return render_template('dashboard2.html')

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



if __name__ == '__main__':
    app.run(debug=True)
