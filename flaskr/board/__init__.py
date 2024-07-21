from flask import Flask, render_template
from pages import bp
import sys
import os
from flask_mysqldb import MySQL
# Get the absolute path to the parent of the parent directory (go back two levels)
parent_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# Append the directory containing the file you want to import
sys.path.append(os.path.join(parent_parent_dir, 'pokemon_stat_finder'))

from var import *


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    app.config['MYSQL_USER'] = db_user
    app.config['MYSQL_PASSWORD'] = db_password
    app.config['MYSQL_DB'] = 'PokeData'
    app.config['MYSQL_HOST'] = host
    #Important to have this so data returns as a dictionary and not a tuple
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    # Initialize MySQL
    mysql = MySQL(app)

    # Make MySQL instance available throughout the application
    app.mysql = mysql

    return app


#  return app

if __name__ == "__main__":
   program = create_app()
   program.run(host="0.0.0.0", port=8000, debug=True)
   #app.run(host="0.0.0.0", port=8000, debug=True)