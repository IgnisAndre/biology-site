# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
from crontab import CronTab # was it even working? Doubt

#from credentials import server_confirmation_code as s_c_c, vk_secret, token #don't think i need dis



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file, Biology_site.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Biology_site.db'),
    SECRET_KEY='test_development_key',
    USERNAME='RedWitch',
    PASSWORD='RedDog'
))
app.config.from_envvar('BIOLOGY_SITE_SETTINGS', silent=True)

"""
DATABASE
"""

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:    #faq, dis is cool
        db.cursor().executescript(f.read())                 #it means, you write in file
    db.commit()                                             #and then execute the read info

#@app.cli.command('initdb')
@app.route('/initdb_command')
def initdb_command():
    """Initializes the database."""
    init_db()
    return render_template('init_db.html')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

"""
LOGIN AND LOGOUT
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


#VK
"""


@app.route('/callback', methods=['POST'])
def processing():
    data = json.loads(request.data)
    print(data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return s_c_c
    elif data['type'] == 'message_new' and data['secret'] == vk_secret:
        messageHandler.create_answer(data=data['object'], token=token)
    #    user_id = data['object']['user_id']
    #    api.messages.send(user_id=str(user_id), message='Привет, я новый бот!', access_token=token)
        # Сообщение о том, что обработка прошла успешно
        return 'ok'

@app.route('/impflow', methods=['POST', 'GET'])
def impflow():
    return redirect("https://oauth.vk.com/authorize?client_id=6304767&display=popup&redirect_uri=https://oauth.vk.com/blank.html&scope=73728&response_type=token&v=5.73&state=123456")
"""
