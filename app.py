from flask import Flask, render_template, request
import pandas as pd
from exchanges import exchange

app = Flask(__name__)

exch = exchange()
dataframe = exch.combine_dataframes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_matrix', methods=['POST'])
def generate_matrix():
    coin = request.form['coin']
    df = dataframe[dataframe['symbol'] == coin]
    exchanges = df['exchange'].unique().tolist()
    matrix = pd.DataFrame(columns=exchanges, index=exchanges)
    matrix.index.name = 'Exchange'
    for i in range(len(exchanges)):
        for j in range(len(exchanges)):
            if i != j:
                rate1 = df[df['exchange'] == exchanges[i]]['askRate'].min()
                rate2 = df[df['exchange'] == exchanges[j]]['bidRate'].max()
                diff = (rate1 - rate2) / rate1
                matrix.at[exchanges[i], exchanges[j]] = diff
    return matrix.to_json()

if __name__ == '__main__':
    app.run(debug=True)
