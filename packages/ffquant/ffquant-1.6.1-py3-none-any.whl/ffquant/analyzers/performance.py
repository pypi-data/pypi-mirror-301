import backtrader as bt
import numpy as np
import dash
from dash import dash_table
from dash import dcc, html
import pandas as pd
import ffquant
import plotly.graph_objs as go
from ffquant.strats.MyStrategy import MyStrategy
from datetime import datetime

def init_analyzers(cerebro):
    cerebro.addanalyzer(bt.analyzers.Returns, 
                        _name='returns', 
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1,
                        tann=252 * 6.5 * 60)

    cerebro.addanalyzer(bt.analyzers.TimeReturn, 
                        _name='timereturn',
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, 
                        _name='sharpe',
                        timeframe=bt.TimeFrame.Minutes,
                        compression=1,
                        annualize=True)

    cerebro.addanalyzer(bt.analyzers.DrawDown, 
                        _name='drawdown')

def show_performance(strats):
    for strat in strats:
        returns = strat.analyzers.returns.get_analysis()
        # print(f"Total Compound Return: {returns['rtot']:.2%}")
        # print(f"Annualized Return: {returns['rnorm']:.2%}")

        sharpe = strat.analyzers.sharpe.get_analysis()
        # print(f"Sharpe Ratio: {sharpe['sharperatio']:.2f}")

        timereturn = strat.analyzers.timereturn.get_analysis()
        timereturn_list = list(timereturn.values())
        volatility = np.std(timereturn_list)
        annual_volatility = volatility * np.sqrt(252)
        # print(f"Annualized Volatility: {annual_volatility:.2%}")

        drawdown = strat.analyzers.drawdown.get_analysis()
        # print(f"Max Drawdown: {drawdown.max.drawdown:.2f}%")
        # print(f"Max Drawdown Duration: {drawdown.max.len}")

        views = []

        # Metrics Table
        metrics_data = {
            "Metrics": [
                "Total Compound Return", 
                "Annualized Return", 
                "Sharpe Ratio", 
                "Annualized Volatility", 
                "Max Drawdown", 
                "Max Drawdown Duration"
            ],
            "Result": [
                f"{returns['rtot']:.2%}", 
                f"{returns['rnorm']:.2%}", 
                f"{sharpe['sharperatio']:.2f}", 
                f"{annual_volatility:.2%}",
                f"{drawdown.max.drawdown:.2f}%",
                f"{drawdown.max.len}"
            ]
        }
        metrics_df = pd.DataFrame(metrics_data)
        views.append(dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in metrics_df.columns],
                data=metrics_df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold'
                },
                style_table={'width': '100%'}
        ))

        # TimeReturn Plot - Adjust to minute-level precision
        # timereturn_df = pd.DataFrame({
        #     'Date': pd.to_datetime(list(timereturn.keys())),  # Convert to datetime for minute precision
        #     'Time Return': timereturn_list
        # })

        # views.append(html.H1(children='Time Return Over Time'))
        # views.append(
        #     dcc.Graph(
        #         id='timereturn-graph',
        #         figure={
        #             'data': [
        #                 go.Scatter(
        #                     x=timereturn_df['Date'],
        #                     y=timereturn_df['Time Return'],
        #                     mode='lines',
        #                     name='Time Return'
        #                 )
        #             ],
        #             'layout': go.Layout(
        #                 title='Time Return Distribution',
        #                 xaxis={'title': 'Date', 'tickformat': '%Y-%m-%d %H:%M'},  # Format to show date and time to the minute
        #                 yaxis={'title': 'Return'},
        #                 hovermode='closest'
        #             )
        #         }
        #     )
        # )

        # Use PyFolio's transactions for Buy/Sell signals and ensure minute-level precision
        # transactions = strat.analyzers.pyfolio.get_analysis()['transactions']
        # transaction_df = pd.DataFrame(
        #     [(k, v[0][0], v[0][1], v[0][2], v[0][3], v[0][4]) for k, v in transactions.items() if isinstance(k, datetime)],
        #     columns=['Date', 'Amount', 'Price', 'Sid', 'Symbol', 'Value']
        # )

        # # 根据 Amount 划分买卖信号
        # buy_signals = transaction_df[transaction_df['Amount'] > 0]
        # sell_signals = transaction_df[transaction_df['Amount'] < 0]

        # data = strat.data.lines[0].array
        # print(data)
        # dates = [data.datetime.datetime(i) for i in range(len(data))]
        
        # opens = [data.open[i] for i in range(len(data))]
        # highs = [data.high[i] for i in range(len(data))]
        # lows = [data.low[i] for i in range(len(data))]
        # closes = [data.close[i] for i in range(len(data))]
        
        # ohlc_df = pd.DataFrame({
        #     'Date': dates,
        #     'Open': opens,
        #     'High': highs,
        #     'Low': lows,
        #     'Close': closes
        # })
        # ohlc_df['Date'] = pd.to_datetime(ohlc_df['Date'])  # Ensure Date is in minute precision

        # # Create the K-line chart with buy/sell points
        # views.append(html.H1(children='Market Data with Buy/Sell Points'))
        # views.append(
        #     dcc.Graph(
        #         id='kline-graph',
        #         figure={
        #             'data': [
        #                 go.Candlestick(
        #                     x=ohlc_df['Date'],
        #                     open=ohlc_df['Open'],
        #                     high=ohlc_df['High'],
        #                     low=ohlc_df['Low'],
        #                     close=ohlc_df['Close'],
        #                     name='K-line'
        #                 ),

        #                 go.Scatter(
        #                     x=buy_signals['Date'],
        #                     y=buy_signals['price'],
        #                     mode='markers',
        #                     marker=dict(color='green', size=10, symbol='triangle-up'),
        #                     name='Buy Signals'
        #                 ),

        #                 go.Scatter(
        #                     x=sell_signals['Date'],
        #                     y=sell_signals['price'],
        #                     mode='markers',
        #                     marker=dict(color='red', size=10, symbol='triangle-down'),
        #                     name='Sell Signals'
        #                 )
        #             ],
        #             'layout': go.Layout(
        #                 title='Market Data with Buy/Sell Points',
        #                 xaxis={'title': 'Date', 'tickformat': '%Y-%m-%d %H:%M'},
        #                 yaxis={'title': 'Price'},
        #                 hovermode='closest'
        #             )
        #         }
        #     )
        # )

        app = dash.Dash(__name__)
        app.layout = html.Div(views)


        app.run_server(host='0.0.0.0', 
            port=8050, 
            jupyter_mode="jupyterlab",
            jupyter_server_url="http://192.168.25.144:8050", 
            debug=True
        )