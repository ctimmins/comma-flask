from flask import jsonify, request
from shapely import wkb, wkt, geometry
from geojson import Feature, FeatureCollection, Polygon, MultiPoint
import logging

from . import api
from .. import db, get_db_conn


@api.route('/points/<string:lat>/<string:lng>/<string:radius>', methods=['GET'])
def get_points_by_radius(lat, lng, radius):
    cur = get_db_conn().cursor()
    sql = "SELECT count(*) FROM trips"
    cur.execute(sql)

    return jsonify({"sql": sql, "result": cur.fetchone()[0]})


@api.route('/overview/<string:lat>/<string:lng>/<string:radius>', methods=['GET'])
def get_overview_by_radius(lat, lng, radius):
    cur = get_db_conn().cursor()
    sql = "SELECT count(*) FROM trips"
    cur.execute(sql)

    return jsonify({"sql": sql, "result": cur.fetchone()[0]})


@api.route('/points/<string:min_lat>/<string:min_lng>/<string:max_lat>/<string:max_lng>', methods=['GET'])
def get_points_by_bbox(min_lat, min_lng, max_lat, max_lng):
    coords = clean_coords(min_lat, min_lng, max_lat, max_lng)
    conn = get_db_conn()
    try:
        limit = request.args.get('limit', 100)
        offset = request.args.get('offset', 0)
        with conn.cursor() as cur:
            sql = """
            select trip_id, start_time, end_time, coord_index, speed, dist, lat, lng, st_astext(geom) as wkt 
            from trips 
            where st_intersects(geom, st_makeenvelope(%s, %s, %s, %s, 4326))
            order by trip_id, coord_index
            limit %s
        """ % (coords['min_lng'], coords['min_lat'], coords['max_lng'], coords['max_lat'], limit)
            cur.execute(sql)
            res = [
                {"trip_id": r[0],
                 "start_time": r[1],
                 "end_time": r[2],
                 "index": r[3],
                 "speed": r[4],
                 "dist": r[5],
                 "lat": r[6],
                 "lng": r[7],
                 "geoJSON": Feature(geometry=wkt.loads(r[8]))} for r in cur]
    except Exception as e:
        logging.error(e)
        conn.rollback()
        response = jsonify({'message': e[0], 'code': '400'})
        response.status_code = 400
        return response
    return jsonify({'data': res})


@api.route('/overview/<string:min_lat>/<string:min_lng>/<string:max_lat>/<string:max_lng>', methods=['GET'])
def get_overview_by_bbox(min_lat, min_lng, max_lat, max_lng):
    coords = clean_coords(min_lat, min_lng, max_lat, max_lng)
    conn = get_db_conn()
    try:
        limit = request.args.get('limit', 100)
        offset = request.args.get('offset', 0)
        with conn.cursor() as cur:
            sql = """
            select trip_id, avg_speed, st_astext(route) as wkt
            from trips_overview 
            where st_intersects(route, st_makeenvelope(%s, %s, %s, %s, 4326))
            limit %s
        """ % (coords['min_lng'], coords['min_lat'], coords['max_lng'], coords['max_lat'], limit)
            cur.execute(sql)
            res = [{"trip_id": r[0], "avg_speed": r[1], "geoJSON": Feature(geometry=wkt.loads(r[2]))} for r in cur]
    except Exception as e:
        logging.error(e)
        conn.rollback()
        response = jsonify({'message': e[0], 'code': '400'})
        response.status_code = 400
        return response
    return jsonify({'data': res})


@api.errorhandler(ValueError)
def handle_invalid_usage(error):
    logging.info(error)
    response = jsonify({'message': error[0], 'code': '400'})
    response.status_code = 400
    return response

def clean_coords(min_lat, min_lng, max_lat, max_lng):
    validate_coord(min_lat, min_lng)
    validate_coord(max_lat, max_lng)
    return {
        "min_lat": min(float(min_lat), float(max_lat)),
        "min_lng": min(float(min_lng), float(max_lng)),
        "max_lat": max(float(min_lat), float(max_lat)),
        "max_lng": max(float(min_lng), float(max_lng)),
    }


def validate_coord(lat, lng):

    try:
        lat = float(lat)
        if (lat == 0 or lat <= -90 or lat >= 90):
            raise ValueError('Invalid Latitude')
    except Exception:
        raise ValueError('Invalid Latitude')

    try:
        lng = float(lng)
        if (lng == 0 or lng <= -180 or lng >= 180):
            raise ValueError('Invalid Longitude')
    except Exception:
        raise ValueError('Invalid Longitude')

