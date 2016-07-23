import psycopg2
import time

class PokemonFortDB(object):
    def __init__(self):
        self.conn = psycopg2.connect(host="pokemon-fort-dev.cafr6s1nfibs.us-west-2.rds.amazonaws.com", 
                                     port=5432, 
                                     user="pokemon_fort",
                                     password="pokemon_fort",
                                     database="pokemon_fort_dev")

    def add_fort(self, fortid, cellid, enabled, latitude, longitude, lure_expire=0, forttype=None, gymteam=None):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO fort_map (fortid, cellid, enabled, latitude, longitude, forttype, gymteam, lure_expire, last_update)" +  
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" +
                    " ON CONFLICT (fortid) DO UPDATE SET gymteam = EXCLUDED.gymteam, lure_expire = EXCLUDED.lure_expire, last_update = EXCLUDED.last_update;", 
            (fortid, cellid, enabled, latitude, longitude, forttype, gymteam, lure_expire, time.time()))

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
                    " ON CONFLICT (encounter_id) DO NOTHING;", 
            (encounter_id, expire, pokemon_id, latitude, longitude))


    def commit(self):
        self.conn.commit()

    def cell_exists(self, cellid):
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM fort_map WHERE cellid=%s", (str(cellid),))
        number = cur.fetchone()[0]
        return number > 0


    def query_forts(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, forttype, gymteam FROM fort_map WHERE longitude > %s and longitude < %s and latitude > %s and latitude < %s limit 200", 
                (west, east, south, north))
        rows = cur.fetchall()
        forts = []
        for row in rows:
            forts.append({ "latitude": row[0],
                              "longitude" : row[1],
                              "forttype" : row[2],
                              "gymteam" : row[3]
                            })
        return forts


