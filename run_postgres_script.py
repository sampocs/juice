import os
import sys
import psycopg2 as psql
import utils

def main():

    script_filename = sys.argv[1]
    assert os.path.isfile(f'./{script_filename}'), 'SQL Script does not exist'

    conn, cur = utils.connect_to_postgres()

    with open(script_filename, 'r') as f:
        script_text = f.read()

    # all SQL commands (split on ';')
    sql_commands = script_text.split(';')[:-1]

    for command in sql_commands:
        try:
            cur.execute(command)
        except psql.OperationalError as msg:
            print(f"Command skipped: {msg}")

    conn.commit()

if __name__ == "__main__":
    main()