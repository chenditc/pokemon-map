import os
import json
import itertools

from django.shortcuts import render
from django.http import HttpResponse
import s2sphere
import boto3
import redis

import pokemon_fort_db

SQS_QUEUE_NAME = os.environ.get("SQS_QUEUE_NAME", "awseb-e-h66tqvpuym-stack-AWSEBWorkerQueue-1X04PKYR2KY9D")

db = pokemon_fort_db.PokemonFortDB()
work_queue = boto3.resource('sqs', region_name='us-west-2').get_queue_by_name(QueueName=SQS_QUEUE_NAME)

def refresh_cells(cell_ids):
    work_queue.send_message(MessageBody=json.dumps(cell_ids))

def refresh_fort(west, east, north, south):
    p1 = s2sphere.LatLng.from_degrees(north, west); 
    p2 = s2sphere.LatLng.from_degrees(south, east);
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    area = rect.area() * 1000 * 1000

    # If area is too large, don't return 
    if area < 0.85:
        cover = s2sphere.RegionCoverer()
        cover.max_cells = 200
        cover.max_level = 15
        cover.min_level = 15
        cells = cover.get_covering(rect)

        cell_ids = [ cell.id() for cell in cells ]
        refresh_cells(cell_ids)

def refresh_pokemon(west, east, north, south):
    p1 = s2sphere.LatLng.from_degrees(north, west); 
    p2 = s2sphere.LatLng.from_degrees(south, east);
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    area = rect.area() * 1000 * 1000

    # If area is too large, return nothing
    if area < 0.85:
        cover = s2sphere.RegionCoverer()
        cover.max_cells = 200
        cover.max_level = 15
        cover.min_level = 16
        cells = cover.get_covering(rect)

        cell_ids = [ cell.id() for cell in cells ]
        refresh_cells(cell_ids)




def fort(request):
    data = request.GET
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_fort(west, east, north, south)
    forts = db.query_forts(west, north, east, south)

    return HttpResponse(json.dumps(forts))

def pokemon(request):
    data = request.GET
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_pokemon(west, east, north, south)

    pokemons = db.query_pokemon(west, north, east, south)

    return HttpResponse(json.dumps(pokemons))

