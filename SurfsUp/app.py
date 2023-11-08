# Importing related libraries and modules:

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta



# 1. import Flask
from flask import Flask, jsonify
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route
@app.route("/")
def hello_world():
    return (
        f"<h1>Available routes:</h1>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start> <br/>"
    )

#@app.route("/api/v1.0/precipitation")
#################################################   
#SQLAlchemy

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station


@app.route("/api/v1.0/precipitation")
def date_prcp():
# Create our session (link) from Python to the DB
    session = Session(engine)

    recent_date=session.query(Measurement).group_by(Measurement.date).order_by(Measurement.date.desc()).first()

    last_date_string=recent_date.date
    last_date=datetime.strptime(last_date_string,"%Y-%m-%d").date()
    one_year_ago=last_date-timedelta(days=365)




    results = session.query(Measurement.date, Measurement.prcp)\
                 .filter(Measurement.date >= one_year_ago, Measurement.prcp.isnot(None)).all()

# Create a dictionary from date and prcp retrieved above    
    date_prcp={date:prcp for date, prcp in results} 

    session.close()







    ####################################################################
    ####################################################################
    ####################################################################
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)

   
    results = session.query(Station.id, Station.name)\
                 .group_by(Station.station).all()

# Create a dictionary from date and prcp retrieved above    
    station={id:name for id, name in results} 


    

    session.close()




    return jsonify(station)




if __name__ == "__main__":
    app.run(debug=True)
