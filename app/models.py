from app import app, create_conn
from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    def __init__(self, _id=None, _username="", _email="", _pass_hash=""):
        self.conn, self.cursor = create_conn()
        self._id = _id
        if not self._id:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            self._id = self.cursor.fetchone()[0] + 1
        self._name = _username
        self._email = _email
        self._pass_hash = _pass_hash
    def save(self):
        u = User.get_with_username(self._name)
        if u:
            self.cursor.execute("UPDATE users SET id = {}, username = \"{}\", email = \"{}\" password_hash = \"{}\" WHERE id = {}".format(self._id, self._name, self._email, self._pass_hash, u._id))
            self.conn.commit()
        else:
            self.cursor.execute("INSERT INTO users VALUES ({}, \"{}\", \"{}\", \"{}\")".format(self._id, self._name, self._email, self._pass_hash))
            self.conn.commit()

    @classmethod
    def get_all(cls):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [cls(row[0], row[1], row[2], row[3]) for row in rows]
    
    @classmethod
    def get_with_id(cls, _id):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM users WHERE id = {}".format(_id))
        row = cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None

    @classmethod
    def get_with_username(cls, username):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM users WHERE username = \"{}\"".format(username))
        row = cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None

    @classmethod
    def get_with_email(cls, email):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM users WHERE email = \"{}\"".format(email))
        row = cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None
    
    def get_logs(self):
        self.cursor.execute("SELECT * FROM logs WHERE u_id = {}".format(self._id))
        rows = self.cursor.fetchall()
        return [Log(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        
    def set_password(self, password):
        self._pass_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self._pass_hash, password)
class Log(object):
    def __init__(self, _id=None, activity_type="", time=0, hr=0, user_id=0):
        self.conn, self.cursor = create_conn()
        self._id = _id
        if not self._id:
            self.cursor.execute("SELECT COUNT(*) FROM logs")
            self._id = self.cursor.fetchone()[0] + 1
        self.activity_type = activity_type
        self.time = time
        self.hr = hr
        self.user_id = user_id
    def save(self):
        l = Log.get_with_id(self._id)
        if l:
            self.cursor.execute("UPDATE logs SET id = {}, type = \"{}\", time = {}, hr = {}, u_id = {} WHERE id = {}".format(self._id, self.activity_type, self.time,\
                                                                                                self.hr, self.user_id, self.l._id))
            self.conn.commit()
        else:
            self.cursor.execute("INSERT INTO logs VALUES ({}, \"{}\", {}, {}, {})".format(self._id, self.activity_type, self.time, self.hr, self.user_id))
            self.conn.commit()

    @classmethod
    def get_all(cls):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()
        return [cls(row[0], row[1], row[2], row[3]) for row in rows]
    
    @classmethod
    def get_with_id(cls, _id):
        conn, cursor = create_conn()
        cursor.execute("SELECT * FROM logs WHERE id = {}".format(_id))
        row = cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2], row[3])
        return None
    def get_user(self):
        return User.get_with_id(self.user_id)
