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
        stat_rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', poke_stats=stat_rows)
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
        stat_rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', poke_stats=stat_rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/home.html', rows=[])


@bp.route('/search/ability', methods=['POST'])
def search_ability():
    query = request.form.get('query')
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT distinct * FROM abilities Where ability_name LIKE %s;", (f"%{query}%",))
        ability_rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/abilities.html', abilities=ability_rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])


@bp.route('/')
def home():
    try:
        mysql = current_app.mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM poke_stats;")
        stat_rows = cursor.fetchall()
        cursor.close()
        #print(rows)
        return render_template('pages/home.html', poke_stats=stat_rows)
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
        # Gather pokemon stats
        cursor.execute("SELECT * FROM poke_stats p WHERE p.id = %s;", (query,))
        stat_rows = cursor.fetchall()
        # Gather pokemon weaknesses
        cursor.execute("Select  distinct w.* from poke_stats p join pokemon_weakness w on w.poke_name = p.poke_name where p.id = %s;", (query,))
        weakness_rows = cursor.fetchall()
        # Gather pokemon abilities
        cursor.execute("""
            SELECT distinct p.poke_name,
                p.ability AS ability_1, 
                case 
                           when a1.scarlet_violet != 'n/a' then a1.scarlet_violet
                           when a1.scarlet_violet = 'n/a' then a1.sword_shield 
                           when a1.sword_shield = 'n/a' then a1.ultra_sun_ultra_moon
                           when a1.ultra_sun_ultra_moon = 'n/a' then a1.x_y  end AS ability_1_description,
                pp.ability_2 as ability_2, 
                       
                case 
                           when a2.scarlet_violet != 'n/a' then a2.scarlet_violet
                           when a2.scarlet_violet = 'n/a' then a2.sword_shield 
                           when a2.sword_shield = 'n/a' then a2.ultra_sun_ultra_moon
                           when a2.ultra_sun_ultra_moon = 'n/a' then a2.x_y   end AS ability_2_description
            FROM poke_stats p
            JOIN abilities a1 ON p.ability = a1.ability_name
            LEFT JOIN poke_stats pp ON p.ability_2 = pp.ability_2
            LEFT JOIN abilities a2 ON pp.ability_2 = a2.ability_name
            WHERE p.id = %s;
        """, (query,))
        ability_rows = cursor.fetchall()


        cursor.execute("""  
        select distinct s.*
        from pokemon_sprites s
        join poke_stats p on s.poke_name = p.poke_name 
        where p.id = %s;
    """, (query,))

        sprite_rows = cursor.fetchall()

        cursor.execute("""
        select s.pokemon, s.move_name, 
        s.level_learned_at, 
        learn_method, 
        p.move_description,
        p.move_attack_type,
        p.move_type,
        case when p.attack is null then '0' 
            else p.attack end as 'attack', 
         p.pp,
        p.priority
            from pokemon_move_set s
            join pokemon_moves p on s.move_name = p.move_name
            where s.game_name ='scarlet-violet'
            and s.learn_method = 'level-up'
            and s.pokemon_id = %s
            order by level_learned_at asc
            ;
        """,(query,))

        level_up_moves_rows = cursor.fetchall()
        
        cursor.execute("""
        select s.pokemon, s.move_name, 
        s.level_learned_at, 
        learn_method, 
        p.move_description,
        p.move_attack_type,
        p.move_type,
        case when p.attack is null then '0' 
            else p.attack end as 'attack', 
         p.pp,
        p.priority
            from pokemon_move_set s
            join pokemon_moves p on s.move_name = p.move_name
            where s.game_name ='scarlet-violet'
            and s.learn_method = 'egg'
            and s.pokemon_id = %s
            order by move_name asc
            ;
        """,(query,))

        egg_moves_row = cursor.fetchall()

        cursor.execute("""
        select s.pokemon, s.move_name, 
        s.level_learned_at, 
        learn_method, 
        p.move_description,
        p.move_attack_type,
        p.move_type,
        case when p.attack is null then '0' 
            else p.attack end as 'attack', 
         p.pp,
        p.priority,
        m.machine_name
            from pokemon_move_set s
            join pokemon_moves p on s.move_name = p.move_name
            join machine_moves m on m.move_name =  p.move_name
            where s.game_name ='scarlet-violet'
            and s.learn_method = 'machine'
            and s.pokemon_id = %s
            and m.game_name = 'scarlet-violet'
            order by move_name asc
            ;
        """,(query,))

        machine_moves_row = cursor.fetchall()

        cursor.close()

        return render_template('pages/pokemon.html', poke_stats=stat_rows, type_weakness=weakness_rows, 
        abilities=ability_rows, sprites = sprite_rows, level_up_moves = level_up_moves_rows, egg_moves = egg_moves_row,
        machine_moves = machine_moves_row)
    except Exception as e:
        logging.error(f"could not fetch data due to {e}")
        return render_template('pages/pokemon.html', rows=[])


@bp.route('/abilities')
def abilities():

    try:
            mysql = current_app.mysql
            cursor = mysql.connection.cursor()
            cursor.execute("""SELECT ability_name, 
                           case 
                           when scarlet_violet != 'n/a' then scarlet_violet
                           when scarlet_violet = 'n/a' then sword_shield 
                           when sword_shield = 'n/a' then ultra_sun_ultra_moon
                           when ultra_sun_ultra_moon = 'n/a' then x_y    
                           end as 'ability_desc'                        
            FROM abilities order by ability_name asc;
            """)
            ability_rows = cursor.fetchall()
            cursor.close()
            return render_template('pages/abilities.html', abilities=ability_rows)
    except Exception as e:
        logging.error(f"could not insert data due to {e}")
        return render_template('pages/abilities.html', rows=[])