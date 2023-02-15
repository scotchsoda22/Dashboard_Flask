from flask import Flask, render_template, request, url_for
import pandas as pd
import time
import scheduler
import threading
from exchanges import exchange
from dashboard_1 import update_matrix, poll_matrix
import warnings
warnings.filterwarnings("ignore", message="The frame.append method is deprecated")


app = Flask(__name__)

exch = exchange()
dataframe = exch.combine_dataframes()

@app.route("/")
def index():
    print( url_for('index'))
    symbols = dataframe['symbol'].unique().tolist()
    return render_template('index.html', symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)
