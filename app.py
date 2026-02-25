# pip install flask Flask-SQLAlchemy pandas numpy scikit-learn
from data import Data
from config import Config
import flask
from flask import Flask, request, session, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
import os
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

app=Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_very_secret_key_here'

db = SQLAlchemy(app)
class CompetitionSettings(db.Model):
  __tablename__ = 'comp_settings'
  id = db.Column(db.Integer, primary_key=True, default=1)
  competition = db.Column(db.String(100), default='march_madness')
  submission = db.Column(db.String(100), default='initial')

  __table_args__ = (
    db.CheckConstraint('id = 1', name='only_one_row'),
  )

def initialize_settings():
  with app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # Check if the single row exists
    settings = db.session.get(CompetitionSettings, 1)
    if settings is None:
      # If not, create it
      initial_settings = CompetitionSettings(id=1)
      db.session.add(initial_settings)
      db.session.commit()

def update_row(column, value):
  settings = db.session.get(CompetitionSettings, 1)
  if settings:
    if column == 'competition':
      settings.competition = value
    else:
      settings.submission = value

    db.session.commit()

def getCompetition():
  settings = db.session.get(CompetitionSettings, 1)
  current_value = settings.competition
  default_value = "march_madness"
  return current_value or default_value

def getSubmission():
  settings = db.session.get(CompetitionSettings, 1)
  current_value = settings.submission
  default_value = "initial"
  return current_value or default_value

@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')

@app.after_request
def add_nosniff_header_to_static(response):
    # Check if the request path starts with the static files URL
    if request.path.startswith(app.static_url_path):
        response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route('/')
@app.route('/index')
def index():
  return flask.render_template('index.html')

@app.route('/columns')
def columns():
  return flask.render_template(getCompetition()+'/columns.html')

@app.route('/ideas')
def ideas():
  return flask.render_template('ideas.html')

@app.route('/rules')
def rules():
  return flask.render_template(getCompetition()+'/rules.html')

@app.route('/data')
def data():
  category = request.args.get('category', 'all')
  csv_columns_map = Data.get_all_columns_and_names(getCompetition(), category)
  return flask.render_template('data.html', csv_data=csv_columns_map)

@app.route('/tables')
def tables():
  item = request.args.get('item')
  table_data = Data.get_data(getCompetition(), item)
  return flask.render_template('tables.html', table=table_data)

@app.route('/set_competition', methods=['POST'])
def set_competition():
  data = request.get_json()
  if data is None or 'selection' not in data:
      return jsonify({"error": "Missing selection value"}), 400
  update_row('competition', data.get('selection'))
  return jsonify({"message": "Competition saved!"}), 200

@app.route('/set_submission', methods=['POST'])
def set_submission():
  data = request.get_json()
  if data is None or 'selection' not in data:
      return jsonify({"error": "Missing selection value"}), 400
  update_row('submission', data.get('selection'))
  return jsonify({"message": "Submission saved!"}), 200

@app.context_processor
def competitions():
  available_dirs = Data.get_subdirectories(
    os.path.join(app.root_path, 'competitions')
  )
  proper_name_dict = {}
  for machine_name in available_dirs:
    proper_name = machine_name.replace('_', ' ').title()
    proper_name_dict[machine_name] = proper_name
  return dict(competition_directories=proper_name_dict)

@app.context_processor
def submissions():
  available_dirs = Data.get_subdirectories(
    os.path.join(app.root_path, 'competitions', getCompetition(), 'submissions')
  )
  proper_name_dict = {}
  for machine_name in available_dirs:
    proper_name = machine_name.replace('_', ' ').title()
    proper_name_dict[machine_name] = proper_name
  return dict(submission_directories=proper_name_dict)

@app.context_processor
def inject_site_settings():
  competition = getCompetition()
  submission = getSubmission()
  return dict(
    competition=competition.replace('_', ' ').title(),
    mach_competition = competition,
    mach_submission = submission,
  )

if __name__ == '__main__':
  initialize_settings()
  app.run(debug=True)
