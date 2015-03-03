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
		# all_stations[station.given_id] = geohashed_station
		all_stations[geohashed_station] = station.id
		# sorted_stations = sorted(all_stations, key=all_stations.get, reverse=True)
	ordered_loc_list = sorted(all_stations)
	print ordered_loc_list
	return ordered_loc_list

def nearest_neighbors():
	reference_lat = 46.9153
	reference_long = -121.6422
	reference_location = geohash.encode(reference_lat, reference_long)
	print reference_location
	geohash_str = reference_location[:3] + '%'
	print geohash_str 
	# ten_neighbors = dbsession.query(model.Station_Geohash).filter(model.Station_Geohash.geohash_loc.ilike("c2%")).limit(10)
	ten_neighbors = dbsession.query(model.Station_Geohash).\
		select_from(model.Station_Geohash).\
		filter(model.Station_Geohash.geohash_loc.ilike(geohash_str)).\
		limit(10).all()
	for item in ten_neighbors:
		print item.id, item.station_id, item.geohash_loc

if __name__ == "__main__":
    see_all()
    # ordered_loc_list = see_all()
    nearest_neighbors()