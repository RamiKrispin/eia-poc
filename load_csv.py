import eia_api
import os
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from ydata_profiling import ProfileReport

data = pd.read_csv("data/us48.csv")

data.head()
data.dtypes

data["time"] = pd.to_datetime(data["period"])
data.tail()


 df = eia_api.eia_get(api_key = eia_api_key, 
    api_path = api_path, 
    facets = facets, 
    start = start,
    end = end_api) 