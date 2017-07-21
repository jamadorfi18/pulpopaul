import os
from flask_script import Manager, Server
from pulpopaul import create_app
from pulpopaul.models import db, Match, Team, Tournament

# default to dev config
ENV = os.environ.get('WEBAPP_ENV', 'dev')
APP = create_app('pulpopaul.config.%sConfig' % ENV.capitalize())
MANAGER = Manager(APP)

# Commands
MANAGER.add_command("server", Server(use_reloader=True))

@MANAGER.shell
def make_shell_context():
    return dict(app=APP, db=db, Match=Match, Team=Team, Tournament=Tournament)

if __name__ == "__main__":
    MANAGER.run()
