"""
Used to help write tests: https://pythonhosted.org/Flask-Testing/ and http://damyanon.net/flask-series-testing/
"""

from portfolio import app, db
from portfolio.models import Comment, Expletives
from portfolio.views import edit_expletives
import unittest


class FlaskCommentTests(unittest.TestCase):

    def setUp(self):
        """ Used to set up the database and app for each test """
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()
        censor = {"fuck": "f***", "shit": "s***", "crap": "c***", "damn": "d***", "bitch": "b****", "ass": "a**"}
        for word in censor:
            new_expletive = Expletives(word, censor[word])
            db.session.add(new_expletive)
            db.session.commit()

    def tearDown(self):
        """ Used to remove the database for each test """
        db.session.remove()
        db.drop_all()

    def test_home_status_code(self):
        """ Test of home page rendering """
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_empty_db(self):
        """ Test that empty database has no content """
        all_comments = Comment.query.all()
        self.assertTrue(len(all_comments) == 0)

    def test_creating_comment(self):
        """ Test that comments are added correctly """
        comment = Comment("username", "comment", "timestamp", "file_path", -1)
        db.session.add(comment)
        db.session.commit()
        self.assertTrue(comment in db.session)
        all_comments = Comment.query.all()
        self.assertEqual(len(all_comments), 1)
        self.assertEqual(all_comments[0].username, "username")
        self.assertEqual(all_comments[0].comment_text, "comment")
        self.assertEqual(all_comments[0].timestamp, "timestamp")
        self.assertEqual(all_comments[0].file_path, "file_path")
        self.assertEqual(all_comments[0].parent_id, -1)

    def test_sql_injection(self):
        """ Test that SQL style comments don't affect the database """
        comment = Comment("username", "DROP DATABASE Comment", "timestamp", "file_path", -1)
        db.session.add(comment)
        db.session.commit()
        self.assertTrue(comment in db.session)
        all_comments = Comment.query.all()
        self.assertEqual(len(all_comments), 1)
        self.assertEqual(all_comments[0].username, "username")
        self.assertEqual(all_comments[0].comment_text, "DROP DATABASE Comment")
        self.assertEqual(all_comments[0].timestamp, "timestamp")
        self.assertEqual(all_comments[0].file_path, "file_path")
        self.assertEqual(all_comments[0].parent_id, -1)

    def test_expletives(self):
        """ Test that expletives are appropriately replaced """
        comment_text = edit_expletives("Fuck this shit.")
        comment = Comment("username", comment_text, "timestamp", "file_path", -1)
        db.session.add(comment)
        db.session.commit()
        self.assertTrue(comment in db.session)
        all_comments = Comment.query.all()
        self.assertEqual(len(all_comments),1)
        self.assertEqual(all_comments[0].username, "username")
        self.assertEqual(all_comments[0].comment_text, "f*** this s***.")
        self.assertEqual(all_comments[0].timestamp, "timestamp")
        self.assertEqual(all_comments[0].file_path, "file_path")
        self.assertEqual(all_comments[0].parent_id, -1)

    def test_add_replies(self):
        """ Test that replies are added correctly """
        comment_text = "parent"
        comment = Comment("username", comment_text, "timestamp", "file_path", -1)
        db.session.add(comment)
        db.session.commit()
        parent_id = Comment.query.filter(Comment.comment_text == comment_text).first().id
        reply = Comment("username", "reply", "timestamp", "file_path", parent_id)
        db.session.add(reply)
        db.session.commit()
        reply = Comment("username", "reply2", "timestamp", "file_path", parent_id)
        db.session.add(reply)
        db.session.commit()
        all_parents = Comment.query.filter(Comment.parent_id == -1)
        num_parents = 0
        for parent in all_parents:
            self.assertEqual(parent.comment_text, "parent")
            num_parents += 1
        self.assertEqual(num_parents, 1)
        all_children = Comment.query.filter(Comment.parent_id == all_parents[0].id)
        num_children = 0
        for child, message in zip(all_children, ["reply", "reply2"]):
            self.assertEqual(child.comment_text, message)
            num_children += 1
        self.assertEqual(num_children, 2)

    def test_vote(self):
        """ Test that voting increases the vote count of a comment """
        comment = Comment("username", "comment", "timestamp", "file_path", -1)
        db.session.add(comment)
        db.session.commit()
        all_comments = Comment.query.all()
        comment_id = all_comments[0].id
        comment = Comment.query.get(comment_id)
        self.assertEqual(comment.votes, 0)
        comment.votes += 1
        db.session.commit()
        comment = Comment.query.get(comment_id)
        self.assertEqual(comment.votes, 1)

if __name__ == '__main__':
    unittest.main()
