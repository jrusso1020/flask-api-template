from flask_script import Manager
from flask import url_for, current_app
from app import create_app
from app.extensions import db
import os

def create_my_app(config=None):
  app = create_app()
  return app

manager = Manager(create_my_app)

manager.add_option('-c', '--config',
                    dest="config",
                    required=False,
                    help="config [local, dev, prod]")

@manager.command
def run():
  """Run in local machine."""
  port = int(os.environ.get("PORT", 5000))
  current_app.run(host='0.0.0.0', port=port, debug=True)

@manager.command
def initdb():
  """Init/reset database."""

  db.drop_all(bind=None)
  db.create_all(bind=None)

@manager.command
def list_routes():
  import urllib
  output = []
  for rule in current_app.url_map.iter_rules():
      options = {}
      for arg in rule.arguments:
          options[arg] = "[{0}]".format(arg)
          
      #filter out head and options
      methods = ', '.join([i for i in rule.methods if i !='HEAD' and i!='OPTIONS'])
      #url = url_for(rule.endpoint, **options)
      if rule.endpoint != 'static':
         url = "%s" % rule
         
         output.append({
             'endpoint' : rule.endpoint,
             'methods':   methods,
             'url'    :   url
         })


  for line in sorted(output, key=lambda l: l['url']) :
      line = urllib.unquote("{:40s} {:20s} {}".format(line['endpoint'], line['methods'], line['url']))
      print(line)

if __name__ == "__main__":
  manager.run()
