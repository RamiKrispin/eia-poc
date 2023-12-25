import eia_api
import datetime
import os
import requests

api_path = "electricity/rto/region-data/data"
facets = {
    "respondent": "US48",
    "type": "D"
}


start = datetime.datetime(2021, 7, 1, 0)
start = datetime.datetime(2023, 12, 14, 0)
end = datetime.datetime(2023, 12, 15, 0)

eia_api_key = os.getenv('EIA_API_KEY')



df = eia_api.eia_backfile(api_key = eia_api_key, 
        api_path = api_path, 
        facets = facets, 
        start = start,
        end = end,
        offset = 2000) 

offset = 2250
df = eia_api.eia_backfile(api_key = eia_api_key, 
        api_path = api_path, 
        facets = facets, 
        start = start,
        end = end,
        offset = offset)  


# d = eia_api.eia_get(api_key=eia_api_key, api_path=api_path, facets = facets, start =  datetime.datetime(2021, 7, 1, 0), end = datetime.datetime(2021, 8, 1, 0)) 
d = eia_api.eia_get(api_key=eia_api_key, api_path=api_path, facets = facets, start =  start, end = end) 
d.data

d.data["period"] = pd.to_datetime(d.data["period"])

def eia_metadata(api_key, api_path = None):
    
    class response:
        def __init__(output, meta, url, parameters):
            output.meta = meta
            output.url = url
            output.parameters = parameters


    if type(api_key) is not str:
        print("Error: The api_key argument is not a valid string")
        return
    elif len(api_key) != 40:
        print("Error: The length of the api_key is not valid, must be 40 characters")
        return
    
    if api_path is None:
        url = "https://api.eia.gov/v2/" + "?api_key="
    else:
        if api_path[-1] != "/":
            api_path = api_path + "/"
        url = "https://api.eia.gov/v2/" + api_path + "?api_key="

    d = requests.get(url + api_key).json()

    parameters = {
        "api_path": api_path
    }

    output = response(url = url, meta = d["response"], parameters= parameters)

    return output 


     
d = eia_metadata(api_key= eia_api_key)
d.meta
d2 = eia_metadata(api_key= eia_api_key, api_path="electricity")
d2.meta


def hour_offset(start, end, offset):
    current = [start]
    while max(current) < end:
        if(max(current) + datetime.timedelta(hours = offset) < end):
            current.append(max(current) + datetime.timedelta(hours = offset))
        else:
           current.append(end) 
           
    return current

api_key = eia_api_key

api_path = "electricity/rto/region-data/data"
facets = {
    "respondent": "US48",
    "type": "D"
}

start = datetime.datetime(2015, 7, 1, 5)
end = datetime.datetime(2023, 12, 15, 0)

offset = 2250

class response:
        def __init__(output, data, parameters):
            output.data = data
            output.parameters = parameters
    
if type(api_key) is not str:
    print("Error: The api_key argument is not a valid string")

elif len(api_key) != 40:
    print("Error: The length of the api_key is not valid, must be 40 characters")


if api_path[-1] != "/":
    api_path = api_path + "/"    
if  type(start) is datetime.date:
    s = "&start=" + start.strftime("%Y-%m-%d")
elif type(start) is datetime.datetime:
    s = "&start=" + start.strftime("%Y-%m-%dT%H")
else:
    print("Error: The start argument is not a valid date or time object")

         
if  type(end) is datetime.date:
    e = "&end=" + end.strftime("%Y-%m-%d")
elif type(end) is datetime.datetime:
    e = "&end=" + end.strftime("%Y-%m-%dT%H")
else:
    print("Error: The end argument is not a valid date or time object")


if  type(start) is datetime.date:
    time_vec_seq = eia_api.day_offset(start = start, end = end, offset = offset)
elif  type(start) is datetime.datetime:
    time_vec_seq = eia_api.hour_offset(start = start, end = end, offset = offset)
    
    for i in range(len(time_vec_seq[:-1])):
        start = time_vec_seq[i]
        if i < len(time_vec_seq[:-1]) - 1:
            end = time_vec_seq[i + 1] -  datetime.timedelta(hours = 1)
        elif i == len(time_vec_seq[:-1]) -1:
            end = time_vec_seq[i + 1]
        temp = eia_get(api_key = api_key, 
                       api_path = api_path, 
                       facets= facets, 
                       start = start,
                       data = "value", 
                       end = end)
        if i == 0:
            df = temp.data
        else:
            df = df._append(temp.data)

parameters = {
    "api_path": api_path,
    "data" : "value",
    "facets": facets, 
    "start": start, 
    "end": end, 
    "length": None, 
    "offset": offset, 
    "frequency":None
}
output = response(data = df, parameters = parameters)


for i in range(len(time_vec_seq[:-1])):
    if i < len(time_vec_seq[:-1]):
        print(i)

