import json
import itertools

from django.shortcuts import render
from django.http import HttpResponse
import s2sphere
import boto3
import redis

import pokemon_fort_db

db = pokemon_fort_db.PokemonFortDB()
work_queue = boto3.resource('sqs').get_queue_by_name(QueueName='awseb-e-h66tqvpuym-stack-AWSEBWorkerQueue-1X04PKYR2KY9D')
redis_client = redis.StrictRedis(host='mypokemon-io.qha7wz.ng.0001.usw2.cache.amazonaws.com', port=6379, db=0)

def refresh_cells(cell_ids):
    work_queue.send_message(MessageBody=json.dumps(cell_ids))

def index(request):
    data = request.GET
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    p1 = s2sphere.LatLng.from_degrees(north, west); 
    p2 = s2sphere.LatLng.from_degrees(south, east);
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    area = rect.area() * 1000 * 1000

    # If area is too large, return nothing
    if area < 0.85:
        cover = s2sphere.RegionCoverer()
        cover.max_cells = 200
        cover.max_level = 15
        cover.min_level = 15
        cells = cover.get_covering(rect)

        cell_ids = [ cell.id() for cell in cells ]
        #cell_fort_key = [ "fort.{0}".format(cell_id) for cell_id in cell_ids ] 
        #cell_fort_jsons = redis_client.mget(cell_fort_key)

        ## Update expired forts
        #expired_cell_ids = []
        #forts = []
        #for i in range(len(cell_fort_jsons)):
        #    if cell_fort_jsons[i] == None:
        #        expired_cell_ids.append(cell_ids[i])
        #    else:
        #        forts += json.loads(cell_fort_jsons[i])
        refresh_cells(cell_ids)

    forts = db.query_forts(west, north, east, south)

    return HttpResponse(json.dumps(forts))
