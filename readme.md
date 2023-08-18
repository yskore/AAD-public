
### How does it work
- A 'boundary' variable is created and is equal to the calculation of the mean of the deviation between session_start event count and the sessions metric count for a previous data range ( > a month). The date range chosen should be one with relatively ‘normal’ data as this will be used for referencing against potential attribution issues

- For each day going forward, the difference between the session_start event count and sessions metric will be computed and compared against the 'boundary' variable

- If the difference is greater than the boundary, an alert is sent to the user via email about a potential attribution anomaly.

Before you begin, be sure to follow the steps [here](https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart-client-libraries) to connect to the GA4 API and create a service account.


**fetch_ga4data.py**

This file:

- Gets the current date and time

- Contains a credentials variable which will store the path to your service account credentials JSON file.

- Contains propertyID variable. Replace with your GA4 property ID

- Creates the GA4 service object

- The function ‘fetch_ga4_data’ takes two arguments: start_date and end_date

- It defines and executes the GA4 API request using the runReport() method from the ga4_service

- The data from this request is then extracted and stored in the data variable

- The data includes the date and event name dimensions as well as the sessions and event count metric. A dimension filter is applied to allow for only the session_start event to be collected.

- It then returns a dictionary consisting of “dates”, “session_start_count” and “sessions_metric_count” as keys with their respective values

Towards the end of the file, you will be able to set the start_date and end_date values which will be the ‘previous data range’ mentioned in this section.


**mean_deviation.py**

This file:

- Leverages the data pulled from the fetch_ga4data.py file and calculates the difference between session_start event count and sessions metric count for each day 

- Calculates the absolute deviation for each day

- Calculates and returns the mean deviation


**anomaly_alert.py**

This file:

- Checks daily to see if the deviation for the current day is greater than the boundary. If it is, then it flags this as a potential attribution anomaly and an email is sent to the address specified. This is a scheduled job that runs constantly at a specified time.


In order to start the program, ensure all required variables have values and then run the anomaly_alert.py file. 


**Note**: If you encounter an SSL certificate error, this is caused by the sender email address having two-step authentication and an app password should be used instead of the user's  email address password. You can do this [here](https://knowledge.workspace.google.com/kb/how-to-generate-an-app-passwords-000009237).