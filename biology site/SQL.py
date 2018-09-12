import sqlite3
'''
DB has the following tables:
entries;
Question;
Blocks;
Box;
Answer;
QUUSBOX_MATRIX;
User;
UserRoles;
Roles;
'''
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
'''
