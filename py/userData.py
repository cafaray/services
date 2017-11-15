import sqlite3
import hashlib

database = 'dbuser.sqlite'

def createDataStructure():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    print("Generating structure for users.sqlite")
    statement = '''DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS phrase;
        DROP TABLE IF EXISTS groups;
        DROP TABLE IF EXISTS user_group;
        DROP TABLE IF EXISTS function;
        DROP TABLE IF EXISTS group_function;
    '''
    cursor.executescript(statement)
    conexion.commit()
    statement = '''
        CREATE TABLE user (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            user VARCHAR(12) UNIQUE,
            user_mail VARCHAR(120) UNIQUE,
            status VARCHAR(1),
            last_secret TEXT
        );

        CREATE TABLE phrase (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_user INTEGER,
            phrase TEXT,
            date_phrase TEXT,
            status VARCHAR(1)
        );

        CREATE TABLE groups (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE
        );

        CREATE TABLE user_group (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_user INTEGER,
            id_group INTEGER
        );

        CREATE TABLE function (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            function TEXT UNIQUE,
            endpoint TEXT UNIQUE
        );

        CREATE TABLE group_function (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_group INTEGER,
            id_function INTEGER
        );
    '''

    cursor.executescript(statement)
    conexion.commit()
    cursor.close()
    print("Structure generated")

def insertGroups(groups):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    for g in groups:
        cursor.execute('''INSERT OR IGNORE INTO groups (name) 
            VALUES ( ? )''', ( g,))
        conexion.commit()
    cursor.close()

def insertFunctions(functions):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    for f in functions:
        cursor.execute('''INSERT OR IGNORE INTO function (function, endpoint) 
            VALUES ( ? ,?)''', ( f[0],f[1]))
        conexion.commit()
    cursor.close()

def insertGroupFunctions(groupFunctions):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    for g, fs in groupFunctions.items():       
        cursor.execute('''INSERT OR IGNORE INTO groups (name) 
            VALUES ( ? )''', ( g,)) 
        cursor.execute('SELECT id FROM groups WHERE name = ? ', (g, ))
        group_id = cursor.fetchone()[0]
        for f in fs:
            cursor.execute('SELECT id FROM function WHERE function = ? ', (f, ))
            function_id = cursor.fetchone()[0]
            cursor.execute('''INSERT OR IGNORE INTO group_function (id_group, id_function) 
                VALUES ( ? ,?)''', ( group_id, function_id))
        conexion.commit()
    cursor.close()

def insertUser(users):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    for user, values in users.items():
        cursor.execute('''INSERT OR IGNORE INTO user (user, user_mail, status, last_secret) 
            VALUES (?, ?, ?, ?)''', (user, values[1], 'A', values[2])) 
        cursor.execute('SELECT id FROM user WHERE user = ?', (user, ))
        user_id = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO phrase (id_user, phrase, status, date_phrase) 
            VALUES (?, ?, 'D', ?)''', (user_id, values[0], values[2])) 
        for g in values[3]:
            cursor.execute('SELECT id FROM groups WHERE name = ?', (g, ))
            group_id = cursor.fetchone()[0]
            cursor.execute('''INSERT INTO user_group (id_user, id_group) 
               VALUES (?, ? )''', (user_id, group_id)) 
        conexion.commit()   
    cursor.close()

def getUser(user):
    cursor = getConecction()
    statement = '''SELECT user, user_mail, status, last_secret, id FROM user WHERE user = ?;'''
    cursor.execute(statement, (user, ))
    try:
        record = cursor.fetchone()        
        theUser = {'user':record[0], 'user_mail':record[1], 'status':record[2], 'last_secret':record[3], 'code':hashlib.md5(str(record[4]).encode()).hexdigest()}
    except:        
        theUser = None
    cursor.close()
    return theUser

def auth(user, phrase):
    cursor = getConecction()
    statement = '''SELECT user, phrase, B.status, A.status, A.id 
        FROM user A INNER JOIN phrase B 
          ON A.id = B.id_user
        WHERE user = ? and phrase = ?
        ORDER BY B.date_phrase desc;'''
    cursor.execute(statement, (user, phrase))
    try:
        record = cursor.fetchone()
        theUser = {'user':record[0], 'status':record[2], 'userStatus':record[3], 'code':hashlib.md5(str(record[4]).encode()).hexdigest()}
    except:
        theUser = None
    cursor.close()
    return theUser

def getConecction():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    return cursor
