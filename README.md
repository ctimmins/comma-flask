## Overview
This flask application is backed by a geospatially indexed postgres/postgis database with two endpoints to query by 
bounding box the trips collected by Comma. 

### Installation
On OSX:
    
    `brew install postgresql && brew install postgis`
    create the db: `createdb -O postgres comma`
    to connect: `psql -U postgres -d comma`
    once in a psql shell: 
    `create extension postgis;`
    `create extension postgis_topology;`

### Import
1. create the tables `psql -U postgres -d comma -f ./static/scripts/trips.ddl`
2. import the data `python ./static/import.py <path to data directory>`
3. create the overview table `psql -U postgres -d comma -f ./static/scripts/trips_overview.ddl`

### Alternative Import
restore from the uploaded snapshot `bzip2 -d ./static/data/comma_export.bz2 && pg_restore -U postgres -d comma comma_export`        

There are two tables of importance:
*  `trips`
*  `trips_overview`

#### Trips Table
 * trip_id     
 * start_time  
 * end_time    
 * coord_index 
 * speed       
 * dist        
 * lat         
 * lng         
 * geom (spatially indexed point)
 
#### Trips Overview Table
It is all the points from trips compressed into a simplified geometry for showing the entire route.

 * trip_id   
 * pt_count  
 * avg_speed
 * route


## Service
You can run Flask's local server by executing the manager script:
`./manage.py runserver` will start a dev server locally on port 5000


### Endpoints

#### Get All Points by Bounding Box
` GET /api/v1/points/<min_lat>/<min_lng>/<max_lat>/<max_lng>[?limit=<limit>]`
queries the trips table for all the points and speed

#### Get Route Overviews by Bounding Box
` GET /api/v1/overview/<min_lat>/<min_lng>/<max_lat>/<max_lng>[?limit=<limit>]`
queries the trips_overview table to return routes by trip_id




