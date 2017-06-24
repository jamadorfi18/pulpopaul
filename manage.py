import os
from flask_script import Manager, Server
from pulpopaul import create_app
from pulpopaul.models import db, Match, Team

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('pulpopaul.config.%sConfig' % env.capitalize())

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
