# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

from flask import Flask, jsonify


#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

#################################################

# reflect an existing database into a new model
# reflect the tables

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)
#################################################




#################################################
# Flask Routes

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<br/>"
        )
#query of precipitation and getting the last year from the latest date
@app.route("/api/v1.0/precipitation")
def precipitation():
    #date as key and prcp as value
    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-22').\
    order_by(Measurement.date).all()

    precipitation_dict = {date:prcp for date, prcp in data}
    return jsonify(precipitation_dict)

#query of all the stations
@app.route("/api/v1.0/stations")
def stations():
    # Query the stations
    results = session.query(Station.station).all()

    # Convert the query results to a list
    station_list = list(np.ravel(results))

    # Return the JSON list of stations
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year
        
    temperature_data = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-08-23').all()
    # Create a list of temperature observations
    temp_list = list(np.ravel(temperature_data))
    # Return the JSON list of temperature observations
    return jsonify(temp_list)

#stats for a specific start date, can input any data in the url 
@app.route("/api/v1.0/<start>")
def temperature_stats_start(start):
    start = datetime.strptime(start, '%Y-%m-%d').date()
    # Query the minimum, average, and maximum temperatures for the dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temperature_stats = list(np.ravel(results))
    min = temperature_stats[0]
    avg = temperature_stats[1]
    max = temperature_stats[2]

    return (
        f'Min value = {min} F<br/>'
        f'Avg value = {avg} F<br/>'
        f'Max value = {max} <end>'
    )
    
    # Return the JSON representation of the temperature statistics
   
# stats for any start - end date
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_range(start, end):
    start = datetime.strptime(start, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    # Query the minimum, average, and maximum temperatures for the dates within the specified start and end date range (inclusive)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temperature_stats = list(np.ravel(results))
    min = temperature_stats[0]
    avg = temperature_stats[1]
    max = temperature_stats[2]
    
    # Return the JSON representation of the temperature statistics
    return (
        f'Min value = {min} F<br/>'
        f'Avg value = {avg} F<br/>'
        f'Max value = {max} <end>'
    )
session.close()
#################################################
if __name__ == "__main__":
    app.run(debug=True)

# just notes please ignore 
# 
        # #most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        #group_by(Measurement.station).\
        #order_by(func.count(Measurement.station).desc()).first()
        # most_act= list(np.ravel(most_active_station[0]))


    