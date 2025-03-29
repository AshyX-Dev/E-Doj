import sqlite3
import json
from interface import Includes

class Manager(object):
    def __init__(self):
        self.dbs = sqlite3.connect("doj_users.db", check_same_thread=False)
        self.setup()

    def setup(self):
        self.dbs.execute(
            """CREATE TABLE IF NOT EXISTS dusers ( uid INTEGER PRIMARY TEXT, includes TEXT )"""
        )

    async def getUser(self, uid: int):
        users = self.dbs.execute("SELECT * FROM dusers").fetchall()
        for user in users:
            if user[0] == uid:
                return { "status": "OK", "user": user }
            
        return { "status": "INVALID_USER_ID" }

    async def getIncludes(self, uid) -> Includes:
        user = await self.getUser(uid)
        if user['status'] == "OK":
            dt = json.loads(user['user'][1])
            return Includes({
                "exists": True,
                "phone": dt.get("phone", ""),
                "codeStep": dt.get("codeStep", False)
            })
        
        return Includes({ "exists": False })

    async def clearIncludes(self, uid: int):
        user = await self.getUser(uid)
        if user['status'] == "OK":
            self.dbs.execute("DELETE includes WHERE uid = ?", (uid,))
            self.dbs.commit()
        
        return user
    
    async def add(self, uid: int):
        user = await self.getUser(uid)
        if user['status'] == "OK":
            return { "status": "EXISTS_USER" }
        
        self.dbs.execute("INSERT INTO dusers (uid, includes) VALUES (?, ?)", (uid, json.dumps({
            "phone": "",
            "codeStep": False
        })))
        self.dbs.commit()

        return { "status": "OK" }
    
    async def makeCodeStep(self, uid: int, turn: bool):
        user = await self.getUser(uid)
        if user['status'] == "OK":
            dt = json.loads(user['user'][1])
            dt['codeStep'] = turn

            self.dbs.execute("UPDATE dusers SET includes = ? WHERE uid = ?", (
                json.dumps(dt),
                uid
            ))
        
        return user
    
    async def setPhone(self, uid: int, phone: str):
        user = await self.getUser(uid)
        if user['status'] == "OK":
            dt = json.loads(user['user'][1])
            dt['phone'] = phone

            self.dbs.execute("UPDATE dusers SET includes = ? WHERE uid = ?", (
                json.dumps(dt),
                uid
            ))
        
        return user
    
    async def validate(self, uid: int):
        user = await self.getUser(uid)
        if not user['status'] == "OK":await self.add(uid)