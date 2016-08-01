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

def parse_request(request):
    data = request.GET
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])
    return { "west": west,
             "north" : north,
             "east" : east,
             "south" : south }

def refresh_cells(request):
    work_queue.send_message(MessageBody=json.dumps(request))

def refresh_fort(request):
    request["target"] = "fort"
    refresh_cells(request)

def refresh_pokemon(request):
    request["target"] = "pokemon"
    refresh_cells(request)

def fort(request):
    data = parse_request(request)
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_fort(data)
    forts = db.query_forts(west, north, east, south)

    return HttpResponse(json.dumps(forts))

def pokestop(request):
    data = parse_request(request)
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_fort(data)
    pokestops = db.query_pokestop(west, north, east, south)

    return HttpResponse(json.dumps(pokestops))

def gym(request):
    data = parse_request(request)
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_fort(data)
    gyms = db.query_gym(west, north, east, south)

    return HttpResponse(json.dumps(gyms))


def pokemon(request):
    data = parse_request(request)
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])

    refresh_pokemon(data)

    pokemons = db.query_pokemon(west, north, east, south)

    return HttpResponse(json.dumps(pokemons))
