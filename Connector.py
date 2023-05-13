import sqlite3

class Connector:
    def __init__(self, source):
        self.source = source
    
    #TODO abstraction
    def query_SQLite(self, query):
        con = sqlite3.connect(f"data/{self.source}.db")
        cur = con.cursor()
        data = []
        if query:
            try:
                res = cur.execute(query)
                headers = list(map(lambda attr : attr[0], cur.description))
                data = [{header:row[i] for i, header in enumerate(headers)} for row in cur]
            except:
                data = [{"question unclear": 0}]
        con.close()
        return data
    