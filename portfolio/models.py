from portfolio import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    comment_text = db.Column(db.Text)
    timestamp = db.Column(db.Text)
    file_path = db.Column(db.Text)
    votes = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)

    def __init__(self, username, comment, timestamp, file_path, parent_id):
        self.username = username
        self.comment_text = comment
        self.timestamp = timestamp
        self.file_path = file_path
        self.parent_id = parent_id
        self.votes = 0

    def __repr__(self):
        return "<Comment(username='%s', comment='%s', timestamp='%s', file_path='%s')>" \
               % (self.username, self.comment_text, self.timestamp, self.file_path)


class Expletives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expletive = db.Column(db.Text)
    correction = db.Column(db.Text)

    def __init__(self, expletive, correction):
        self.expletive = expletive
        self.correction = correction

    def __repr__(self):
        return "<Expletives(expletive='%s', correction='%s')>" % (self.expletive, self.correction)
