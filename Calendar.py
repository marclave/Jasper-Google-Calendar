import httplib2
import sys
import datetime
import re
import gflags

from client.app_utils import getTimezone
from dateutil import tz
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.tools import *


# Written by Marc Poul Joseph Laventure

FLAGS = gflags.FLAGS
WORDS = [ "Calendar", "Events", "Check", "My" ]
client_id = 'xxxxxxxx.apps.googleusercontent.com'
client_secret = 'xxxxxxxxxxxxxx'

monthDict = {'January': '01', 
		'February': '02', 
		'March': '03', 
		'April': '04', 
		'May': '05', 
		'June': '06', 
		'July': '07', 
		'August': '08', 
		'September': '09', 
		'October': '10', 
		'November': '11', 
	    'December': '12'}


# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/calendar'

if bool(re.search('--noauth_local_webserver', str(sys.argv), re.IGNORECASE)):
	argv = FLAGS(sys.argv[1])

def addEvent(profile, mic):

	while True:
		try:
			mic.say("What would you like to add?")
			eventData = mic.activeListen()
			createdEvent = service.events().quickAdd(calendarId='primary', text=eventData).execute()
			eventRawStartTime = createdEvent['start']
			
			m = re.search('([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})', str(eventRawStartTime))
			eventDateYear = str(m.group(1))
			eventDateMonth = str(m.group(2))
			eventDateDay = str(m.group(3))
			eventTimeHour = str(m.group(4))
			eventTimeMinute =  str(m.group(5))
			appendingTime = "am"

			if len(eventTimeMinute) == 1:
				eventTimeMinute = eventTimeMinute + "0"

			eventTimeHour = int(eventTimeHour)

			if ((eventTimeHour - 12) > 0 ):
					eventTimeHour = eventTimeHour - 12
					appendingTime = "pm"
		
			dictKeys = [ key for key, val in monthDict.items() if val==eventDateMonth ]
			eventDateMonth = dictKeys[0]
			mic.say("Added event " + createdEvent['summary'] + " on " + str(eventDateMonth) + " " + str(eventDateDay) + " at " + str(eventTimeHour) + ":" + str(eventTimeMinute) + " " + appendingTime)
			mic.say("Is this what you wanted?")
			userResponse = mic.activeListen()
			
			if bool(re.search('Yes', userResponse, re.IGNORECASE)):
				mic.say("Okay, I added it to your calendar")
				return
	
			service.events().delete(calendarId='primary', eventId=createdEvent['id']).execute()

		except KeyError:

			mic.say("Could not add event to your calender; check if internet issue.")
			mic.say("Would you like to attempt again?")
			responseRedo = mic.activeListen()

			if bool(re.search('No', responseRedo, re.IGNORECASE)):
				return

def getEventsToday(profile, mic):

	tz = getTimezone(profile)

	# Get Present Start Time and End Time in RFC3339 Format
	d = datetime.datetime.now(tz=tz)
	utcString = d.isoformat()	
	m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
	utcString = str(m.group(0))
	todayStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
	todayEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString
	page_token = None
	
	while True:

		# Gets events from primary calender from each page in present day boundaries
		events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=todayStartTime, timeMax=todayEndTime).execute() 
		
		if(len(events['items']) == 0):
			mic.say("You have no events scheduled for today")
			return

		for event in events['items']:

			try:
				eventTitle = event['summary']
				eventTitle = str(eventTitle)
				eventRawStartTime = event['start']
				eventRawStartTime = eventRawStartTime['dateTime'].split("T")
				temp = eventRawStartTime[1]
				startHour, startMinute, temp = temp.split(":", 2)
				startHour = int(startHour)
				appendingTime = "am"

				if ((startHour - 12) > 0 ):
					startHour = startHour - 12
					appendingTime = "pm"

				startMinute = str(startMinute)
				startHour = str(startHour)
				mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime) # This will be mic.say

			except KeyError, e:
				mic.say("Check Calender that you added it correctly")
			
		page_token = events.get('nextPageToken')

		if not page_token:
			return


