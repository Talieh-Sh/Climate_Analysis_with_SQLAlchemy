# Importing related libraries and modules:

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta



#  import Flask
from flask import Flask, jsonify
# Initializing Flask application
app = Flask(__name__)

########################################### API Static Routes ########################################

# Start at the homepage.
# List all the available routes.

@app.route("/")
def beginning():
    return (
        f"<h1>Available routes:</h1>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"        # Route for data from a start date
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"   # Route for data between start and end dates
        f"Please fill in the &lt;start&gt; and &lt;end&gt; placeholders with dates in the YYYY-MM-DD format."
    )


#################################################   
#SQLAlchemy

#################################################
# SQLAlchemy database setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

####################################################################
####################################################################
####################################################################    
# 2 Convert the query results to a dictionary by using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
# Flask route to retrieve precipitation data

@app.route("/api/v1.0/precipitation")
def date_prcp():
# Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the most recent date and calculate the date one year ago
    recent_date=session.query(Measurement).group_by(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_string=recent_date.date
    last_date=datetime.strptime(last_date_string,"%Y-%m-%d").date()
    one_year_ago=last_date-timedelta(days=365)



    # Query for precipitation data starting from one year ago
    results_date_prcp = session.query(Measurement.date, Measurement.prcp)\
                 .filter(Measurement.date >= one_year_ago, Measurement.prcp.isnot(None)).all()
    # Convert query results to a dictionary
    results_date_prcp_dic=[{date : prcp for date, prcp in results_date_prcp}]
    session.close()
    # Return results in JSON format
    return(jsonify(results_date_prcp_dic))


    ####################################################################
    ####################################################################
# 3 Return a JSON list of stations from the dataset.

# Flask route to retrieve station data
@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for station data
    results_station = session.query(Station.station, Station.name)\
                 .group_by(Station.station).all()


    # Convert query results to a list of dictionaries
    active_station = [{"station": station, "name": name} for station, name in results_station]
    

    session.close()

    return jsonify(active_station)

    ####################################################################
    ####################################################################

# 4 Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

# Flask route to retrieve temperature observations of the most active station for the previous year
@app.route("/api/v1.0/tobs")
def date_tobc_most_active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Repeat query for the most recent date and calculate the date one year ago
    recent_date=session.query(Measurement).group_by(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_string=recent_date.date
    last_date=datetime.strptime(last_date_string,"%Y-%m-%d").date()
    one_year_ago=last_date-timedelta(days=365)
   

    #query for station and count of repeated
    station_activity=session.query(Measurement.station,func.count(Measurement.id)).\
    filter(Measurement.date >= one_year_ago).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.id).desc()).all()
  
    # Extracting the station ID of the most active station
    most_active_station=station_activity[0][0]
    # Querying the date and temperature observations of the most-active station for the previous year
    most_active_data=session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station,Measurement.date >= one_year_ago,Measurement.station==most_active_station)

    active_station_data = [{"date": date, "tobs": tobs} for date, tobs in most_active_data]
    
    session.close()

    return jsonify(active_station_data)

########################################### API Dynamic Routes ########################################

# 1 /api/v1.0/<start>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# API route to get data from a specified start date
@app.route("/api/v1.0/<start>")

def data_from_start_date(start):
# Create our session (link) from Python to the DB
    session = Session(engine)
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
    # Handling incorrect date format
    except ValueError:
        session.close()
        return f"<h1> Error: Data format should be YYYY-MM-DD , 400 </h1>"


    # Query to get minimum, maximum, and average temperatures from the start date
    results_data_from_start_date = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

# Create a dictionary from above results

    dict_data_from_start_date = [{
        "TMIN": result[0],
        "TMAX": result[1],
        "TAVG": result[2]} 
        for result in results_data_from_start_date]
    

    session.close()

    return jsonify(dict_data_from_start_date)



######################################
# 2 /api/v1.0/<start>/<end>
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
# API route to get data for a specified start and end date range

@app.route("/api/v1.0/<start>/<end>")

def data_from_start_to_end(start, end):
# Create our session (link) from Python to the DB
    session = Session(engine)
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        session.close()
        return f"<h1> Error: Data format should be YYYY-MM-DD , 400 </h1>"


    # Query to get minimum, maximum, and average temperatures for the date range
    results_data_from_start_to_end = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date ,Measurement.date<= end_date ).all()

# Create a dictionary from above results

    dict_data_from_start_to_end = [{
        "TMIN": result[0],
        "TMAX": result[1],
        "TAVG": result[2]} 
        for result in results_data_from_start_to_end]
    

    session.close()

    return jsonify(dict_data_from_start_to_end)



if __name__ == "__main__":
    app.run(port=8000,debug=True)
