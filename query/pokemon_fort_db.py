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
# Crawl API 
############################################################################################################

    def add_fort(self, fortid, cellid, enabled, latitude, longitude, lure_expire=0, forttype=None, gymteam=None):
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO fort_map (fortid, cellid, enabled, latitude, longitude, forttype, gymteam, lure_expire, last_update)" +  
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" +
                    " ON CONFLICT (fortid) DO UPDATE SET gymteam = EXCLUDED.gymteam, lure_expire = EXCLUDED.lure_expire, last_update = EXCLUDED.last_update;", 
            (fortid, cellid, enabled, latitude, longitude, forttype, gymteam, lure_expire, now))

    def mark_search(self, cellid):
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO map_search_record (timestamp, cellid) " + 
                    " VALUES (%s, %s) ON CONFLICT (cellid) DO NOTHING", (now, cellid)) 
        self.conn.commit()


    def add_spawn_points(self, cellid, spawn_points):
        now = time.time()
        # Check if this cell already exists
        cur = self.conn.cursor()
        cur.execute("SELECT count(cellid) FROM spawn_point_map WHERE cellid=%s limit 1", (str(cellid),))
        count = cur.fetchone()[0]
        if count != 0:
            return

        for point in spawn_points:
            latitude = point["latitude"]
            longitude = point["longitude"]
            cur = self.conn.cursor()
            cur.execute("INSERT INTO spawn_point_map (cellid, latitude, longitude, last_check)" +  
                        " VALUES (%s, %s, %s, %s)",
                (cellid, latitude, longitude, now))
        self.conn.commit()

    def get_first_spawn_point(self, cellid):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude FROM spawn_point_map WHERE cellid=%s limit 1", (str(cellid),))
        records = cur.fetchall()
        if len(records) == 0:
            return None
        else:
            return (records[0][0], records[0][1], 0)


    def add_pokemon(self, encounter_id, expire, pokemon_id, latitude, longitude):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO pokemon_map (encounter_id, expire, pokemon_id, latitude, longitude)" +  
                    " VALUES (%s, %s, %s, %s, %s)" +
                    " ON CONFLICT (encounter_id, expire, pokemon_id, latitude, longitude) DO NOTHING",
            (encounter_id, expire, pokemon_id, latitude, longitude))
        self.conn.commit()

    def get_search_cellids(self, limit=200):
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT(map_visit_record.cellid) " +  
                    " FROM map_visit_record, map_search_record" + 
                    " WHERE map_visit_record.timestamp > %s" +  # Visited last hour
                        " AND map_search_record.timestamp < %s" +   # Didn't update last minute
                        " AND map_search_record.cellid = map_visit_record.cellid " +
                    " ORDER BY map_visit_record.timestamp DESC" + 
                    " LIMIT %s", (now - 3600, now - 60, limit))
        rows = cur.fetchall()
        result = [ int(row[0]) for row in rows ]
        return result


############################################################################################################
# Web API 
############################################################################################################



    def cell_exists(self, cellid):
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM fort_map WHERE cellid=%s", (str(cellid),))
        number = cur.fetchone()[0]
        return number > 0


    def query_forts(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, forttype, lure_expire, gymteam FROM fort_map " + 
                    "WHERE longitude > %s " + 
                        "and longitude < %s " + 
                        "and latitude > %s " + 
                        "and latitude < %s " +
                     "ORDER BY lure_expire, fortid limit 200",
                (west, east, south, north))
        rows = cur.fetchall()
        forts = []
        for row in rows:
            forts.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "forttype" : row[2],
                              "lure_expire" : row[3],
                              "gymteam" : row[4]
                            })
        return forts

############################################################################################################
# utility
############################################################################################################


    def commit(self):
        self.conn.commit()