def getEventsTomorrow(profile, mic):

	# Time Delta function for adding one day 
	
	one_day = datetime.timedelta(days=1)
	tz = getTimezone(profile)
	
	# Gets tomorrows Start and End Time in RFC3339 Format

	d = datetime.datetime.now(tz=tz) + one_day
	utcString = d.isoformat()
	m = re.search('((\+|\-)[0-9]{2}\:[0-9]{2})', str(utcString))
	utcString = m.group(0)
	tomorrowStartTime = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utcString
	tomorrowEndTime = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utcString

	page_token = None

	while True:

		# Gets events from primary calender from each page in tomorrow day boundaries

		events = service.events().list(calendarId='primary', pageToken=page_token, timeMin=tomorrowStartTime, timeMax=tomorrowEndTime).execute()
		if(len(events['items']) == 0):
			mic.say("You have no events scheduled Tomorrow")
			return
	
		for event in events['items']:
			
			try:
				eventTitle = event['summary']
				eventTitle = str(eventTitle)
				eventRawStartTime = event['start']
				eventRawStartTime = eventRawStartTime['dateTime'].split("T")
				temp = eventRawStartTime[1]
				startHour, startMinute, temp = temp.split(":", 2)
				startHour = int(startHour)
				appendingTime = "am"

				if ((startHour - 12) > 0 ):
					startHour = startHour - 12
					appendingTime = "pm"

				startMinute = str(startMinute)
				startHour = str(startHour)
				mic.say(eventTitle + " at " + startHour + ":" + startMinute + " " + appendingTime) # This will be mic.say

			except KeyError, e:
				mic.say("Check Calender that you added it correctly")
			
		page_token = events.get('nextPageToken')
		
		if not page_token:
			return




# Create a flow object. This object holds the client_id, client_secret, and
# scope. It assists with OAuth 2.0 steps to get user authorization and
# credentials.

flow = OAuth2WebServerFlow(client_id, client_secret, scope)


# Create a Storage object. This object holds the credentials that your
# application needs to authorize access to the user's data. The name of the
# credentials file is provided. If the file does not exist, it is
# created. This object can only hold credentials for a single user, so
# as-written, this script can only handle a single user.
storage = Storage('credentials.dat')

# The get() function returns the credentials for the Storage object. If no
# credentials were found, None is returned.
credentials = storage.get()

# If no credentials are found or the credentials are invalid due to
# expiration, new credentials need to be obtained from the authorization
# server. The oauth2client.tools.run() function attempts to open an
# authorization server page in your default web browser. The server
# asks the user to grant your application access to the user's data.
# If the user grants access, the run() function returns new credentials.
# The new credentials are also stored in the supplied Storage object,
# which updates the credentials.dat file.
if credentials is None or credentials.invalid:
	credentials = run(flow, storage)

# Create an httplib2.Http object to handle our HTTP requests, and authorize it
# using the credentials.authorize() function.
http = httplib2.Http()

http = credentials.authorize(http)

# The apiclient.discovery.build() function returns an instance of an API service
# object can be used to make API calls. The object is constructed with
# methods specific to the calendar API. The arguments provided are:
#   name of the API ('calendar')
#   version of the API you are using ('v3')
#   authorized httplib2.Http() object that can be used for API calls
service = build('calendar', 'v3', http=http)

def handle(text, mic, profile):
		
	if bool(re.search('Add', text, re.IGNORECASE)):
		addEvent(profile,mic)

	if bool(re.search('Today', text, re.IGNORECASE)):
		getEventsToday(profile,mic)

	if bool(re.search('Tomorrow', text, re.IGNORECASE)):
		getEventsTomorrow(profile,mic)


def isValid(text):
	return bool(re.search(r'\bCalendar\b', text, re.IGNORECASE))
