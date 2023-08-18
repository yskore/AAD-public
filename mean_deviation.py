from fetch_ga4data import fetch_ga4_data
start_date = '2023-07-01'
end_date = '2023-07-31'

data_set= fetch_ga4_data(start_date,end_date)

def mean_deviation(session_start_counts, sessions_metric_counts):
    # Check if the length of both lists is the same
    if len(session_start_counts) != len(sessions_metric_counts):
        raise ValueError("Input lists must have the same length.")

    # Calculate the difference between session_start and sessions_metric for each day
    differences = [session - metric for session, metric in zip(session_start_counts, sessions_metric_counts)]

    # Calculate the absolute deviation for each day
    absolute_deviations = [abs(diff) for diff in differences]

    # Calculate the mean deviation
    mean_deviation = sum(absolute_deviations) / len(absolute_deviations)

    return mean_deviation

session_start_counts = data_set["session_start_count"]
sessions_metric_counts = data_set["sessions_metric_count"]

# Calculate the mean deviation
mean_deviation_value = mean_deviation(session_start_counts, sessions_metric_counts)

