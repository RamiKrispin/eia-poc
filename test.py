import eia_api
import datetime
import os

api_path = "electricity/rto/region-data/data"
facets = {
    "respondent": ["US48"],
    "type": "D"
}


start = datetime.datetime(2021, 7, 1, 0)
end = datetime.datetime(2023, 12, 15, 0)

eia_api_key = os.getenv('EIA_API_KEY')



df = eia_api.eia_backfile(api_key = eia_api_key, 
        api_path = api_path, 
        facets = facets, 
        start = start,
        end = end,
        offset = 2000) 


eia_api.eia_get(api_key=eia_api_key, api_path=api_path, facets = facets, start = start, end =end) 
