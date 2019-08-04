import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

###############################
# Database Setup
###############################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session from Python to DB
session = Session(engine)

###############################
# Flask Setup
###############################
app = Flask(__name__)

###############################
# Flask Routes
###############################

@app.route("/")
def welcome():
    """List all available api routes."""
    return """<html>
    <body background = "https://wallpaperbro.com/img/631281.jpg">
    <center><strong><h1>Hawaii Flask API</h1></strong></center>
    <h3>Available API Routes:</h3>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/><br/>
    <a href="/api/v1.0/stations">/api/v1.0/stations</a><br/><br/>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/><br/>
    <a href="/api/v1.0/<start>">/api/v1.0/yyyy-mm-dd</a><br/><br/>
    <a href="/api/v1.0/<start>/<end>">/api/v1.0/yyyy-mm-dd/yyyy-mm-dd</a><br/><br/>
    <h4> Replace yyyy-mm-dd placeholders with desired start/end query dates </h4>
    </body>
    </html>
    """

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return date and precipitation"""
     # Query 
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).\
    order_by(Measurement.date).all()

    # Convert list of tuples into dictionary and return JSON 
    precipitation_dict = dict(precipitation)

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def station():
    "Return list of stations"
    # Query
    session = Session(engine)

    # List all of the unique stations
    active_station = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list and return JSON
    station_list = list(np.ravel(active_station))
     
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    "Return the dates and temperature observations from a year from the last data point"
    #Query
    session = Session(engine)

    # Query the last 12 months of temperature observation data
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date).\
    filter(Measurement.date > query_date).all()


    # Convert list of tuples into normal list and return JSON
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)
    
@app.route("/api/v1.0/<start>")
def start_date(start):
    "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range."
    start_date = start
    start_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        group_by(Measurement.date).\
        filter(Measurement.date >= start_date).all()
    
    # Convert List of Tuples Into Normal List
    start_range_list = list(start_range)
    # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
    return jsonify(start_range_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start/end range."
    start_date = start
    end_date = end
    start_end_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        group_by(Measurement.date).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    
    # Convert List of Tuples Into Normal List
    start_end_range_list = list(start_end_range)
    # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
    return jsonify(start_end_range_list)


    

if __name__ == '__main__':
    app.run(debug=True)