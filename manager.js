const { Database } = require("sqlite3");

class Manager {
    constructor(){
        this.db = new Database("mngs.db", (err) => {
            if (err){
                console.log(`[manager] error: ${err}`);
            }
            this.setup();
        })
    }

    setup(){
        this.db.run("CREATE TABLE IF NOT EXISTS dusers (uid INTEGER PRIMARY KEY, language TEXT)", (err) => {
            if (err){
                console.log(`[manager] error: ${err}`);
            }
        })
    }

    async getAll(callback = () => {}){
        this.db.all("SELECT * FROM dusers", [], (err, rows) => {
            if (err){
                callback({
                    status: "ERROR",
                    message: err
                });
                return;
            } else {
                callback({
                    status: "OK",
                    users: rows
                });
                return;
            }
        })
    }

    async getUserById(uid, callback = () => {}){
        await this.getAll(async (data) => {
            if (data.status === "OK"){
                for (let user of data.users){
                    if (user.uid === uid){
                        callback({
                            status: "OK",
                            user: user
                        });
                        return;
                    }
                }
                callback({
                    status: "INVALID_UID"
                });
                return;
            }
        })
    }

    async add(
        uid,
        callback = () => {}
    ){
        await this.getUserById(uid, async (user) => {
            if (user.status === "OK"){
                callback({
                    status: "EXISTS_USER"
                });
                return;
            } else {
                const stmt = this.db.prepare("INSERT INTO dusers (uid, language) VALUES (?, ?)");
                stmt.run(uid, "eng");
                stmt.finalize((er) => {
                    if (er){
                        callback({
                            status: "CANNOT_FINALIZE",
                            message: er
                        });
                        return;
                    } else {
                        callback({
                            status: "OK",
                            user: {
                                uid: uid
                            }
                        });
                    }
                })
            }
        })
    }

}

module.exports = { Manager };