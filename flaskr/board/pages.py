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
        cursor.execute("SELECT distinct * FROM poke_stats Where poke_name LIKE %s;", (f"%{query}%",))
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
        cursor.execute("SELECT distinct * FROM poke_stats Where type LIKE %s or type_2 like %s;", (f"%{query}%",(f"%{query}%")))
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
        cursor.execute("SELECT * FROM abilities Where ability_name LIKE %s;", (f"%{query}%",))
        rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/abilities.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])


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
        cursor.execute("SELECT * FROM poke_stats p WHERE p.id = %s;", (query,))
        rows = cursor.fetchall()
        cursor.execute("Select  distinct w.* from poke_stats p join pokemon_weakness w on w.poke_name = p.poke_name where p.id = %s;", (query,))
        row2 = cursor.fetchall()
        cursor.execute("""
            SELECT distinct p.poke_name,
                p.ability AS ability_1, 
                a1.sword_shield AS ability_1_description,
                pp.ability_2 as ability_2, 
                a2.sword_shield AS ability_2_description
            FROM poke_stats p
            JOIN abilities a1 ON p.ability = a1.ability_name
            LEFT JOIN poke_stats pp ON p.ability_2 = pp.ability_2
            LEFT JOIN abilities a2 ON pp.ability_2 = a2.ability_name
            WHERE p.id = %s;
        """, (query,))
        row3 = cursor.fetchall()

        cursor.close()
        return render_template('pages/pokemon.html', rows=rows, rows2=row2, rows3=row3)
    except Exception as e:
        logging.error(f"could not fetch data due to {e}")
        return render_template('pages/pokemon.html', rows=[])

@bp.route('/abilities')
def abilities():

    try:
            mysql = current_app.mysql
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT ability_name, sword_shield FROM abilities order by ability_name asc;")
            rows = cursor.fetchall()
            cursor.close()
            return render_template('pages/abilities.html', rows=rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])