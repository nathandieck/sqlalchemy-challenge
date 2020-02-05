# Flask skeleton from 11/Day 3/04 folder

# Imports
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import numpy as np
import datetime as dt

#Set up the database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create an app, being sure to pass __name__
app = Flask(__name__)

#Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(
        f"Welcome to the Hawai'i weather database.<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend"
    ) 


#Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    
    #Create a session with the database
    session = Session(engine)

    #Query preciptation and date

    results = session.query (Measurement.date, Measurement.prcp).all()

    session.close()

    torrential_downpours = []
    for date, prcp in results:
        rain_dict = {date: prcp}
        torrential_downpours.append(rain_dict)

    #this is the working code for when you screw up. 
    # torrential_downpours = []
    # for date, prcp in results:
    #     rain_dict = {}
    #     rain_dict["date"] = date
    #     rain_dict["precipitation"] = prcp
    #     torrential_downpours.append(rain_dict)

    return jsonify(torrential_downpours)


#Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    #Create a session with the database
    session = Session(engine)

    #Query preciptation and date

    results = session.query (Station.station, Station.name).all()

    session.close()

    secret_rebel_bases = []
    for station, name in results:
        station_dict = {}
        station_dict["station_code"] = station
        station_dict["place"] = name
        secret_rebel_bases.append(station_dict)

    return jsonify(secret_rebel_bases)


#Define what to do when a user hits the /api/v1.0/temperatures route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperatures' page...")

    #Create a session with the database
    session = Session(engine)

    maxdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    year_prior = dt.datetime.strptime(maxdate, "%Y-%m-%d") - dt.timedelta(days=365)
    year_prior_d = year_prior.date()

    sel4 = [Measurement.station,
        func.count(Measurement.id)]
    
    stat_cts = session.query(*sel4).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
   
    high_value=0
    for station in stat_cts:
        if station[1] > high_value:
            high_value = station[1]
    
    for station in stat_cts:
        if station[1] == high_value:
            active_station = station[0]

    sel1 = [Measurement.station, 
        Measurement.date,
        Measurement.tobs]

    results = session.query(*sel1).filter(Measurement.date >= year_prior_d).filter(Measurement.station == active_station).all()

    session.close()
    
    #Organize and jsonify the data.
    
    global_warming = []
    for station, date, temp in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["observation_date"] = date
        temp_dict["observed_temp"] = temp
        global_warming.append(temp_dict)

    return jsonify(global_warming)
    
#Define what to do when a user hits the /api/v1.0/start route
@app.route("/api/v1.0/start")
def start():
    print("Server received request for 'Start' page...")

    return (f"To query by start date enter the start date in format YYYY-MM-DD<br/>"
        "using format /api/v1.0/start/startdate")

@app.route("/api/v1.0/start/<start_date>")
def weather_by_start(start_date):
    start_date_1 = dt.datetime.strptime(start_date, "%Y-%m-%d")
    start_date_1 = start_date_1.date()

    sel2 = [func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]
    
    session = Session(engine)

    results = session.query(*sel2).filter(Measurement.date >= start_date_1).all()

    session.close()

    tempstart = []
    for minimum, average, maximum in results:
        startdict = {}
        startdict["minimum temp"] = minimum
        startdict["average temp"] = average
        startdict["maximum temp"] = maximum
        tempstart.append(startdict)
    
    return jsonify(startdict)

#Define what to do when a user hits the /api/v1.0/startend route
@app.route("/api/v1.0/startend")
def startend():
    print("Server received request for 'Start-End' page...")

    return (f"To query by start date enter the start date and end date in format YYYY-MM-DD<br/>"
        "using format /api/v1.0/startend/startdate/enddate")
    

@app.route("/api/v1.0/startend/<start_date>/<end_date>")
def weather_by_startend(start_date, end_date):
    start_date_2 = dt.datetime.strptime(start_date, "%Y-%m-%d")
    start_date_2 = start_date_2.date()
    end_date_2 = dt.datetime.strptime(end_date, "%Y-%m-%d")
    end_date_2 = end_date_2.date()

    sel3 = [func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]
    
    session = Session(engine)

    results = session.query(*sel3).filter(Measurement.date >= start_date_2).filter(Measurement.date <= end_date_2).all()

    session.close()

    tempstart = []
    for minimum, average, maximum in results:
        startdict = {}
        startdict["minimum temp"] = minimum
        startdict["average temp"] = average
        startdict["maximum temp"] = maximum
        tempstart.append(startdict)
    
    return jsonify(startdict)


# make the app runnable
if __name__ == "__main__":
    app.run(debug=True)
