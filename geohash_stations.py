import model
import geohash
import psycopg2
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



if __name__ == "__main__":
    # see_all()
	nearest_neighborhoods()
	# nearby_geohash_list()


