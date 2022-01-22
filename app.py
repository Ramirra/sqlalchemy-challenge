#import dependencies
import json
from mimetypes import read_mime_types
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

#save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup
app = Flask(__name__)

#flask routes
#home
@app.route("/")
def home():
    return (
        f"Welcome to my Home Page! <br/>"
        f"Available Routes:<br/>" 
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/(start) <br/>"
        f"/api/v1.0/(start)/(end)"
    )
    
#precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]
    precip_scores = session.query(*sel).filter(Measurement.date >= year_prior).all()

    #close session
    session.close()

    #create dictionary from query
    precipitation = {}
    for tuple in precip_scores:
        precipitation[tuple[0]] = tuple[1]

    #return json
    return jsonify(precipitation)

#stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve stations
    stations = session.query(Station.station).all()

    #close session
    session.close()

    #create list from query
    station = list(np.ravel(stations))

    #return json
    return jsonify(station)

#tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Find the most recent date in the data set
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and temperature
    year_temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_prior).\
    filter(Measurement.station == "USC00519281").all()

    #close session
    session.close()

    #create dictionary from query
    tob = {}
    for tuple in year_temp:
        tob[tuple[0]] = tuple[1]

    #return json
    return jsonify(tob)
    
#start


#start,end



if __name__ == "__main__":
    app.run(debug=True)