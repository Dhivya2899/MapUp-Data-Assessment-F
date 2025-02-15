# -*- coding: utf-8 -*-
"""python_task_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11mUQyxfNk6jfjgjcTrjXPBSzvo61XRLH

# QUESTION NO:1
# Car Matrix Generation
"""

import pandas as pd
import networkx as nx

df2 =pd.read_csv('/content/dataset-3.csv')

def compute_unique_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:


    # Create a directed graph
    G = nx.from_pandas_edgelist(df, 'id_start', 'id_end', ['distance'], create_using=nx.DiGraph())

    # Create an undirected graph for symmetric distances
    G_undirected = G.to_undirected()

    # Get unique nodes from the graph
    nodes = sorted(set(G.nodes) | set(node for edge in G.edges for node in edge))

    # Initialize distance matrix with zeros
    unique_distance_matrix = pd.DataFrame(index=nodes, columns=nodes, dtype=float)
    unique_distance_matrix[:] = 0.0

    # Fill in the matrix with cumulative distances
    for source in nodes:
        for target in nodes:
            if source != target:
                try:
                    # Use bidirectional shortest path for cumulative distances
                    unique_distance_matrix.at[source, target] = nx.bidirectional_dijkstra(G_undirected, source=source, target=target, weight='distance')[0]
                except nx.NetworkXNoPath:
                    # If there is no path, set the distance to NaN or a suitable default
                    unique_distance_matrix.at[source, target] = float('inf')

    return unique_distance_matrix



result_matrix = compute_unique_distance_matrix(df2)
print(result_matrix)

"""# QUESTION NO: 2
# Car Type Count Calculation

# TYPE 1
"""

import pandas as pd

df2 =pd.read_csv('/content/dataset-3.csv')

def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    # Create an empty list to store unrolled distances
    unrolled_distances = []

    # Iterate over the rows of the distance matrix
    for id_start, row in distance_matrix.iterrows():
        # Iterate over the columns, excluding the diagonal
        for id_end, distance in row.items():
            if id_start != id_end:
                # Append the data to the unrolled_distances list
                unrolled_distances.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance
                })

    # Create a DataFrame from the list
    result_unrolled = pd.DataFrame(unrolled_distances, columns=['id_start', 'id_end', 'distance'])

    return result_unrolled

# Assuming result_matrix is the DataFrame generated from the calculate_distance_matrix function
result_unrolled = unroll_distance_matrix(result_matrix)

# Print the entire DataFrame without ellipses
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(result_unrolled)

"""# TYPE 2"""

import pandas as pd
df2 =pd.read_csv('/content/dataset-3.csv')

def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Create an empty list to store unrolled distances
    unrolled_distances = []

    # Step 2: Iterate over the rows of the distance matrix
    for id_start, row in distance_matrix.iterrows():
        # Step 3: Iterate over the columns, excluding the diagonal
        for id_end, distance in row.items():
            if id_start != id_end:
                # Step 4: Append the data to the unrolled_distances list
                unrolled_distances.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance
                })

    # Step 5: Create a DataFrame from the list
    result_unrolled = pd.DataFrame(unrolled_distances, columns=['id_start', 'id_end', 'distance'])

    # Step 6: Return both the DataFrame and the unrolled_distances list
    return result_unrolled, unrolled_distances

# Step 7: Assuming result_matrix is the DataFrame generated from the calculate_distance_matrix function
result_unrolled, unrolled_distances = unroll_distance_matrix(result_matrix)

# Step 8: Print the process and the resulting DataFrame
print("Step 1: Create an empty list to store unrolled distances")
print("unrolled_distances =", unrolled_distances)
print("\nStep 2: Iterate over the rows of the distance matrix")
for id_start, row in result_matrix.iterrows():
    print(f"\nProcessing row with id_start = {id_start}")

    # Step 3: Iterate over the columns, excluding the diagonal
    for id_end, distance in row.items():
        if id_start != id_end:
            # Step 4: Append the data to the unrolled_distances list
            print(f"  Appending data: id_start = {id_start}, id_end = {id_end}, distance = {distance}")

# Step 5: Create a DataFrame from the list
print("\nStep 5: Create a DataFrame from the list")
print("result_unrolled =", result_unrolled)

# Step 8: Print the resulting DataFrame
print("\nResulting DataFrame:")
print(result_unrolled)

"""# QEUESTION NO: 3
# Bus Count Index Retrieval
"""

