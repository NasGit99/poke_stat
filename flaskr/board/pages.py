from flask import Blueprint, render_template, current_app, request
import sys
import os
import logging
from flask_mysqldb import MySQL
from contextlib import closing

bp = Blueprint("pages", __name__)

def execute_query(query, params=()):
    try:
        mysql = current_app.mysql
        with closing(mysql.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return []

@bp.route('/index')
def index():
    return render_template('pages/index.html')

@bp.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    try:
        stat_rows = execute_query("SELECT DISTINCT * FROM poke_stats WHERE poke_name LIKE %s;", (f"%{query}%",))
        return render_template('pages/home.html', poke_stats=stat_rows)
    except Exception as e:
        logging.error(f"Could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])

@bp.route('/search/type', methods=['POST'])
def search_type():
    query = request.form.get('query')
    try:
        stat_rows = execute_query("SELECT DISTINCT * FROM poke_stats WHERE type LIKE %s OR type_2 LIKE %s;", 
                                   (f"%{query}%", f"%{query}%"))
        return render_template('pages/home.html', poke_stats=stat_rows)
    except Exception as e:
        logging.error(f"Could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])

@bp.route('/search/ability', methods=['POST'])
def search_ability():
    query = request.form.get('query')
    try:
        ability_rows = execute_query("SELECT DISTINCT * FROM abilities WHERE ability_name LIKE %s;", (f"%{query}%",))
        return render_template('pages/abilities.html', abilities=ability_rows)
    except Exception as e:
        logging.error(f"Could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])

@bp.route('/')
def home():
    try:
        stat_rows = execute_query("SELECT * FROM poke_stats;")
        return render_template('pages/home.html', poke_stats=stat_rows)
    except Exception as e:
        logging.error(f"Could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route('/pokemon', methods=['GET'])
def search_pokemon():
    query = request.args.get('id')
    try:
        stat_rows = execute_query("SELECT * FROM poke_stats p WHERE p.id = %s;", (query,))
        weakness_rows = execute_query("""
            SELECT DISTINCT w.* 
            FROM poke_stats p 
            JOIN pokemon_weakness w ON w.poke_name = p.poke_name 
            WHERE p.id = %s;
        """, (query,))
        ability_rows = execute_query("""
            SELECT DISTINCT p.poke_name,
                p.ability AS ability_1, 
                CASE 
                    WHEN a1.scarlet_violet != 'n/a' THEN a1.scarlet_violet
                    WHEN a1.scarlet_violet = 'n/a' THEN a1.sword_shield 
                    WHEN a1.sword_shield = 'n/a' THEN a1.ultra_sun_ultra_moon
                    WHEN a1.ultra_sun_ultra_moon = 'n/a' THEN a1.x_y 
                END AS ability_1_description,
                pp.ability_2 AS ability_2, 
                CASE 
                    WHEN a2.scarlet_violet != 'n/a' THEN a2.scarlet_violet
                    WHEN a2.scarlet_violet = 'n/a' THEN a2.sword_shield 
                    WHEN a2.sword_shield = 'n/a' THEN a2.ultra_sun_ultra_moon
                    WHEN a2.ultra_sun_ultra_moon = 'n/a' THEN a2.x_y 
                END AS ability_2_description
            FROM poke_stats p
            JOIN abilities a1 ON p.ability = a1.ability_name
            LEFT JOIN poke_stats pp ON p.ability_2 = pp.ability_2
            LEFT JOIN abilities a2 ON pp.ability_2 = a2.ability_name
            WHERE p.id = %s;
        """, (query,))
        sprite_rows = execute_query("""
        SELECT DISTINCT s.*
        FROM pokemon_sprites s
        JOIN poke_stats p ON s.poke_name = p.poke_name 
        WHERE p.id = %s;
        """, (query,))
        level_up_moves_rows = execute_query("""
        WITH moveset AS (
            SELECT 
                s.move_name, 
                s.level_learned_at, 
                s.learn_method, 
                p.move_description,
                p.move_attack_type,
                p.move_type,
                COALESCE(p.attack, '0') AS attack, 
                p.pp,
                p.priority,
                ROW_NUMBER() OVER (PARTITION BY s.move_name ORDER BY s.level_learned_at ASC) AS rn
            FROM 
                pokemon_move_set s
            JOIN 
                pokemon_moves p ON s.move_name = p.move_name
            JOIN 
                poke_stats ps ON s.pokemon = ps.poke_name
            WHERE  
                s.learn_method = 'level-up'
                AND s.game_name IN ('scarlet-violet', 'sword-shield', 'ultra-sun-ultra-moon', 'brilliant-diamond-shining-pearl')
                AND ps.id = %s
        )
        SELECT 
            move_name,
            level_learned_at,
            learn_method,
            move_description,
            move_attack_type,
            move_type,
            attack,
            pp,
            priority
        FROM 
            moveset
        WHERE 
            rn = 1
        ORDER BY 
            level_learned_at ASC;
        """, (query,))
        egg_moves_row = execute_query("""
        WITH moveset AS (
            SELECT 
                s.move_name, 
                s.level_learned_at, 
                s.learn_method, 
                p.move_description,
                p.move_attack_type,
                p.move_type,
                COALESCE(p.attack, '0') AS attack, 
                p.pp,
                p.priority,
                ROW_NUMBER() OVER (PARTITION BY s.move_name ORDER BY s.level_learned_at ASC) AS rn
            FROM 
                pokemon_move_set s
            JOIN 
                pokemon_moves p ON s.move_name = p.move_name
            JOIN 
                poke_stats ps ON s.pokemon = ps.poke_name
            WHERE  
                s.learn_method = 'egg'
                AND s.game_name IN ('scarlet-violet', 'sword-shield', 'ultra-sun-ultra-moon', 'brilliant-diamond-shining-pearl')
                AND ps.id = %s
        )
        SELECT 
            move_name,
            level_learned_at,
            learn_method,
            move_description,
            move_attack_type,
            move_type,
            attack,
            pp,
            priority
        FROM 
            moveset
        WHERE 
            rn = 1
        ORDER BY 
            level_learned_at ASC;
        """, (query,))
        machine_moves_row = execute_query("""
        WITH moveset AS (
            SELECT 
                s.move_name, 
                m.machine_name,
                s.level_learned_at, 
                s.learn_method, 
                p.move_description,
                p.move_attack_type,
                p.move_type,
                COALESCE(p.attack, '0') AS attack, 
                p.pp,
                p.priority,
                ROW_NUMBER() OVER (PARTITION BY s.move_name ORDER BY s.level_learned_at ASC) AS rn
            FROM 
                pokemon_move_set s
            JOIN 
                pokemon_moves p ON s.move_name = p.move_name
            JOIN 
                poke_stats ps ON s.pokemon = ps.poke_name
            JOIN 
                machine_moves m ON m.move_name = p.move_name
            WHERE  
                s.learn_method = 'level-up'
                AND s.game_name IN ('scarlet-violet', 'sword-shield', 'ultra-sun-ultra-moon')
                AND ps.id = %s
        )
        SELECT 
            move_name,
            machine_name,
            level_learned_at,
            learn_method,
            move_description,
            move_attack_type,
            move_type,
            attack,
            pp,
            priority
        FROM 
            moveset
        WHERE 
            rn = 1
        ORDER BY 
            move_name ASC;
        """, (query,))
        return render_template('pages/pokemon.html', poke_stats=stat_rows, type_weakness=weakness_rows, 
                               abilities=ability_rows, sprites=sprite_rows, level_up_moves=level_up_moves_rows, 
                               egg_moves=egg_moves_row, machine_moves=machine_moves_row)
    except Exception as e:
        logging.error(f"Could not fetch data due to {e}")
        return render_template('pages/pokemon.html', rows=[])

@bp.route('/abilities')
def abilities():
    try:
        ability_rows = execute_query("""
            SELECT ability_name, 
                CASE 
                    WHEN scarlet_violet != 'n/a' THEN scarlet_violet
                    WHEN scarlet_violet = 'n/a' THEN sword_shield 
                    WHEN sword_shield = 'n/a' THEN ultra_sun_ultra_moon
                    WHEN ultra_sun_ultra_moon = 'n/a' THEN x_y    
                END AS 'ability_desc'                        
            FROM abilities 
            ORDER BY ability_name ASC;
        """)
        return render_template('pages/abilities.html', abilities=ability_rows)
    except Exception as e:
        logging.error(f"Could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])
