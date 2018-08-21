import sqlite3
#from credentials import bd
'''
DB has the following tables:
Names, Events, Members, MemberRoles, Roles,
'''

def injector(command):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    res = list()
    print(f'injection: {command}')
    try:
        for row in cur.execute(str(command)):
            print(row)
            res.append(row)
        conn.commit()
    except BaseException as be:
        print("SQL injection error: ", type(be), be)
    return res

def add_event(e_i, y, m, d, t):
    #def add_event(e_i, dt):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
        cur.execute('''INSERT OR IGNORE into Events (event_id, year, month, day, time) values (?, ?, ?, ?, ?)
    ''', (e_i, y, m, d, t))

        #cur.execute('''INSERT OR IGNORE into Events (event_id, event_dt) values (?, ?)
    #''', (e_i, dt))

        conn.commit()
    except BaseException as be:
        print('add event error: ',type(be), be)

def find_event(year, month, day, time):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
        cur.execute('''select Events.event_id from Events where
         Events.year = ? and Events.month = ? and Events.day = ? and Events.time = ?
    ''', (year, month, day, time))
        e_i = cur.fetchone()[0]
    except TypeError as te:
        e_i = None
    except BaseException as be:
        print("Found no DB while finding event: ",type(be), be)
        e_i= -1
    finally:
        return e_i

def is_event(e_i):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
       cur.execute('''SELECT COUNT(*) FROM Events where event_id= ?
           ''', (e_i))
       r = cur.fetchone()[0]
    except BaseException as be:
        print("is event error: ",type(be), be)
    if r == 0:
        res = False
    else:
        res = True
    return res

def add_member(e_i, name, a_o):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
   #     cur.execute('''INSERT into Archers (event_id, name) values (?, ?)
   # ''', (e_i, name))
        cur.execute('''INSERT OR IGNORE into Members (event_id, name, add_order) values (?, ?, ?)
    ''', (e_i, name, a_o))
        conn.commit()
    except BaseException as be:
        print('add_member error: ',type(be), be)

def show_members(year, month, day, time):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
        members = list()
        for member in cur.execute('''
    select Members.name from Members inner join Events on Events.event_id = Members.event_id
    and year = ? and month = ? and day = ? and time = ? ORDER BY Members.add_order ASC
    ''', (year, month, day, time)):
            members.append(member)
    except BaseException as be:
        print('show member error: ',type(be), be)
        members = None
    return members

def patch_EandM(e_i):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    try:
       cur.execute('''
       DELETE FROM Events where event_id = ?
       ''', (e_i,))
    except BaseException as be:
        print('patch events error: ', be)
    try:
      cur.execute('''
       DELETE FROM Members where event_id = ?
       ''', (e_i,))
    except BaseException as be:
        print('patch members error: ',type(be), be)
    finally:
        conn.commit()

def fullfill(start):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()

    cur.execute('''
    SELECT DATE(?, '+1 day')
    ''', (start,))
    start = cur.fetchone()[0]
    return start




"""
print('Start init')
init_tables()
print('End init')

c_i1 = 247893408
c_i2 = 354668710

n1 = "Денис"
s1 = 'Давыдов'

n2 = "Лида"
s2 = 'Рудакова'

print('...\nStart adding')
add_name(c_i1, n1, s1)
add_name(c_i2, n2, s2)

add_event('abyr', 1, 2, 3, 4)
add_event('abyrwalg', 1, 2, 3, 5)

add_event('abyr',       '01-02-03T04:05:06.000')
add_event('abyrwalg',   '01-02-03T05:05:06.000')


add_member('abyr', 'abal1', 0)
add_member('abyrwalg', 'abal', 0)
add_member('abyr', 'abal2',1)
add_member('abyr', 'abal3',2)
conn = sqlite3.connect(bd)
cur = conn.cursor()
cur.execute('''
       DELETE FROM Members where event_id = 'abyr'
       ''')
conn.commit()
add_member('abyr', 'abal1',0)
add_member('abyrwalg', 'abal',3)
add_member('abyr', 'abal2',1)
add_member('abyr', 'abal3',2)
print('End adding')

print('Show starts')
members = show_members(1,2,3,4)
for member in members:
    print(member)
print('Show ends')

d = '2017-09-01'
d = fullfill(d)
print(d)


print('...\nStart read')
name_surname = read_name(247893408)
print('End read\n', name_surname[0], name_surname[1])


"""


"""
def del_member(e_i, name):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    success = False
    try:
        cur.execute('''DELETE from Members where event_id = ? and name = ?
''', (e_i, name))
        conn.commit()
        success = True
    except BaseException as be:
        print('del_member error: ', be)
    finally:
        return success
"""

#from create_tables

"""    cur.executescript('''
    DROP TABLE IF EXISTS Names;
    DROP TABLE IF EXISTS Events;
    DROP TABLE IF EXISTS Members;
    DROP TABLE IF EXISTS MemberRoles;
    DROP TABLE IF EXISTS Roles;
    ''')
    cur.executescript('''
    CREATE TABLE Names (chat_id INTEGER PRIMARY KEY UNIQUE, name text, surname text);
    CREATE TABLE Events (event_id TEXT, year INTEGER, month INTEGER,  day INTEGER,  time INTEGER, PRIMARY KEY (year, month, day, time));
    CREATE TABLE Members (event_id text, name text, add_order INTEGER, PRIMARY KEY (event_id, name));
    CREATE TABLE MemberRoles (chat_id INTEGER UNIQUE, role_id INTEGER, PRIMARY KEY (chat_id));--, role_id)); --??
    CREATE TABLE Roles (role_id integer PRIMARY KEY AUTOINCREMENT, name text);
    ''')
    conn.commit()
    """
