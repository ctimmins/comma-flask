import os, sys, json
from shapely.geometry import Point
import psycopg2

if __name__ == '__main__':
    dirname = sys.argv[1]
    print("dirname: %s" % dirname)
    conn = psycopg2.connect("dbname=comma user=ctimmins")
    cur = conn.cursor()

    for f in os.listdir(dirname):
        file_path = os.path.abspath(dirname + '/' + f)
        print "file path: %s" % file_path
        trip = json.load(open(file_path, 'r'))
        start_time = trip['start_time']
        end_time = trip['end_time']
        coords = trip['coords']
        for coord in coords:
            lat, lng = coord['lat'], coord['lng']
            dist, speed = coord['dist'], coord['speed']
            index = coord['index']
            pt = Point(lng, lat)
            cur.execute("""
                INSERT INTO trips (trip_id, start_time, end_time, coord_index, speed, dist, lat, lng, geom)
                VALUES ('%s', '%s', '%s', %s, %s, %s, %s, %s, st_setsrid(st_geomfromtext('%s'), 4326))
            """ % (f, start_time, end_time, index, speed, dist, lat, lng, pt))


    conn.commit()
    conn.close()
