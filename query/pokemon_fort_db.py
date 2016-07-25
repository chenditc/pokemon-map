import time

import psycopg2
import s2sphere

class PokemonFortDB(object):
    def __init__(self):
        self.conn = psycopg2.connect(host="pokemon-fort-dev.cafr6s1nfibs.us-west-2.rds.amazonaws.com", 
                                     port=5432, 
                                     user="pokemon_fort",
                                     password="pokemon_fort",
                                     database="pokemon_fort_dev")

############################################################################################################
# Web API 
############################################################################################################

    def query_forts(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, forttype, lure_expire, gymteam FROM fort_map " + 
                    "WHERE longitude > %s " + 
                        "and longitude < %s " + 
                        "and latitude > %s " + 
                        "and latitude < %s " +
                     "ORDER BY lure_expire DESC, fortid DESC limit 200",
                (west, east, south, north))
        rows = cur.fetchall()
        forts = []
        for row in rows:
            forts.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "forttype" : row[2],
                              "lure" : row[3],
                              "gymteam" : row[4]
                            })
        return forts

    def query_pokemon(self, west, north, east, south):
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, pokemon_id, expire FROM pokemon_map " + 
                    "WHERE longitude > %s " + 
                        "and longitude < %s " + 
                        "and latitude > %s " + 
                        "and latitude < %s " +
                        "AND expire > %s " + 
                     "ORDER BY encounter_id DESC limit 200",
                (west, east, south, north, now))
        rows = cur.fetchall()
        pokemons = []
        for row in rows:
            pokemons.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "pokemon_id" : row[2],
                              "expire" : row[3]
                            })
        return pokemons
