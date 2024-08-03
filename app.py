from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}
notes = {}

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
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password", 401
    return render_template_string(open('templates/login.html').read())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists", 400
        users[username] = password
        notes[username] = []
        return redirect(url_for('login'))
    return render_template_string(open('templates/signup.html').read())

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_notes = notes[username]
    return render_template_string(open('templates/dashboard.html').read(), notes=user_notes)

@app.route('/note')
def new_note_form():
    return """
    <form hx-post="/add-note" hx-target="#notes-list" class="note">
        <textarea name="note" placeholder="Enter your note"></textarea>
        <button type="submit">Save Note</button>
    </form>
    """

@app.route('/add-note', methods=['POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    note = request.form['note']
    username = session['username']
    notes[username].append(note)
    is_red_flag = "red flag" in note.lower()
    return render_template_string(open('templates/note.html').read(), note=note, is_red_flag=is_red_flag)

if __name__ == '__main__':
    app.run(debug=True)
