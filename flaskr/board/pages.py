from flask import Blueprint, render_template, current_app, g

import sys
import os
import logging
from flask_mysqldb import MySQL
# # Get the absolute path to the parent of the parent directory (go back two levels)
# parent_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# # Append the directory containing the file you want to import
# sys.path.append(os.path.join(parent_parent_dir, 'pokemon_stat_finder'))

# from var import *

bp = Blueprint("pages", __name__)


@bp.route('/')
def home():
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats ;")
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")

@bp.route("/about")
def about():
    return render_template("pages/about.html")