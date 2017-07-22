import os
from datetime import datetime, timedelta


def get_current_time():
  return datetime.utcnow()
   
def get_current_time_plus(days=0, hours=0, minutes=0, seconds=0):
  return get_current_time() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

#see http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
def dump_datetime(value):
  if value is None:
    return None
  return value.strftime("%Y-%m-%d") +"T"+ value.strftime("%H:%M:%S")+"Z"

def make_dir(dir_path):
  try:
    if not os.path.exists(dir_path):
      os.mkdir(dir_path)
  except Exception as e:
    raise e
