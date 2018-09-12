# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
import datetime
from forms import AddBlockForm, AddQuestionForm

#from credentials import server_confirmation_code as s_c_c, vk_secret, token #don't think i need dis


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file, Biology_site.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Biology_site.db'),
    SECRET_KEY='test_development_key',
#    USERNAME='RedWitch',
#    PASSWORD='RedDog'
))
app.config.from_envvar('BIOLOGY_SITE_SETTINGS', silent=True)

"""
DATABASE
"""

def init_db():
    session['role_id'] = -1
    session['user_id'] = -1
    session['logged_in'] = False

    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:    #faq, dis is cool
        db.cursor().executescript(f.read())                 #it means, you write in file
    db.commit()                                             #and then execute the read info

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
    try:
        cur = db.execute('select title, text from entries order by id desc')
        entries = cur.fetchall()
        return render_template('show_entries.html', entries=entries)
    except sqlite3.OperationalError as s:
        init_db()
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
LOGIN, REGISTER AND LOGOUT
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u_n = request.form['username']
        u_p = request.form['password']
        if get_user(u_n) == -1:
            error = 'Invalid username'
        elif not password_check(u_n, u_p):
            error = 'Invalid password'
        else:
            session['role_id'] = get_role_id(u_n)
            session['user_id'] = get_user(u_n)
            session['logged_in'] = True
            u_n_s = get_user_ns(u_n)
            flash(f'Вы вошли, {u_n_s[0]} {u_n_s[1]}')
            dt = datetime.datetime.now()
            ndt = dt + datetime.timedelta(hours=3)
            flash(f"server date and time: {dt}")
            flash(f"Moscow date and time: {ndt}")

            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        u_n = request.form['username']
        u_i = None
        try:
            u_i = get_user(u_n)
        except TypeError as te:
            pass
        if u_i != -1:
            error = 'Такой ник занят'
        else:
            pas = request.form['password']
            u_na = request.form['Name']
            u_su = request.form['Surname']
            if (pas and u_na and u_su):
                new_u = add_user(u_n, pas, u_na, u_su)
                role = get_role(u_n)
                u_i = get_user(u_n)
                session['user_id'] = u_i
                session['logged_in'] = True
                flash(f'You were registered as {u_na} {u_su}. You are {role}.')
                return redirect(url_for('show_entries'))
            else:
                error = 'Нужно заполнить все поля'
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['role_id'] = -1
    session['user_id'] = -1

    flash('You were logged out')
    return redirect(url_for('show_entries'))

def add_user(username, password, name, surname):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT OR IGNORE into User (username, password, name, surname) values (?, ?, ?, ?)
    ''', (username, password, name, surname))
        conn.commit()
        cur.execute('''SELECT user_id FROM User WHERE username = ? ''', (username,))
        u_i = cur.fetchone()[0]
        return u_i
    except BaseException as be:
        print('add user error: ',type(be), be)
        return be

def add_userrole(user_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''INSERT OR IGNORE into UserRoles (user_id, role_id) values (?, &)''', (user_id, 1))
        conn.commit()
    except BaseException as be:
        print('add user error: ',type(be), be)
        return be

def get_user(username):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''SELECT user_id FROM User WHERE username = ? ''', (username,))
        u_i = cur.fetchone()[0]
        return u_i
    except BaseException as be:
        print('get user error: ',type(be), be)
        if  type(be) == TypeError:
            return -1
        return be

def password_check(u_n, u_p):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''SELECT password FROM User WHERE username = ? ''', (u_n,))
        pas = cur.fetchone()[0]
        if pas == u_p:
            return True
        else:
            return False
    except BaseException as be:
        print('password_check error: ',type(be), be)
        return be

def get_role(username):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''SELECT Roles.name FROM Roles inner join UserRoles on roles.role_id = UserRoles.role_id inner join User on UserRoles.user_id = user.user_id where  User.username = ? ''', (u_n,))
        role = cur.fetchone()[0]
        return role
    except BaseException as be:
        print('get role error: ',type(be), be)
        return be

def get_role_id(username):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''SELECT role_id FROM UserRoles inner join User on UserRoles.user_id = User.user_id where  User.username = ? ''', (username,))
        role_id = cur.fetchone()[0]
        return role_id
    except BaseException as be:
        print('get role_id error: ',type(be), be)
        return be

