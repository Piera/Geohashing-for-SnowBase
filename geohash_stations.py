import model
import geohash
import psycopg2
import heapq
import json
from haversine import distance
from sqlalchemy import Table, Column, Float, Integer, Boolean, String, MetaData, ForeignKey, desc, select
from model import session as dbsession

def see_all():
	all_stations = {}
	ordered_sta = []
	stations = dbsession.query(model.Station).all()
	for station in stations:
		geohashed_station = geohash.encode(station.latitude, station.longitude)
		all_stations[geohashed_station] = station.id
	ordered_loc_list = sorted(all_stations)
	print ordered_loc_list
	return ordered_loc_list

def nearest_neighborhoods():
	reference_lat = 46.9153
	reference_long = -121.6422
	reference_location = geohash.encode(reference_lat, reference_long)
	location_box = geohash.expand(reference_location[:3])
	neighborhoods = []
	for loc in location_box:
		geohash_str = loc + '%'
		neighbor = dbsession.query(model.Station_Geohash).\
			select_from(model.Station_Geohash).\
			filter(model.Station_Geohash.geohash_loc.ilike(geohash_str)).\
			all()
		neighborhoods = neighborhoods + neighbor
	print neighborhoods

	neighbor_data = []
	for loc in neighborhoods:
		try: 
			snow = dbsession.query(model.Snow_Data).filter(model.Snow_Data.station_id == loc.station_id).all()
			neighbor_data.append(loc.geohash_loc)
		except IndexError:
			continue
	print neighbor_data[-10:]

def nearby_geohash_list():
	data_point = 'c23dgdfyrujq'
	m = dbsession.query(model.Station_Geohash).filter(model.Station_Geohash.geohash_loc == data_point).all()
	for i in m:
		print i.geohash_loc
		i.nearby = []
		print i.nearby
		for o in range(1,len(i.geohash_loc)):
		  for c in geohash.expand(i.geohash_loc[2:o]):
		    i.nearby.append(c)
	print i.nearby

def lookup():
	"""Calculate ten closest stations from input latitude and longitude, return data for ten closest stations as a JSON object."""

	# Geohash encode the input, then determine the expanded neighborhood based on expanded geohash
	reference_lat = 46.9153
	reference_long = -121.6422
	reference_location = geohash.encode(reference_lat, reference_long)
	location_box = geohash.expand(reference_location[:3])
	neighborhoods = []
	for place in location_box:
		geohash_str = place + '%'
		neighbor = dbsession.query(model.Station_Geohash).\
			select_from(model.Station_Geohash).\
			filter(model.Station_Geohash.geohash_loc.ilike(geohash_str)).\
			all()
		neighborhoods = neighborhoods + neighbor
	dist_list = []
	# For all of the stations found in neighborhoods, check for data and snow. 
	# If there is data and snow for a given station, add it to the list
	for location in neighborhoods:
		try: 
			station = dbsession.query(model.Station).filter(model.Station.id == location.station_id).one()
			snow = station.snow_data[-1]
			origin = float(reference_lat), float(reference_long)
			destination = float(station.latitude), float(station.longitude)
			kms = int(distance(origin, destination))
			mi = int(0.621371*kms)
			if snow.depth != None and snow.depth > 0:
				if snow.water_equiv != None and snow.water_equiv != 0:
					density = (int((snow.water_equiv / snow.depth) * 100))
					if density > 100:
							density = 100
				else: 
					density = "No Data" 
				heapq.heappush(dist_list, (mi, station.id))
			else:
				continue
		except IndexError:
			continue
	# Return the 10 closest stations, their distances away in miles (converted from kms)
	#  and basic telemetry data for that station

	closest_sta = [heapq.heappop(dist_list) for i in range(10)]
	responses_list = []
	for station in closest_sta:
		print station[0], station[1]
		mi = station[0]
		station = dbsession.query(model.Station).filter(model.Station.id == station[1]).one()
		responses_list.append({'dist':mi, 'text-code':station.id, 'id':station.given_id, 'ele':station.elevation,\
				'lat':station.latitude, 'lng':station.longitude, 'name':station.name, 'depth':snow.depth,\
				'depth_change':snow.depth_change, 'density':density, 'date':snow.date.strftime("%m/%d/%y %H:%M")})

	time_stamps = [x['date'] for x in responses_list]
	time_stamp = max(time_stamps)
	response = json.dumps({"closest": responses_list, "time_stamp":time_stamp})

	print response
	return response



if __name__ == "__main__":
    # see_all()
	# nearest_neighborhoods()
	# nearby_geohash_list()
	lookup()


