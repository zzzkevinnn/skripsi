from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        minggu = int(request.form.get('minggu'))
        breakout = request.form.get('breakout')
        roc_period = int(request.form.get('roc_period'))
        min_roc = float(request.form.get('min_roc'))
        avt_period = int(request.form.get('avt_period'))
        min_value = float(request.form.get('min_value'))
        atr_period = int(request.form.get('atr_period'))
        min_atr = float(request.form.get('min_atr'))
        max_atr = float(request.form.get('max_atr'))

        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=minggu)

        # Load stock symbols from JSON file
        with open('list-1.json') as file:
            stocks = json.load(file)

        lulus = []

        for stock_symbol in stocks:
            try:
                stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

                all_time_high = stock_data['Close'].max()
                last_close = stock_data['Close'].iloc[-1]
                start_date_close = stock_data['Close'][0]

                if last_close == all_time_high and (start_date_close * 2) < last_close:
                    roc = ((last_close - start_date_close) / start_date_close) * 100
                    if roc >= min_roc:
                        lulus.append({
                            "roc": roc,
                            "kode_saham": stock_symbol,
                            "harga_hari_ini": last_close,
                            "harga_awal": start_date_close,
                            "link_saham": f"https://finance.yahoo.com/quote/{stock_symbol}"
                        })
            except Exception as e:
                print(f"Failed to retrieve data for {stock_symbol}: {str(e)}")

        if lulus:
            df = pd.DataFrame(lulus)
            df.to_excel("stock_analysis.xlsx", index=False)

        return render_template('result.html', lulus=lulus, total=len(lulus), minggu=minggu)

    return render_template('perhitungan.html')

if __name__ == '__main__':
    app.run(debug=True)
