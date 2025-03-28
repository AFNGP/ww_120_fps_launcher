import sqlite3
import os
import json
import time

def special_exit():
    input("Press any key to continue...")
    exit()

def get_game_directory():
    try:
        with open('config.json', 'r') as c:
            c = c.read()
            c = json.loads(c)
            return c['game_directory']
    except:
        print('Incorrect config.json format or config.json not found')
        special_exit()

def cleanup_db_dir(db_dir):
    found_db = False
    for file in os.listdir(db_dir):
        if file == 'LocalStorage.db':
            found_db = True
            continue
        try:
            os.remove(os.path.join(db_directory, file))
        except:
            print(f'Couldn\'t delete {file}')

    if not found_db:
        print('LocalStorage.db not found, make sure the game directory is correct or launch the game at least once')
        special_exit()

def update_db(db_directory):
    try:
        con = sqlite3.connect(f'{db_directory}\\LocalStorage.db')
        cur = con.cursor()

        cur.execute("""
            INSERT OR REPLACE INTO LocalStorage
            VALUES ("CustomFrameRate", 120);
                    """)

        cur.execute("""
            INSERT OR REPLACE INTO LocalStorage
            VALUES ("GameQualitySetting", '{"KeyCustomFrameRate": 120}')
        """)

        cur.close()
        con.commit()
        con.close()

    except:
        print('Make sure your LocalStorage is not read-only and the game is closed')

def launch_game(game_directory):
    try:
        os.startfile(f'"{game_directory}\\Wuthering Waves Game\\Client\\Binaries\\Win64\\Client-Win64-Shipping.exe"')
    except:
        print('Couldn\'t find client to launch. You can proceed to launch the game manually')
        special_exit()

if __name__ == "__main__":
    game_directory = get_game_directory()
    db_directory = f'{game_directory}\\Wuthering Waves Game\\Client\\Saved\\LocalStorage'
    
    print('Attempting to locate DB')
    cleanup_db_dir(db_directory)
    
    print('DB Located, updating DB')
    update_db(db_directory)
    
    print('DB Updated, launching game')
    launch_game(game_directory)

    time.sleep(2)
