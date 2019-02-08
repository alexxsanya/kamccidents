from . import db, bcrypt
import datetime
from marshmallow import fields, Schema

class UsersModel(db.Model):
  """
  Users Model
  """
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(25), nullable=False)
  lastname = db.Column(db.String(25), nullable=False)
  email = db.Column(db.Text,nullable=False)
  password = db.Column(db.Text, nullable=False)
  phone = db.Column(db.String(12),nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    print(">>> {} ".format(data))
    self.firstname = data.get('firstname')
    self.lastname = data.get('lastname')
    self.email = data.get('email') 
    self.password = self.__generate_hash(data.get('password'))
    self.phone = data.get('phone')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      if key == 'password': 
        self.password = self.__generate_hash(value)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    de.session.commit()
  
  @staticmethod
  def get_all_users():
    return UsersModel.query.all()
  
  @staticmethod
  def get_one_user(id):
    return UsersModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  @staticmethod
  def get_user_by_email(email):
    return UsersModel.query.filter_by(email=email).first()
# add this class
class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  firstname = fields.Str(required=True)
  lastname = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True)
  phone = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True) 