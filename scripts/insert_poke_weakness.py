from db_connector import *
from var import *


# Define type columns
type_columns = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy", "Stellar"]

# Base query part
query_base = """

INSERT INTO pokemon_weakness (poke_name, Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy, Stellar)
Select ps.poke_name,
"""

# Dynamically generate the CASE statements for each type column
#Future iterations of this will take into account pokemon with the ability of levitate (Ground = 0)
case_statements = []
for col in type_columns:
    case_statement = f"""
    CASE 
        WHEN ps.type_2 IS NOT NULL THEN 
            CASE 
                -- If either type is 0, the result is 0
                WHEN tw1.{col} = 0 OR tw2.{col} = 0 THEN 0
                -- If type_2 is 2, apply the adjustment logic
                WHEN tw2.{col} = 2 THEN 
                    CASE 
                        -- If the total weakness is 2 or more, adjust it accordingly
                        WHEN (tw1.{col} = 2 AND tw2.{col} = 2) THEN 4
                        WHEN (tw1.{col} + tw2.{col}) = 3 THEN 2
                        WHEN (tw1.{col} + tw2.{col}) = 2.5 THEN 1
                        WHEN (tw1.{col} + tw2.{col}) = 1.5 THEN 1
                        ELSE tw1.{col} + tw2.{col}
                    END
                -- If type_2 is 0.5, divide the value by 2
                WHEN tw2.{col} = 0.5 THEN 
                    CASE
                        -- If the primary type is 0.5, then the result should be 0.5
                        WHEN tw1.{col} = 0.5 THEN 0.5
                        ELSE tw1.{col} / 2
                    END
                ELSE tw1.{col}
            END
        ELSE tw1.{col}
    END AS {col}
    """
    case_statements.append(case_statement)

# Combine the CASE statements with the base query
query_middle = ",\n".join(case_statements)

# Add the FROM and JOIN parts
query_end = """
FROM 
    poke_stats ps
JOIN 
    type_weakness tw1 
ON 
    ps.Type = tw1.Type_Name
LEFT JOIN 
    type_weakness tw2 
ON 
    ps.Type_2 = tw2.Type_Name;
"""

# Combine all parts to form the complete query
query = query_base + query_middle + query_end

print(query)


mydb = db_connection()
mycursor = mydb.cursor()



mycursor.execute("""
CREATE TABLE IF NOT EXISTS pokemon_weakness  (
    poke_name VARCHAR(255),
    Normal FLOAT,
    Fire FLOAT,
    Water FLOAT,
    Electric FLOAT,
    Grass FLOAT,
    Ice FLOAT,
    Fighting FLOAT,
    Poison FLOAT,
    Ground FLOAT,
    Flying FLOAT,
    Psychic FLOAT,
    Bug FLOAT,
    Rock FLOAT,
    Ghost FLOAT,
    Dragon FLOAT,
    Dark FLOAT,
    Steel FLOAT,
    Fairy FLOAT,
    Stellar FLOAT
);


""")

mycursor.execute(query)

results = mycursor.fetchall()

for row in results:
    print(row)


try:
    # Execute the INSERT query
    mycursor.execute(query)
    # Commit the transaction
    mydb.commit()
    print("Data inserted successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    mydb.rollback()

mycursor.close()
mydb.close()


