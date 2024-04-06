import sqlite3

from flask import Flask, render_template, redirect,flash, session, request, g

DATABASE = './assignment3.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db =g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    cur.close()
    db.close()

def make_dict(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():

    if 'username' not in session:
        return redirect('/loginpage')
    
    return render_template('welcome.html', username=session['username'], admin=session['admin'])

@app.route('/loginpage')
def loginpage():

    if not request.args:
        return render_template('loginpage.html')
    
    username = request.args['username']
    password = request.args['password']

    db = get_db()
    db.row_factory = make_dict
    user = query_db('SELECT * FROM User WHERE username=? AND password=?',
                     [username, password], one=True)
    db.close()

    if user:
        session['username'] = user['username']
        session['admin'] = True if user['admin'] == 1 else False
        return redirect('/')
    else:
        return render_template('loginpage.html', error=True)

@app.route('/signup')
def signup():

    if not request.args:
        return render_template('signup.html')
    
    username = request.args['username']
    password = request.args['password']

    is_admin = 1 if 'admin' in request.args else 0

    db = get_db()
    db.row_factory = make_dict
    user = query_db('SELECT * FROM User WHERE username=?', [username], one=True)

    if user:
        return redirect('/signup')
    else:
        insert_db('INSERT INTO User VALUES(?, ?, ?)', (username, password, is_admin))
        return redirect('/loginpage')
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/loginpage')

@app.route('/feedback')
def feedback():
    if session['admin']:
        if 'username' not in session:
            return redirect('/loginpage')
        
        db = get_db()
        db.row_factory = make_dict
        feedbacks = query_db('SELECT * FROM Feedback WHERE instructor=?', [session['username']])
        db.close()

        print(feedbacks)

        return render_template('feedback_instructor.html', feedbacks=feedbacks)
    
    else:
        if 'username' not in session:
            return redirect('/loginpage')
        
        # GET
        if not request.args:

            db = get_db()
            db.row_factory = make_dict
            instructors = query_db('SELECT username FROM User WHERE admin = 1')
            db.close()
            return render_template('feedback.html', instructors = instructors)

        # POST
        else:

            instructor = request.args['username']
            question1 = request.args['question1']
            question2 = request.args['question2']
            question3 = request.args['question3']
            question4 = request.args['question4']

            # try: catch
            insert_db(
                'INSERT INTO Feedback ("Instructor", "Q1", "Q2", "Q3", "Q4") VALUES(?, ?, ?, ?, ?)',
                (instructor, question1, question2, question3, question4))
            flash('Submitted')
            return redirect('/')
        
# @app.route('/view')
# def view():
#     if 'username' not in session:
#         return redirect('/loginpage')
#     db = get_db()
#     db.row_factory = make_dict
#     if session['admin']:
#         view = query_db('SELECT * FROM Mark')
#     else:
#         view = query_db('SELECT * FROM Mark WHERE username=?', [session['username']])
#     db.close()
#
#     return render_template('view.html', username=session['username'], view=view, admin=session['admin'])

@app.route('/mark')
def mark():

    if 'username' not in session:
        return redirect('/login')

    if session['admin']:
        # get
        if not request.args:
            db = get_db()
            db.row_factory = make_dict
            students = query_db('SELECT DISTINCT username FROM User WHERE admin = 0')
            marks = query_db('SELECT name,grade,username  FROM mark order by username,name desc')
            db.close()

            return render_template('uploadmark.html', students=students,marks=marks)
        # post
        else:
            name = request.args['name']
            grade = float(request.args['grade'])
            username = request.args['username']

            insert_db(
                'INSERT INTO Mark (name, grade, username) VALUES (?, ?, ?)',
                (name, grade, username))

            return redirect('/mark')
    else:
        db = get_db()
        db.row_factory = make_dict
        marks = query_db('SELECT name,grade,username  FROM mark where username=?', [session['username']])
        db.close()
        return render_template('showmark.html', marks=marks)


@app.route('/remark')
def remark():
    if 'username' not in session:
        return redirect('/login')
    
    if session['admin']:
        if not request.args:
            db = get_db()
            db.row_factory = make_dict
            remarks = query_db(
                'SELECT * FROM Remark, Mark WHERE Remark.mark_id = Mark.mark_id')
            db.close()
            return render_template('remarks.html', remarks=remarks)
    
    else:
        if not request.args:
            return render_template('showmark.html')

        mark_id = request.args['mark_id']
        reason = request.args['reason']
        insert_db('INSERT INTO Remark VALUES(?, ?)', (mark_id, reason))
        return redirect('/success')


@app.route('/success')
def success():
    if 'username' not in session:
        return redirect('/login')
    return render_template('success.html')



if __name__ == '__main__':
   app.secret_key = 'sb cscb20'
   app.run(debug=True)