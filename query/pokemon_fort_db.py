import time
import os

import psycopg2
import s2sphere

class PokemonFortDB(object):
    def __init__(self):
        rds_host = os.environ.get("RDS_HOST","pokemon-fort-dev.cafr6s1nfibs.us-west-2.rds.amazonaws.com" )
        rds_user = os.environ.get("RDS_USER", "pokemon_fort")
        rds_password = os.environ.get("RDS_PASSWORD", "pokemon_fort")
        rds_database = os.environ.get("RDS_DATABASE", "pokemon_fort_dev")

        self.conn = psycopg2.connect(host=rds_host, 
                                     port=5432, 
                                     user=rds_user,
                                     password=rds_password,
                                     database=rds_database)

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

    def query_pokestop(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, lure_expire FROM fort_map " + 
                    "WHERE longitude > %s " + 
                        "and longitude < %s " + 
                        "and latitude > %s " + 
                        "and latitude < %s " +
                        "and forttype = 1 " +
                     "ORDER BY lure_expire DESC, fortid DESC limit 200",
                (west, east, south, north))
        rows = cur.fetchall()
        forts = []
        for row in rows:
            forts.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "lure" : row[2],
                            })
        return forts

    def query_gym(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, gymteam FROM fort_map " + 
                    "WHERE longitude > %s " + 
                        "and longitude < %s " + 
                        "and latitude > %s " + 
                        "and latitude < %s " +
                        "and gymteam > 0 " +
                     "ORDER BY fortid DESC limit 200",
                (west, east, south, north))
        rows = cur.fetchall()
        forts = []
        for row in rows:
            forts.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "gymteam" : row[2],
                            })
        return forts


    def query_pokemon(self, west, north, east, south):
        now = time.time() * 1000
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