def get_user_ns(username):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''SELECT name, surname FROM User WHERE username = ? ''', (username,))
        name_surname = cur.fetchall()[0]
        print(name_surname[0], name_surname[1])
        return name_surname
    except BaseException as be:
        print('get user name_surname rror: ',type(be), be)
        return be



"""
QUESTIONS AND ANSWERS
"""
@app.route('/add_block', methods=['POST', 'GET'])
def add_block():
    if not (session.get('logged_in')):
        abort(401)
    if not session.get('role_id') > 4:
        abort(405)
    form = AddBlockForm()
    if form.validate_on_submit():
        dat = form.blockname.data
        flash(f"something {dat}")
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute('''INSERT INTO Blocks (block_name, is_open) values (?, 0)''', (dat,))
            conn.commit()
            flash('New block was successfully added')
            return redirect(url_for('show_entries'))
        except BaseException as be:
            print('add block error: ', type(be), be)
            return be
        return redirect(url_for('show_entries'))
    return render_template('add_block_form.html', title='add block', form=form)

@app.route('/manage_blocks', methods=['POST', 'GET'])
def manage_blocks():
    if not (session.get('logged_in')):
        abort(401)
    if not session.get('role_id') > 4:
        abort(405)
    try:
        print('Show blocks 1')
        db = get_db()
        print('2')
        cur = db.execute('select block_id, block_name, is_open from Blocks order by block_id ASC')
        blocks = cur.fetchall()
        print('3', blocks)
        return render_template('show_blocks.html', blocks=blocks)
    except BaseException as be:
        print('show blocks error: ',type(be), be)
        return be
    #return render_template('show_blocks.html')

@app.route('/change_block_state', methods=['POST'])
def change_block_state():
    if not (session.get('logged_in')):
        abort(401)
    if not session.get('role_id') > 4:
        abort(405)
    print('try to process the form')
    if request.method == 'POST':
        block_id = request.form['block_id']
        state = request.form['change_state']
        print('suc!', block_id, state)
    try:
        print('change blocks 1')
        conn = get_db()
        cur = conn.cursor()
        print('2')
        c = cur.execute('UPDATE Blocks SET is_open = ? WHERE block_id = ?', (state, block_id))
        print(c)
        conn.commit()
        print('3')
        return redirect(url_for('manage_blocks'))
    except BaseException as be:
        print('change_block_state error: ',type(be), be)
        return be


@app.route('/add_question', methods=['POST', 'GET'])
def add_question():
    if not (session.get('logged_in')):
        abort(401)
    if not session.get('role_id') > 4:
        abort(405)
    form = AddQuestionForm()
    if form.validate_on_submit():
        b_i = int(form.block_id.data)
        q_t = str(form.question_text.data)
        c_a_t = str(form.correct_answer_text.data)
        flash(f"получены данные: {b_i}, {q_t}, {c_a_t}")
        conn = get_db()
        cur = conn.cursor()
        try:
            print('try to insert')
            cur.execute('''INSERT INTO QUESTIONS (block_id, question_text) values (?, ?)''', (b_i, q_t))
            print('try to select')
            cur.execute(''' SELECT question_id from questions where question_text = ?''', (q_t,))
            print('try to fetch')
            q_i = int(cur.fetchone()[0])
            flash(f'Вопрос с ид {q_i} добавлен')
            cur.execute('''INSERT INTO CorrectAnswers (question_id, c_answer_text) values (?, ?)''', (q_i, c_a_t))
            conn.commit()

            flash('New question was successfully added')
            return redirect(url_for('manage_questions'))
        except BaseException as be:
            print('add block error: ', type(be), be)
            return be
        return redirect(url_for('show_entries'))
    return render_template('add_question_form.html', title='add question', form=form)


@app.route('/manage_questions', methods=['POST', 'GET'])
def manage_questions():
    if not (session.get('logged_in')):
        abort(401)
    if not session.get('role_id') > 4:
        abort(405)
    try:
        print('Show questions 1')
        db = get_db()
        print('2')
        cur = db.execute('select question_id, block_id, question_text from QUESTIONS order by block_id ASC, question_id ASC')
        questions = cur.fetchall()
        print('got questions', questions)
        ques = list()
        print('try to get answers')
        for q in questions:
            d = dict()
            l = list()
            for c in q:
                print(type(c), c)
                l.append(c)
            print(l)
            print('try to add values')
            d['block_id'] = l[1]
            d['question_text'] = l[2]
            print('try to get answer text')
            try:
                cur = db.execute('select c_answer_text from CorrectAnswers where question_id = ?', (l[0],))
                res = cur.fetchone()[0]
            except BaseException as be:
                print('show blocks error: ',type(be), be)
                res = 'ОТВЕТА НЕТ'
            d['c_answer_text'] = res
            print(d)
            ques.append(d)
        print('3', ques)

        return render_template('manage_questions.html', ques=ques)
    except BaseException as be:
        print('show blocks error: ',type(be), be)
        return be
    #return render_template('show_blocks.html')
