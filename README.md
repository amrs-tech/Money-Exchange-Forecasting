# Money-Exchange-Forecasting
A simple django web app to forecast the currency exchange rate with the historical data of currency rates from https://www.exchangeratesapi.io/

## Requirements
Refer the requirements.txt file

## How to use it
1. Download this repo and then open it in a Python IDE (in my case PyCharm).
2. Run ``pip install -r requirements.txt`` to install all the packages required.
3. Start the django server to get the app running in localhost.

## Modules
1. First page displays the form for the user to fill in details to get historical data of exchange rates.
2. The app will train the model with fetched data and forecast the rate for the future period provided by user.
3. The output is displayed in table and chart for more spectacular visualization.
