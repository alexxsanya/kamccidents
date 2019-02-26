from . import db
import datetime
from marshmallow import fields, Schema

class AccidentsModel(db.Model):
  """
  Accident Report Model
  """ 
  __tablename__ = 'accidents'

  id = db.Column(db.Integer, primary_key=True)
  acc_title = db.Column(db.String(128), nullable=False)
  acc_desc = db.Column(db.Text, nullable=False)
  acc_time = db.Column(db.Text,nullable=False)
  acc_location = db.Column(db.String(250), nullable=False)
  acc_area_name = db.Column(db.String(250))
  acc_involved = db.Column(db.String(250), nullable=False) 
  acc_is_victim = db.Column(db.Boolean,nullable=True) 
  acc_photo = db.Column(db.String(100), nullable=False)
  acc_created_by = db.Column(db.Integer,db.ForeignKey('users.id'))
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  accidents = db.relationship('AccidentStatModel', backref='accidents', lazy=True)

  def __init__(self, data):
    self.acc_title = data.get('acc_title') 
    self.acc_desc = data.get('acc_desc')
    self.acc_time = data.get('acc_time')
    self.acc_location = data.get('acc_location')
    self.acc_area_name = data.get('acc_area_name')
    self.acc_involved = data.get('acc_involved')
    self.acc_is_victim = data.get('acc_is_victim')
    self.acc_photo = data.get('acc_photo')
    self.acc_created_by = data.get('acc_created_by')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_accidents(user_id):
    return AccidentsModel.query.filter_by(acc_created_by=user_id).all()

  @staticmethod
  def get_accidents_from_db():
    return AccidentsModel.query.all()
  @staticmethod
  def get_one_accident(id):
    return AccidentsModel.query.get(id)
  
  @staticmethod
  def get_accident_by_title(title):
    return AccidentsModel.query.filter_by(acc_title=title).first()

  def __repr__(self):
    return '<id {}>'.format(self.id)


class AccidentStatModel(db.Model):
  """
  Accident Statistics Model
  """ 
  __tablename__ = 'accidents_stat'

  id = db.Column(db.Integer, primary_key=True)
  acc_id = db.Column(db.Integer, db.ForeignKey('accidents.id'),unique=True)
  acc_no_uninjured = db.Column(db.Integer,nullable=False)
  acc_no_minor = db.Column(db.Integer,nullable=False)
  acc_no_major = db.Column(db.Integer, nullable=False)
  acc_no_dead = db.Column(db.Integer, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.acc_id = data.get('acc_id')
    self.acc_no_uninjured = data.get('acc_no_uninjured')
    self.acc_no_minor = data.get('acc_no_minor')
    self.acc_no_major = data.get('acc_no_major')
    self.acc_no_dead = data.get('acc_no_dead') 
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    de.session.commit()
  
  @staticmethod
  def get_accident_stat(id):
    return AccidentStatModel.query.filter_by(acc_id=id).first()
    
  def __repr__(self):
    return '<id {}>'.format(self.id)


class AccidentsModelSchema(Schema):
  """
  AccidentsModel Schema
  """
  id = fields.Int(dump_only=True)
  acc_title = fields.Str(required=True)
  acc_desc = fields.Str(required=True)
  acc_time = fields.Str(required=True)
  acc_location = fields.Str(required=True)
  acc_area_name = fields.Str(required=True)
  acc_involved = fields.Str(required=True)
  acc_is_victim = fields.Boolean()
  acc_photo = fields.Str(required=True)
  acc_created_by = fields.Int(required=True)  
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True) 


class AccidentStatModelSchema(Schema):
  """
  AccidentStatModel Schema
  """
  id = fields.Int(dump_only=True)
  acc_id = fields.Int(required=True)
  acc_no_uninjured = fields.Int(required=True)
  acc_no_minor = fields.Int(required=True)
  acc_no_major = fields.Int(required=True)
  acc_no_dead = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True) 