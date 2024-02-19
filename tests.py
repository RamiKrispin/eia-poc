import eia_etl 
import eia_api
import os
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

# df = eia_api.eia_get(api_key = eia_api_key, 
#                              api_path = api_path, 
#                              facets = facets, 
#                              start = start,
#                              end = end) 

# if df is not None and len(df.data) > 0:
#     start_match_flag = df.data["period"].min() == start
#     end_match_flag = df.data["period"].max() == end
#     start_act = df.data["period"].min()
#     end_act = df.data["period"].max()
#     n_obs = len(df.data)
#     na = df.data["value"].isna().sum()
#     if start_match_flag and end_match_flag and na == 0 and n_obs > 0:
#         print("Refresh successed")
#         success_flag = True
#     else:
#         success_flag = False
#         print("Refresh failed")
# else:
#     print("Refresh failed")
#     success_flag = False
#     start_match_flag = None
#     end_match_flag = None
#     start_act = None
#     end_act = None
#     n_obs = None
#     na = None
