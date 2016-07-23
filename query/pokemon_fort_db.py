import psycopg2

class PokemonFortDB(object):
    def __init__(self):
        self.conn = psycopg2.connect(host="pokemon-fort-dev.cafr6s1nfibs.us-west-2.rds.amazonaws.com", 
                                     port=5432, 
                                     user="pokemon_fort",
                                     password="pokemon_fort",
                                     database="pokemon_fort_dev")

    def add_fort(self, fortid, cellid, enabled, latitude, longitude, forttype=None, gymteam=None):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO fort_map (fortid, cellid, enabled, latitude, longitude, forttype, gymteam)" +  
                    " VALUES (%s, %s, %s, %s, %s, %s, %s)", 
            (fortid, cellid, enabled, latitude, longitude, forttype, gymteam))

    def commit(self):
        self.conn.commit()

    def cell_exists(self, cellid):
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM fort_map WHERE cellid=%s", (str(cellid),))
        number = cur.fetchone()[0]
        return number > 0

    def query_forts(self, west, north, east, south):
        cur = self.conn.cursor()
        cur.execute("SELECT latitude, longitude, forttype, gymteam FROM fort_map WHERE longitude > %s and longitude < %s and latitude > %s and latitude < %s limit 1000", 
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

