# coding=utf-8
import os


from app.models import Comment, User, Role, Permission, Follow, Post
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Follow=Follow, Permission=Permission, Post=Post, Comment=Comment)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
	from flask_migrate import upgrade
	from app.models import Role, User
	upgrade()

# Role.insert_roles()
# User.add_self_follows()

if __name__ == '__main__':
	manager.run()
