
import MySQLdb

class Db(object):
    def __init__(self, host, dbname, user, pw):
        self.db = MySQLdb.connect(host=host, db=dbname, user=user, passwd=pw)

    def create_tables(self):
        stmts = [
            """create table if not exists url (url varchar(255), inserted_at bigint, 
               obj varchar(64), index(inserted_at))"""
        ]
        try:
            cur = self.db.cursor()
            for s in stmts:
                cur.execute(s)
            self.db.commit()                
        finally:
            cur.close()
            
    def insert_url(self, url, obj, inserted_at):
        args = (url, obj, inserted_at)
        try:
            cur = self.db.cursor()
            cur.execute("insert into url (url, obj, inserted_at) values (%s, %s, %s)", args)
            self.db.commit()                
        finally:
            cur.close()
            
    def get_object_counts(self):
        arr = []
        try:
            cur = self.db.cursor()
            cur.execute("select obj, count(*) from url group by obj order by obj")
            row = cur.fetchone()
            while row:
                arr.append({"object": row[0], "count": row[1]})
                row = cur.fetchone()
        finally:
            cur.close()        
        return arr

    def get_urls_by_obj(self, obj, min_date, limit):
        arr = []
        try:
            cur = self.db.cursor()
            cur.execute("select url, inserted_at from url where obj=%s and inserted_at >= %s order by inserted_at limit %s", (obj, min_date, limit))
            row = cur.fetchone()
            while row:
                arr.append({"url": row[0], "inserted_at": row[1]})
                row = cur.fetchone()
        finally:
            cur.close()        
        return arr
        
