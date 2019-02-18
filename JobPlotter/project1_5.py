#!/usr/local/bin/python3

from lxml import html
from lxml import etree
import requests
import os
from sys import platform

import plotly.plotly as py
from plotly.graph_objs import *

from geopy.geocoders import Nominatim

mapbox_access_token = 'pk.eyJ1Ijoibndpc25pb3dza2kiLCJhIjoiY2pleWZjazdsMDZ4ZTJ3bWtzbnZlY3g1NiJ9.BOISXBifZUXWJbb781Azmg'

#Mac OS Notification method
def notify(title):
    os.system("""
              osascript -e 'display notification "{}" with title "New Job"'
              """.format(title))

#This returns the content of the URL
def geturldata():
	page = requests.get('https://stackoverflow.com/jobs/feed?location=newyork&range=50&distanceUnits=Miles')
	return page.content

#This returns job titles in a list
def gettitles():
	etree = etree.fromstring(page.content)
	tree = html.fromstring(page.content)
	titles = tree.xpath('//title/text()')
	return titles

#This confirms there is at least one job within search criteria
def verifyjobspresent(titles):
	if titles[2] == None:
		print ("No jobs found!")
		return 1
	else:
		return 0

#This verifies the amount of jobs is at least as many as the user searched for
def userinputisvalid():
	if len(titles) < userDefinedRange:
		return 1
	else:
		return 0

#This generates the map
def generatemap():
	py.plot(fig, filename='test mapbox')

#This gets latitude
def getlatitude():
	lat[x] = location.latitude

#This gets longitude
def getlongitude():
	lon[x] = location.longitude


#Main program logic
page = requests.get('https://stackoverflow.com/jobs/feed?location=bridgewater&range=50&distanceUnits=Miles')

etree = etree.fromstring(page.content)
tree = html.fromstring(page.content)

#Stores titles, links, and locations in a list
titles = tree.xpath('//title/text()')
links = etree.xpath('//item/link/text()')
locations = tree.xpath('//location/text()')
geolocator = Nominatim()

#Get user defined range
userDefinedRange = input("How many jobs would you like to list? ")

verifyjobspresent(titles)

while not userDefinedRange.isdigit():
	print ("Only integers are accepted!")
	userDefinedRange = input("Please input an integer: ")

userDefinedRange = int(userDefinedRange)

print ("\nFound " + str(len(titles) - 2) + " jobs on Stack Overflow. \n")

#Adjusts for bad starting data in returned titles list
if len(titles) <= userDefinedRange:
	userDefinedRange = len(titles) - 2

#Prints titles and links within range
for x in range(userDefinedRange):
	titleStr = str(titles[x+2])

	#Checks which OS is running
	if platform == "darwin":
		notify(titleStr)
		print(titleStr)
		print (links[x])
		#print (locations[x])
		print ("\n")

	else:
		print(titleStr)
		print (links[x])
		print ("\n")


print ("There were " + str(len(titles) - 2) + " total jobs found on Stack Overflow. \n")


#Init latitude and longitude lists
lat = [None] * userDefinedRange
lon = [None] * userDefinedRange

print ("Processing map data...\n")

#Populates latitude and longitude lists with data from location search
for x in range(userDefinedRange):
	location = geolocator.geocode(locations[x])
	lat[x] = location.latitude
	lon[x] = location.longitude


#Init data for map
data = Data([
	Scattermapbox(
		lat=lat,
		lon=lon,
		mode='markers',
		marker=Marker(size=15),
		text = ["1", "2", "3", "4", "5"],
	)
])

#Init layout for map
layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=41,
            lon=-74
        ),
        pitch=0,
        zoom=7.5
    ),
)

fig = dict(data=data, layout=layout)
generatemap()
