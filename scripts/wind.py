import ee
import pandas as pd
import numpy as np

# Initialize Earth Engine
ee.Initialize(project='plock-air-468917')

# Define point and time range
point = ee.Geometry.Point([19.70, 52.55])  # Płock coordinates
start_date = '2024-01-01'
end_date = '2024-12-31'

# Load ERA5-Land hourly wind data
dataset = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
    .filterBounds(point) \
    .filterDate(start_date, end_date) \
    .select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])

# Extract time series
timeseries = dataset.getRegion(point, scale=1000).getInfo()

# Convert to DataFrame
df = pd.DataFrame(timeseries[1:], columns=timeseries[0])
df['datetime'] = pd.to_datetime(df['time'], unit='ms')

# Calculate wind speed (magnitude)
df['wind_speed'] = np.sqrt(df['u_component_of_wind_10m']**2 + df['v_component_of_wind_10m']**2)

# Calculate wind direction (degrees, meteorological convention)
df['wind_direction_deg'] = np.degrees(np.arctan2(-df['u_component_of_wind_10m'], 
                                                  -df['v_component_of_wind_10m'])) % 360

# Convert degrees to cardinal directions
def degrees_to_cardinal(d):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

df['wind_direction_cardinal'] = df['wind_direction_deg'].apply(degrees_to_cardinal)

# Select final columns
final_columns = [
    'datetime',
    'u_component_of_wind_10m',
    'v_component_of_wind_10m',
    'wind_speed',
    'wind_direction_deg',
    'wind_direction_cardinal'
]
df = df[final_columns]

# Save to CSV
df.to_csv('plock_wind_2024_complete.csv', index=False)
print("CSV saved with all wind metrics!")