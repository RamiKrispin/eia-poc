import dev_fc as fc
import pandas as pd
import datetime



md_params = fc.model_params(model = "LinearRegressionModel",
                    model_label = "model 1",
                    comments = "LM Model",
                    h = 24,
                    lags = [-24, -7 * 24, - 365 * 24],
                    freq = 24,
                    pi = 0.95,
                    train_length =  24 * 365 * 2,
                    num_samples= 500,
                    likelihood = "quantile",
                    quantiles = [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975],
                    seed = 12345)  

mlflow_settings = fc.mlflow_params(path = "./metadata/",
                                experiment_name = "Forecast Dev",
                                type = "forecast",
                                score = False,
                                append = False,
                                version = "0.0.1")


data = pd.read_csv("./data/us48.csv")
data["period"] = pd.to_datetime(data["period"])
end = data["period"].max().floor(freq = "d")  - datetime.timedelta(hours = 1)
data = data[data["period"] <= end]
data.tail

start = end - datetime.timedelta(hours = md_params.train_length)

forecast_start = data["period"].max().floor(freq = "d")

input = fc.set_input(input = data, start = start, end = end)

x = fc.forecast_object()
x.add_input(input = input) 
x.add_model_params(model_params =  md_params)    
x.add_mlflow_settings(mlflow_settings = mlflow_settings)
x.create_forecast()