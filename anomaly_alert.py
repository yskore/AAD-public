from mean_deviation import mean_deviation
from fetch_ga4data import fetch_ga4_data



import schedule
import time
import datetime
import smtplib
from email.mime.text import MIMEText
import ssl


# Get the current date
today = time.strftime("%Y-%m-%d")

# Fetch data for the current date
data_today = fetch_ga4_data(today, today)



# Function to send email alert
start_date = '2023-07-01'
end_date = '2023-07-31'

data_set= fetch_ga4_data(start_date,end_date)
def send_email_alert(discrepancy_date, deviation):
    sender_email = " "
    receiver_email = " "
    password = " "

    subject = "GA4 Attribution Anomaly Alert"
    message = f"Date: {discrepancy_date}\nSession_start event count and Sessions metric deviation: {deviation:.2f}\n\nYou are receiving this alert because an usual discrepancy has been identified between your session_start event count and sessions metric count This could lead to you seeing (not set) values and other data discrepancies in your property. Please investigate or reach out to the Analytics support team"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)  # Replace with your SMTP server and port
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print("Failed to send email alert:", e)

# Function to check daily deviation and send email alert if needed
def check_daily_deviation():

    

    # Calculate the deviation for the current date
    deviation_today = mean_deviation(data_today["session_start_count"], data_today["sessions_metric_count"])

    # Compare with the boundary and send email alert if the deviation is greater
    boundary = mean_deviation(data_set['session_start_counts'], data_set['sessions_metric_counts'])
    
    if deviation_today > boundary:
        send_email_alert(today, deviation_today)
        return('Email sent')
    else: print('no discrepancy observed')





if (data_today != None):
    # Schedule the daily job to run at a specific time (e.g., 9:00 AM)
    schedule.every().day.at("19:00").do(check_daily_deviation)
    

    # Run the schedule loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 60 seconds between iterations
else:
    print('Job not performed because there is no data available today')





