from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.user_model import UsersModel,UserSchema
from views import init_app, db

app = init_app()

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()