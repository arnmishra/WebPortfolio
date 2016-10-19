from portfolio import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    comment_text = db.Column(db.Text)
    timestamp = db.Column(db.Text)
    file_name = db.Column(db.Text)
    votes = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)

    def __init__(self, username, comment, timestamp, file_name, parent_id):
        self.username = username
        self.comment_text = comment
        self.timestamp = timestamp
        self.file_name = file_name
        self.parent_id = parent_id
        self.votes = 0

    def __repr__(self):
        return "<Comment(username='%s', comment='%s', timestamp='%s')>" \
               % (self.username, self.comment_text, self.timestamp)
