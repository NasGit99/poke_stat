from flask import Blueprint, render_template, current_app, request

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

@bp.route('/index')
def index():
    return render_template('pages/index.html')

@bp.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats Where poke_name LIKE %s;", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])
    

@bp.route('/search/type', methods=['POST'])
def search_type():
    query = request.form.get('query')
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats Where type LIKE %s;", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])


@bp.route('/search/ability', methods=['POST'])
def search_ability():
    query = request.form.get('query')
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats Where ability LIKE %s;", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])


@bp.route('/')
def home():
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats;")
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])


@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route('/pokemon', methods=['GET'])
def search_pokemon():
    query = request.args.get('id')
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats WHERE id = %s;", (query,))
        rows = cursor.fetchall()
        cursor.close()
        return render_template('pages/home.html', rows=rows)
    except Exception as e:
        logging.error(f"could not fetch data due to {e}")
        return render_template('pages/home.html', rows=[])