



from google.oauth2 import service_account
from googleapiclient.discovery import build
import time
import datetime

# Replace 'YOUR_CREDENTIALS_JSON_FILE_PATH' with the path to your service account credentials JSON file.
credentials = service_account.Credentials.from_service_account_file('<CREDENTIALS>')
today = time.strftime("%Y-%m-%d")

#Replace with your propertyID
property_id= '<propertyID>'

# Create the GA4 service object.
analyticsdata = build('analyticsdata', 'v1beta', credentials=credentials)
no_data= 'No data available'

# Function to fetch data using the GA4 API.
def fetch_ga4_data(start_date, end_date):
     
    # Define the GA4 API request.
    request = {
        'property': f'properties/{property_id}',
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'name': 'sessions'},{'name': 'eventCount'} ],
        'dimensions': [{'name': 'date'}, {'name': 'eventName'}],
        'dimensionFilter' : {
            'filter': {'fieldName': 'eventName', 'stringFilter': {'value': 'session_start', 'matchType': 'Exact'}}
        },
        'keepEmptyRows': True,
        'returnPropertyQuota': True
    }

    # Execute the API request using the runReport() method from the ga4_service.
    response = analyticsdata.properties().runReport(property= f'properties/{property_id}',body=request).execute()
    

    # Extract the data.
    data = response.get('rows',[])
    if not data:
        print("No data available")
        return None
   

    dates = [row['dimensionValues'][0]['value'] for row in data]
    session_start_counts = [int(row['metricValues'][1]['value']) for row in data]
    
    # Check if the 'eventCount' metric exists in the response.
    #event_counts = [int(row['metricValues'][1]['value']) if len(row['metricValues']) >= 2 else 0 for row in data]

    return {
        "dates": dates,
        "session_start_count": session_start_counts,
        "sessions_metric_count": [int(row['metricValues'][0]['value']) for row in data],
        
    }

# Define the date range for which you want to fetch the data.
start_date = '2023-07-01'
end_date = '2023-07-31'

# Fetch the data using the GA4 API.
data = fetch_ga4_data(start_date, end_date)


# Now, you can use the 'data' dictionary to calculate the mean deviation
