"""
geocoding.py
Processes location data from us_perm_visas.csv
Saves unique identifier, latitude, longitude to visa_locations.csv
"""
__author__ = "SLPeoples"

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from socket import timeout
from time import sleep
import pandas as pd


def do_the_geocode_thing(location,g):
    """
    determines a latitude and longitude from a location
    :param location: city, state string
    :param j: number of tries attempted, default = 0
    :return: Either return location object or None type (after 3 tries)
    """
    lis = [line.split(",") for line in g]
    for row in lis:
        citystate = str(row[0]+" "+row[1]).lower()
        if citystate == location:
            return str(row[2]+", "+row[3])
        else:
            pass
    print("None found for: "+location)
    return None


def main():
    """
    Opens us_perm_visas.csv, then writes unique identifier, latitude, and longitude to visa_locations.csv
    """
    visas = pd.DataFrame.from_csv("C:/Users/Ripti/Desktop/us_perm_visas.csv") # Path to dataset.
    with open('visa_locations.csv', 'w') as f: # New data file for locations to be joined in Tableau.
        for i in range(len(visas)):
            states = {"alabama": "al", "alaska": "ak", "arizona": "az", "arkansas": "ar", "california": "ca",
                      "colorado": "co", "connecticut": "cn", "delaware": "de", "florida": "fl", "georgia": "ga",
                      "hawaii": "hi", "idaho": "id", "illinois": "il", "indiana": "in", "iowa": "ia", "kansas": "ks",
                      "kentucky": "ky", "louisiana": "la", "maine": "me", "maryland": "md", "massachusetts": "ma",
                      "michigan": "mi", "minnesota": "mn", "mississippi": "ms", "missouri": "mo", "montana": "mt",
                      "nebraska": "ne", "nevada": "nv", "new hampshire": "nh", "new jersey": "nj", "new mexico": "nm",
                      "new york": "ny", "north carolina": "nc", "north dakota": "nd", "ohio": "oh", "oklahoma": "ok",
                      "oregon": "or", "pennsylvania": "pa", "rhode island": "ri", "south carolina": "sc",
                      "south dakota": "sd", "tennessee": "tn", "texas": "tx", "utah": "ut", "vermont": "vt",
                      "virginia": "va", "washington": "wa", "west virginia": "wv", "wisconsin": "wi", "wyoming": "wy",
                      "district of columbia": "dc"}
            city = str(visas.employer_city[i]).lower().replace(",","")
            state = str(visas.employer_state[i]).lower()
            if len(state)>2:
                if state in states:
                    state = states[state]
                """
                if state != 'nan':
                    if state != 'guam':
                        if state != "puerto rico":
                            if state != "virgin islands":
                                state = states[state]
            """
            location = str(city+" "+state) # Grab city, state from DataFrame.
            with open('C:/Users/Ripti/Desktop/uscitiesv1.3.csv') as g:
                location = do_the_geocode_thing(location, g) # This is where the recursion for geocode attempts begins.
            g.close()
            if location != None: # Only write if it found a location
                location = str(str(visas.case_no[i])+", "+location)
                print(location) # Print progress
                f.write(location)
        f.close() # Close the csv and save.
    print("Completed")


if __name__ == "__main__":
    main()