from flask_script import Manager, Server
from main import app
from models import db, Match, Team

manager = Manager(app)

# Commands
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    return dict(app=app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Match=Match, Team=Team)

if __name__ == "__main__":
    manager.run()