import pandas as pd
df2 =pd.read_csv('/content/dataset-3.csv')
def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_value: int) -> list:
    # Print Step 1: Filtering rows based on the reference_value in id_start column
    print(f"Step 1: Filtering rows with id_start equal to {reference_value}")
    reference_rows = df[df['id_start'] == reference_value]
    print(reference_rows)

    # Print Step 2: Calculate the average distance for the reference value
    print("\nStep 2: Calculating the average distance for the reference value")
    reference_avg_distance = reference_rows['distance'].mean()
    print(f"Average distance for {reference_value}: {reference_avg_distance}")

    # Print Step 3: Calculate the threshold range (10% of the average distance)
    print("\nStep 3: Calculating the 10% threshold range")
    threshold_lower = reference_avg_distance - (0.1 * reference_avg_distance)
    threshold_upper = reference_avg_distance + (0.1 * reference_avg_distance)
    print(f"Threshold Lower: {threshold_lower}, Threshold Upper: {threshold_upper}")

    # Print Step 4: Filtering rows within the 10% threshold
    print("\nStep 4: Filtering rows within the 10% threshold")
    within_threshold_rows = df[(df['id_start'] != reference_value) & (df['distance'] >= threshold_lower) & (df['distance'] <= threshold_upper)]
    print(within_threshold_rows)

    # Print Step 5: Get unique values from id_start column and sort them
    print("\nStep 5: Getting unique values from id_start column and sorting them")
    within_threshold_ids = sorted(within_threshold_rows['id_start'].unique())
    print(f"IDs within the 10% threshold: {within_threshold_ids}")

    return within_threshold_ids

# Assuming result_unrolled is the DataFrame generated from the unroll_distance_matrix function
reference_value = 1001400  # Replace this with the desired reference value
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled, reference_value)

# Print the final result
print("\nFinal Result:")
print(result_within_threshold)

"""# QUESTION NO: 4
# Route Filtering
"""

import pandas as pd
df2 =pd.read_csv('/content/dataset-3.csv')

def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Iterate over each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        # Calculate toll rates by multiplying the distance with the rate coefficient
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Assuming result_unrolled is the DataFrame generated from the unroll_distance_matrix function
result_with_toll_rates = calculate_toll_rate(result_unrolled)

# Set pandas options to display all rows
pd.set_option('display.max_rows', None)

# Assuming result_with_toll_rates is the DataFrame generated from the calculate_toll_rate function
print(result_with_toll_rates)

# Reset pandas options to default (optional)
pd.reset_option('display.max_rows')

"""# QUESTION NO: 5
# Calculate Time-Based Toll Rates
"""

import pandas as pd
from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)), (time(10, 0, 0), time(18, 0, 0)), (time(18, 0, 0), time(23, 59, 59))]
    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]

    # Define discount factors for different time ranges
    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    # Create lists to store start_day, start_time, end_day, and end_time
    start_day_list = []
    start_time_list = []
    end_day_list = []
    end_time_list = []

    # Iterate over each unique (id_start, id_end) pair
    for _, row in df[['id_start', 'id_end']].drop_duplicates().iterrows():
        id_start, id_end = row['id_start'], row['id_end']

        for day_offset in range(7):  # Cover all 7 days of the week
            for (start_time, end_time), discount_factor in zip(weekday_time_ranges, weekday_discount_factors):
                start_datetime = datetime.combine(datetime.now(), start_time) + timedelta(days=day_offset)
                end_datetime = datetime.combine(datetime.now(), end_time) + timedelta(days=day_offset)

                start_day_list.append(start_datetime.strftime('%A'))
                start_time_list.append(start_datetime.time())
                end_day_list.append(end_datetime.strftime('%A'))
                end_time_list.append(end_datetime.time())

            for start_time, end_time in weekend_time_ranges:
                start_datetime = datetime.combine(datetime.now(), start_time) + timedelta(days=day_offset)
                end_datetime = datetime.combine(datetime.now(), end_time) + timedelta(days=day_offset)

                start_day_list.append(start_datetime.strftime('%A'))
                start_time_list.append(start_datetime.time())
                end_day_list.append(end_datetime.strftime('%A'))
                end_time_list.append(end_datetime.time())

    # Add the new columns to the DataFrame
    df['start_day'] = start_day_list
    df['start_time'] = start_time_list
    df['end_day'] = end_day_list
    df['end_time'] = end_time_list

    # Modify the values of vehicle columns based on time ranges and discount factors
    for column in ['moto', 'car', 'rv', 'bus', 'truck']:
        df[column] = df.apply(lambda row: row[column] * discount_factor(row), axis=1)

    return df

# Define a function to calculate discount factor based on time range and day of the week
def discount_factor(row):
    weekday = row['start_day']
    start_time = row['start_time']

    if weekday in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        for (time_range, _), factor in zip(weekday_time_ranges, weekday_discount_factors):
            if time_range[0] <= start_time <= time_range[1]:
                return factor
    else:
        return weekend_discount_factor

# Assuming result_with_toll_rates is the DataFrame generated from the calculate_toll_rate function
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)

# Print the resulting DataFrame with time-based toll rates
print(result_with_time_based_toll_rates)