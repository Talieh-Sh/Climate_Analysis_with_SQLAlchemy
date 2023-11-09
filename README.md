
# SQLAlchemy Climate Analysis and flask
Project Overview
This project provides climate analysis and creates a Flask API for weather-related data. It utilizes Python, SQLAlchemy, Pandas, and Matplotlib.


## Project Overview
This project provides climate analysis and creates a Flask API for weather-related data. It utilizes Python, SQLAlchemy, Pandas, and Matplotlib.

## Completed Steps

### Part 1: Analyze and Explore the Climate Data
- Connected to the SQLite database using SQLAlchemy.
- Reflected tables into classes with SQLAlchemy's automap_base() and created a session.
- **Analyzed Precipitation:**
  - Retrieved the most recent date.
  - Queried the last 12 months of precipitation data.
  - Plotted the data.
- **Explored Station Data:**
  - Calculated the total number of stations.
  - Identified the most active stations.
  - Calculated min, max, and average temperatures.
  - Plotted temperature observations as a histogram.

### Part 2: Design Your Climate App
- **Designed Flask API routes:**
  - `/`: Homepage listing available routes.
  - `/api/v1.0/precipitation`: Provides precipitation data as JSON.
  - `/api/v1.0/stations`: Offers a JSON list of stations.
  - `/api/v1.0/tobs`: Provides temperature observations for the most active station as JSON.
  - `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Offers temperature statistics for specified dates.

## Tools Used
- Python
- SQLAlchemy
- Pandas
- Matplotlib
- Flask
