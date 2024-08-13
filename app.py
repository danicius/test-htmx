from flask import Flask, render_template_string, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}
notes = {}
folders = {}
#Testing purposes to test certain functionalities like dashboard, note, add-note, get-add-person-form, create-folder

users = {'test': 'p'}
notes = {'test': ['Note 1', 'Note 2']}
def set_default_user():
    if 'email' not in session:
        session['email'] = 'test'  # Set a default user for development
        
@app.before_request
def before_request():
    if app.config.get('ENV') == 'development':
        set_default_user()


@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/home')
def home():
    return render_template_string(open('templates/home.html').read())

@app.route('/about')
def about():
    return render_template_string(open('templates/about.html').read())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password", 401
    return render_template_string(open('templates/login.html').read())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "email already exists", 400
        users[email] = password
        notes[email] = []
        return redirect(url_for('login'))
    return render_template_string(open('templates/signup.html').read())

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    user_notes = notes[email]
    return render_template_string(open('templates/dashboard.html').read(), folders=folders, notes=user_notes)

@app.route('/note')
def note():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template_string(open('templates/note.html').read())

@app.route('/add-note', methods=['POST'])
def add_note():
    if 'email' not in session:
        return redirect(url_for('login'))
    note = request.form['note']
    email = session['email']
    notes[email].append(note)
    is_red_flag = "red flag" in note.lower()
    return render_template_string(open('templates/note.html').read(), note=note, is_red_flag=is_red_flag)

@app.route('/get-add-person-form')
def get_add_person_form():
    return render_template_string('''
        <div id="addPersonForm">
            <input type="text" id="nicknameInput" name="name" placeholder="Enter nickname" class="border border-gray-300 px-4 py-2 rounded-lg">
            <button class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600" 
                    hx-post="/create-folder" 
                    hx-target="#folderList"
                    hx-swap="beforeend">Create Folder</button>
        </div>
    ''')

@app.route('/create-folder', methods=['POST'])
def create_folder():
    name = request.form.get('name')
    if name:
        if name not in folders:
            folders[name] = []
            return render_template_string('''
                <div class="folder bg-gray-200 p-4 mb-2 rounded-lg">
                    <h2 class="text-lg font-semibold">{{ name }}</h2>
                </div>
            ''', name=name)
        else:
            return "Folder already exists", 400
    return "Name is required", 400




if __name__ == '__main__':
    app.run(debug=True)
