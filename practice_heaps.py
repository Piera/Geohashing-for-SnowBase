# Get distance from input to station in neighborhood
# Add distance and station to heap
# Remove 10 lowest values
import heapq

station_distances = {9:'ABC', 3:'DEF', 45:'JKL', 46:'XYZ', 22:'LMN', 10:'MNO', 23:'PQR', 8:'WXY', 90:'QRS', 6:'PAR', 19:'API', 98:'GRN'}

h = []
for key,value in station_distances.iteritems():
	heapq.heappush(h, (key,value))

print [heapq.heappop(h) for i in range(10)]



	