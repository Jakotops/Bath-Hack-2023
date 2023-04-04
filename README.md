# Bath-Hack-2023

This is the Bath Hack Repository for team 13

https://devpost.com/software/second-bus

# Second Bus - Bus Tracking App

## Inspiration

The current bus apps in Bath regularly show incorrect ETAs, which can cause frustration and lead to time being wasted waiting at a bus stop. Our app hopes to elevate this experience by using Google's API and existing datasets on bus timetables and locations.

## What it does

Our app provides functionality that tracks and presents statistics on the user's bus usage, such as time spent on buses, most frequent bus stops used, distance traveled on buses, etc. It displays up-to-date data on bus routes in the Bath area and live positions of buses on an interactive map. Users can register and log into the app. The app also gives the user insight into the next bus that will arrive at their stop, including occupied seats, ETA, and line number (e.g., U1, U2). When the user is riding on the bus, a "Journey Page" is shown to display ads and a live interactive map to show bus location. A virtual bus stop information board is included to show next arrivals and ETA.

All this is presented with an interactive map that displays all live positions of buses in the Bath region, a particular route as chosen by the user, and all the bus stops included along that route. The app calculates bus ETA and distance traveled using Google services, giving the user a trustworthy source to compare to bus timetables.

## How we built it

For the front-end, we used PyQt5 as a way to collect widgets in a stack and to allow navigation between objects. For the back-end, we used Python to interact with various APIs to access datasets and process specific data needed.

Datasets Used:
- Gov dataset that contains all up to date bus route data in Bath: https://data.bus-data.dft.gov.uk/timetable/dataset/5813/
- Real-time data about future arriving buses at any bus stop using https://www.transportapi.com/, including line, occupancy, and arrival time.
- Real-time bus locations within the Bath region using https://bustimes.org/ (abstracts from Gov website API).

## Challenges we ran into

- Bus stop markers from the folium library did not provide the functionality to show the estimated times when clicked, which threatened us to rebuild with a new library or include a JavaScript macro, which we were not fluent with. Our solution was to assign the coordinates to each marker's popup so the user can copy the coordinates into a text entry when they select a bus stop on the map to view the times.
- API data from the helper files needed to be displayed on the app to front-end. This was solved by using data structures such as arrays and dictionaries and by performing loops through the data so it can be saved to the table and labels.

## Accomplishments that we're proud of

Integrating data from multiple sources into one application and presenting it in an accessible fashion. Personal accomplishments on learning new technologies and working with APIs for the first time.

## What we learned

We learned how to utilize several APIs to update an app in real-time. We learned how to use different APIs effectively. How to build a GUI in Python using PyQt5. We learnt the limitations of some datasets provided.

## Built With

- Google Maps API
- PyQt5
- Python
- SQLAlchemy
- SQLite
- TransportAPI
