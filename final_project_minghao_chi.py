# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:38:51 2020

@author: mc590
"""

#final project, python seminar
#crunchbase

import sys
import json
import requests
import csv
from datetime import datetime, date, time, timedelta, timezone
RAPIDAPI_KEY  = "9e1dea1425msh447f7d479d726c6p15f5bajsnd2ae8944056f"
def trigger_api(since_time):
  querystring = {  "updated_since": str(since_time), "sort_order":"updated_at ASC"}
  headers = {
      'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
      'x-rapidapi-key': RAPIDAPI_KEY
        }
  url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"
  response = requests.request("GET", url, headers=headers, params=querystring)
  if(200 == response.status_code):
    return json.loads(response.text)
  else:
    return None
if __name__ == "__main__":
  try: 
    current_date = datetime.combine(date.today(), time(0, 0, 0))
    yesterday_date = current_date - timedelta(days=1)
    yday_timestamp_utc = int(yesterday_date.replace(tzinfo=timezone.utc).timestamp())
    print("Scanning Crunchbase API for company updates on " + yesterday_date.strftime("%m/%d/%YYYY"))
    print(yday_timestamp_utc)
    api_response = trigger_api(yday_timestamp_utc)
    with open('Crunchbase_Updated-' + yesterday_date.strftime("%m-%d-%Y") +  '.csv', 'w',newline='') as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow(["Name","Homepage", "Update Timestamp"])  
      for org in api_response["data"]["items"]:
        try: 
          org_name   = org["properties"]["name"]
          org_url    = org["properties"]["homepage_url"]
          org_update = str(org["properties"]["updated_at"])
          print("Adding Company: " + org_name)
          csv_writer.writerow([org_name,org_url,org_update])  
          
        except TypeError as e:
          print(e)
          print("Type Error...Ignoring")
          
        except csv.Error as e:
          print(e)
          print("CSV Error...Ignoring")
          
        except UnicodeEncodeError as e:
          print(e)
          print("Encoding Error...Ignoring")
          
      csv_file.close()
  except Exception as e:
    print("Major Exception ...Aborting")
    sys.exit(e)