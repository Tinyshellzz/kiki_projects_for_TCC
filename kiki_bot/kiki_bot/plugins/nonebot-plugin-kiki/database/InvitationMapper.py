from .db_config import *
import json
from ..utils import tools

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS invitations (
        id BigInt UNSIGNED,
        inviter BigInt UNSIGNED,
        PRIMARY KEY (id),
        KEY (inviter)
    ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class InvitationMapper:
    def insert(id: int, inviter: int):
        with connect() as db:
            with db.cursor() as c:
                c.execute("""INSERT INTO invitations
                    (id, inviter)
                    values
                    (%s, %s)""", (id, inviter))
                db.commit()
        
        return True
    
    def get_times(inviter: int):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) FROM invitations WHERE inviter=%s", id)
                res = c.fetchall()
        
        return res[0][0]
    
    def exists_id(id: int):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM invitations WHERE id=%s", id)
                res = c.fetchall()
        
        return len(res[0]) > 0
    
    def exists_inviter(inviter: int):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM invitations WHERE inviter=%s", id)
                res = c.fetchall()
        
        return len(res[0]) > 0
    
    def get_inviter(id: int):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM invitations WHERE id=%s", id)
                res = c.fetchall()
        
        if len(res) == 0: return None
        return res[0][1]
    
    def get_relations(id: int):
        inviter = None
        inviter = InvitationMapper.get_inviter(id)
        if inviter == None:
            if InvitationMapper.exists_inviter(id):
                return None
            inviter = id

        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM invitations WHERE inviter=%s", id)
                res = c.fetchall()

        ret = [int(inviter)]
        for r in res:
            ret.append(int(r[0]))

        return ret
