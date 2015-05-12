Jasper-Google-Calendar
======================

Jasper Google Calendar Module

Written By: Marc Poul Joseph Laventure

##Steps to install Google Calendar

* Install/run the following in your home directory
```
sudo pip install httplib2
sudo pip install --upgrade google-api-python-client
sudo easy_install --upgrade python-gflags
```
* run the following commands in order:
```
git clone https://github.com/marclave/Jasper-Google-Calendar.git
cp Software-Projects/JasperCalendar/Calendar.py <path to ..client/jasper/modules>
```
* Login to [Google developer Console](https://console.developers.google.com/project) and complete the following
```
Select a project.
In the sidebar on the left, select APIs & auth. In the list of APIs, make sure the status is ON for the Google Calendar API.
In the sidebar on the left, select Credentials.
Get Client ID and Client Secret (Save for later)
```
* Open Calendar.py and add Client ID and Client secret to appropriate variables (Will be updated later, for based on API version)
* Run the following commnads
```
cd ../jasper/client/
python modules/Calendar.py --noauth_local_webserver
```
* Go to website displayed from script 
* Add the following to __init.py
```
from modules import Calendar
```
##Congrats, JASPER Google Calendar is now installed and ready for use; here are some examples:
```
YOU: Add Calendar event
JASPER: What would you like to add?
YOU: Movie with erin Friday at 5 pm
JASPER: Added event Movie with erin on June 06 at 5:00 pm
JASPER: Is this what you wanted?
YOU: Yes
JASPER: Okay, I added it to your calendar
YOU: Do I have any Calendar events tomorrow
JASPER: Dinner with erin at 9:00 pm
YOU: Do I have any Calendar Events Today
JASPER: Dinner with erin at 6:00 pm
```

