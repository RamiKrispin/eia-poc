import eia_etl 
import eia_api
import eia_forecast as fc
from darts import TimeSeries
import datetime
import pandas as pd
import numpy as np
log_file = eia_etl.load_log(path = "data/us48_metadata.csv")

print(log_file.last_success)
print(log_file.end)
print(log_file.start)
start = log_file.start


api_path = "electricity/rto/region-data/data"
facets = {
    "respondent": "US48",
    "type": "D"
}

offset = 2250

eia_api_key = os.getenv('EIA_API_KEY')


metadata = eia_etl.get_api_end(api_key = eia_api_key, 
api_path = "electricity/rto/region-data/", offset = 16)
print(metadata.end_fix)

end_fix = metadata.end_fix

end = end_fix

# print(end)


new_data = eia_etl.eia_data_refresh(start = start, 
                                    end = end_fix, 
                                    api_key = eia_api_key, 
                                    api_path = api_path, 
                                    facets = facets) 
append_data = eia_etl.append_new_data(data_path = "data/us48.csv",
                           log_path = "data/us48_metadata.csv",
                           new_data = new_data,
                           save = True)

data = append_data.data

h = 24
freq = 24
num_sample = 500 

forecast_start = data["period"].max().floor(freq = "d")
ts_start = forecast_start - datetime.timedelta(hours = freq * 365 * 2)
d1 = data[(data["period"] > ts_start) & (data["period"] < forecast_start)]
ts_obj = pd.DataFrame(np.arange(start = d1["period"].min(), stop = d1["period"].max() + datetime.timedelta(hours = 1), step = datetime.timedelta(hours = 1)).astype(datetime.datetime), columns=["index"])
ts_obj  = ts_obj.merge(d1, left_on = "index", right_on = "period", how="left")
input1 = TimeSeries.from_dataframe(d1,time_col= "period", value_cols= "value")

end =  data["period"].max()
input = fc.set_input(input = data, start = ts_start, end = end)
fc1 = fc.train_lm(input = input, 
            lags = [ -freq, -7 * freq,  - 365 * freq],
            likelihood = "quantile",
            quantiles = [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975],
            h = h,
            pi = 0.95,
            num_samples = 500)


print(fc1.log)

log = fc.append_log(log_path= "data/fc48_metadata.csv", new_log = fc1.log, save = False)

new_fc = fc.append_forecast(fc_path =  "data/fc48.csv", fc_new = fc1, save = False)

new_log = fc.score_forecast(log_path = "data/fc48_metadata.csv", actual = data, forecast = new_fc)
