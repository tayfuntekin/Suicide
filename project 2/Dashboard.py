import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from tqdm import tqdm

class TimeSeriesForecast:
    def __init__(self, data_file):
        self.df = pd.read_csv(data_file)
        self.df = self.df.drop(['text'], axis =1)
        print(self.df.columns)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['label'] = self.df['label'].apply(lambda x : 1 if x == 'suicide' else 0)
        self.df['label'] = pd.to_numeric(self.df['label'], errors='coerce')
        print('NULL', self.df['label'].isnull().sum())
        print('UNQ',  self.df['label'].unique())
        self.df = self.df.set_index('Date')
    
    def make_forecast(self, series, order, n, window_size):
        forecast = []
        for i in tqdm(range(n)):
            train_data = series[:-(n - i)]
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                model = ARIMA(train_data, order=order)
                model_fit = model.fit()
                forecast.append(model_fit.forecast(steps=1).to_list()[0])
        return forecast
    
    def create_plots(self, window_size=20):
        week_forecast = self.make_forecast(self.df['label'], order=(1, 1, 1), n=7, window_size=window_size)
        month_forecast = self.make_forecast(self.df['label'], order=(1, 1, 1), n=30, window_size=window_size)
        three_month_forecast = self.make_forecast(self.df['label'], order=(1, 1, 1), n=90, window_size=window_size)
        fig1 = px.line(self.df, x=self.df.index, y='label')
        fig1.update_layout(title='Time Series Plot')
        
        fig2 = px.line(x=np.arange(7), y=week_forecast)
        fig2.update_layout(title='1 Week Forecast')
        
        fig3 = px.line(x=np.arange(30), y=month_forecast)
        fig3.update_layout(title='1 Month Forecast')
        
        # fig4 = px.line(x=np.arange(90), y=three_month_forecast)
        # fig4.update_layout(title='3 Month Forecast')
        
        return fig1, fig2, fig3#, fig4
    
    def run_dashboard(self, window_size=20):
        fig1, fig2, fig3 = self.create_plots(window_size=window_size)
        
        app = dash.Dash(__name__)
        app.layout = html.Div([
            html.H1('Time Series Forecasting Dashboard'),
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3)
            # dcc.Graph(figure=fig4)
        ])

        app.run_server(debug=True)


# Usage
if __name__ == '__main__':
    tsf = TimeSeriesForecast('SuicideData.csv')
    tsf.run_dashboard(window_size=20)

