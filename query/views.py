import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import pokemon_fort_db

db = pokemon_fort_db.PokemonFortDB()

def index(request):
    data = request.GET
    west = float(data["west"])
    north = float(data["north"])
    east = float(data["east"])
    south = float(data["south"])
    forts = db.query_forts(west, north, east, south)

    return HttpResponse(json.dumps(forts))
