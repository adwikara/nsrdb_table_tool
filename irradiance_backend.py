import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import sys
from urllib.error import HTTPError

# source = https://nsrdb.nrel.gov/data-sets/api-instructions.html

class getIrradience:
    def __init__(self, lat, lon):
        # declare inputs
        self.latitude = lat
        self.longitude = lon
        # initialize other variables
        self.year = '2018'
        self.api_key = 'qcS1rONVybE6Gtw1heDE0dFatuaHBmoVozd1weZX'
        self.attributes = 'ghi,dhi,dni,wind_speed,air_temperature' #'ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle'
        self.leap_year = 'false' # set leap year to true or false. True will return leap day data if present, false will not.
        self.interval = '60' #60 minutes, so hourly data
        self.utc = 'false'
        # other details
        self.your_name = 'Aditya+Wikara'
        self.reason_for_use = 'academic+research'
        self.your_affiliation = 'Boston+University'
        self.your_email = 'adwikara@bu.edu'
        self.mailing_list = 'false'
        # declare url string
        self.url = 'http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=self.year, lat=self.latitude, lon=self.longitude, leap=self.leap_year, interval=self.interval, utc=self.utc, name=self.your_name, email=self.your_email, mailing_list=self.mailing_list, affiliation=self.your_affiliation, reason=self.reason_for_use, api=self.api_key, attr=self.attributes)

    # get the start and end index for the NSRDB dataframe
    def get_today_index(self):
        days = datetime.now().timetuple().tm_yday
        day_end = days*24
        day_start = day_end - 24   
        return day_start,day_end
    
    # generate dataframe for daily data
    def generate_dataframe(self):
        # Return all but first 2 lines of csv to get data:
        df = pd.read_csv(self.url, skiprows=2)
        # Set the time index in the pandas dataframe:
        #525600 is number of minutes in a year
        df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=self.year), freq=self.interval+'Min', periods=525600/int(self.interval)))
        # drop some columns
        df = df.drop(["Year", "Month", "Day", "Hour", "Minute"], axis=1)
        # get the index
        (day_start, day_end) = self.get_today_index()
        return df[day_start:day_end]
    
    # convert dataframe to html
    def df2html(self):
        df = self.generate_dataframe()
        return df.to_html()

if __name__ == "__main__":
    lat = sys.argv[1]
    lon = sys.argv[2]
    
    #lat = 42.3505
    #lon = 71.1054

    #lat = -6.59
    #lon = 107

    try:
        x = getIrradience(lat,lon)
        df = x.generate_dataframe()
        result = df.to_html()
    except HTTPError:
        result = ""

    print(result)
    sys.stdout.flush()
    #print(df)
    #print(df.to_html('sample.html'))
    #print(df.to_html())
